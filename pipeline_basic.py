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

    if isStalled:
        return

    fetchQueue.append(mipsDefs.instructions[allQueue.pop(0)])
    log.debug("Fetched instruction " + str(fetchQueue[0].id) + " at clock cycle " + str(clockCount))

    scoreboard = createScoreboard(fetchQueue[0], clockCount)
    mipsDefs.resultMatrix.append(scoreboard)

def issue():
    global fetchQueue, issueQueue, readQueue, structDependencyDAG, rawDependencyDAG
    global clockCount, isStalled, done

    if len(fetchQueue) == 0:
        return

    issueQueue.append(fetchQueue.pop(0))
    currInst = issueQueue[0]

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

    occupyUnit(currInst)
    log.debug("Issued instruction " + str(issueQueue[0].id) + " at clock cycle " + str(clockCount))

def read():
    global readQueue, execQueue, writeQueue, structDependencyDAG, rawDependencyDAG
    global clockCount, isStalled, done

    if len(issueQueue) == 0:
        return

    readQueue.append(issueQueue.pop(0))
    currInst = readQueue[0]

    if not continueExecution(isStalled, currInst.id, structDependencyDAG, rawDependencyDAG):
        return

    if isRAW(currInst, rawDependencyDAG):
        isStalled = True
        log.debug("RAW hazard for instruction " + str(currInst.id) + ". Pipeline is stalled.")
        return

    log.debug("Read instruction " + str(readQueue[0].id) + " at clock cycle " + str(clockCount))


def execute():
    global execQueue, writeQueue, structDependencyDAG, rawDependencyDAG
    global clockCount, isStalled, done

    if len(readQueue) == 0:
        return

    execQueue.append(readQueue.pop(0))
    currInst = execQueue[0]
    if not continueExecution(isStalled, currInst.id, structDependencyDAG, rawDependencyDAG):
        return

    if mipsDefs.units[currInst.unit].availableCycleCounts == 1:
        currInst.isExecutionDone = True
    mipsDefs.units[currInst.unit].availableCycleCounts = mipsDefs.units[currInst.unit].availableCycleCounts - 1

    log.debug("Executed instruction " + str(execQueue[0].id) + " at clock cycle " + str(clockCount))


def write():
    global writeQueue, structDependencyDAG, rawDependencyDAG
    global clockCount, isStalled, done, programCounter

    if len(execQueue) == 0:
        return

    currInst = execQueue[0]
    if not currInst.isExecutionDone:
        return

    writeQueue.append(execQueue.pop(0))
    currInst = writeQueue[0]
    if not continueExecution(isStalled, currInst.id, structDependencyDAG, rawDependencyDAG):
        return

    currInst.isComplete = True
    structStall = isStallResolved(currInst.id, structDependencyDAG)
    rawStall = isStallResolved(currInst.id, rawDependencyDAG)
    isStalled = structStall or rawStall
    freeUnit(currInst)

    programCounter += 1
    log.debug("Write Back completed for instruction " + str(execQueue[0].id) + " at clock cycle " + str(clockCount))

def start():
    global clockCount, done, programCounter, allQueue, isStalled, structDependencyDAG, rawDependencyDAG
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
