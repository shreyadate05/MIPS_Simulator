from mipsHelper import *
from instruction import *
from scoreboard import *
import logging
import mipsDefs

log = logging.getLogger("MIPS Pipeline ")

allQueue   = []
fetchQueue = []
issueQueue = []
readQueue = []
execQueue = []
writeQueue = []

clockCount = 1
programCounter = 1
isStalled = False
done = False

structDependencyDAG = {}
rawDependencyDAG    = {}

def fetch():
    global allQueue, fetchQueue, issueQueue, structDependencyDAG, rawDependencyDAG
    global clockCount, isStalled, done, programCounter

    log.debug("Fetch Queue Before: ")
    logQueue(fetchQueue)

    if isStalled:
        return

    fetchQueue.append(mipsDefs.instructions[allQueue.pop(0)])
    log.debug("Fetched instruction " + str(fetchQueue[0].id) + ": " + fetchQueue[0].inst+ " at clock cycle " + str(clockCount))

    scoreboard = createScoreboard(fetchQueue[0], clockCount)
    mipsDefs.resultMatrix.append(scoreboard)

    log.debug("Fetch Queue After: ")
    logQueue(fetchQueue)


def issue():
    global fetchQueue, issueQueue, readQueue, structDependencyDAG, rawDependencyDAG
    global clockCount, isStalled, done

    log.debug("Issue Queue Before: ")
    logQueue(issueQueue)

    if len(fetchQueue) == 0:
        return

    currInst = fetchQueue[0]
    if not continueExecution(isStalled, currInst.id, structDependencyDAG, rawDependencyDAG):
        return

    if not isUnitAvailable(currInst, structDependencyDAG):
        isStalled = True
        log.debug("Structural Hazard for instruction " + str(currInst.id) + ". Pipeline is stalled.")
        return

    if isWAW(currInst, structDependencyDAG):
        isStalled = True
        log.debug("WAW hazard for instruction " + str(currInst.id) + ". Pipeline is stalled.")
        return

    isStalled = False
    occupyUnit(currInst)
    issueQueue.append(fetchQueue.pop(0))
    log.debug("Issued instruction " + str(issueQueue[0].id) + ": " + issueQueue[0].inst+ " at clock cycle " + str(clockCount))
    log.debug("Issue Queue After: ")
    logQueue(issueQueue)


def read():
    global readQueue, execQueue, writeQueue, structDependencyDAG, rawDependencyDAG
    global clockCount, isStalled, done

    log.debug("Read Queue Before: ")
    logQueue(readQueue)

    if isStalled:
        return

    if len(issueQueue) != 0:
       readQueue.append(issueQueue.pop(0))

    for inst in readQueue:
        if isRAW(inst, rawDependencyDAG):
            isStalled = True
            log.debug("RAW hazard for instruction " + str(inst.id) + ". Pipeline is stalled.")
            continue
        inst.isReadDone = True
        log.debug("Read instruction " + str(readQueue[0].id) + ": " + readQueue[0].inst+ " at clock cycle " + str(clockCount))

    log.debug("Read Queue After: ")
    logQueue(readQueue)


def execute():
    global execQueue, writeQueue, structDependencyDAG, rawDependencyDAG
    global clockCount, isStalled, done

    log.debug("Exec Queue Before: ")
    logQueue(execQueue)

    for inst in readQueue:
        if inst.isReadDone:
            execQueue.append(inst)

    for inst in execQueue:
        if not continueExecution(isStalled, inst.id, structDependencyDAG, rawDependencyDAG):
            continue

        mipsDefs.units[inst.unit].availableCycleCounts -= 1
        if mipsDefs.units[inst.unit].availableCycleCounts <= 0:
            inst.isExecutionDone = True
            log.debug("Executed instruction " + str(execQueue[0].id) + ": " + execQueue[0].inst + " at clock cycle " + str(clockCount))
        else:
            log.debug("Currently executing instruction " + str(execQueue[0].id) + ": " + execQueue[0].inst + " at clock cycle " + str(clockCount))

    for inst in execQueue:
        if inst in readQueue and inst.isReadDone:
            readQueue.remove(inst)

    log.debug("Exec Queue After: ")
    logQueue(execQueue)


def write():
    global writeQueue, structDependencyDAG, rawDependencyDAG
    global clockCount, isStalled, done, programCounter

    log.debug("Write Queue Before: ")
    logQueue(writeQueue)
    prevStallVal = isStalled

    if len(execQueue) == 0:
        return

    currInst = execQueue[0]
    if not continueExecution(isStalled, currInst.id, structDependencyDAG, rawDependencyDAG):
        return

    if not currInst.isExecutionDone:
        return

    writeQueue.append(execQueue.pop(0))
    currInst.isComplete = True
    structStall = isStallResolved(currInst.id, structDependencyDAG)
    rawStall = isStallResolved(currInst.id, rawDependencyDAG)
    isStalled = not(structStall or rawStall)
    currStallVal = isStalled
    freeUnit(currInst)

    log.debug("Write Back completed for instruction " + str(writeQueue[0].id) + ": " + writeQueue[0].inst + " at clock cycle " + str(clockCount))

    logPrevAndCurrStall(prevStallVal, currStallVal)
    if prevStallVal == True and currStallVal == False:
        clockCount += 1
    #clockCount += 1

    writeQueue.pop(0)
    log.debug("Write Queue After")
    logQueue(writeQueue)

def start():
    global clockCount, done, programCounter, allQueue, isStalled, structDependencyDAG, rawDependencyDAG
    global fetchQueue, issueQueue, readQueue, execQueue, writeQueue

    res = []
    log.debug("Starting Pipeline...\n\n")

    allQueue = [i for i in range(1,len(mipsDefs.instructions)+1)]
    while not done:
        log.debug("Clock Cycle: " + str(clockCount))
        write()
        execute()
        read()
        issue()
        fetch()

        if len(allQueue) == 0:
            done = True

        log.debug("Issue Stage dependency DAG is: ")
        log.debug(structDependencyDAG)

        log.debug("Read stage dependency DAG is: ")
        log.debug(rawDependencyDAG)

        clockCount += 1
        log.debug("\n")

    return res
