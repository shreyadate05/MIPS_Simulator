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

instructionDependencyDAG = {}

def fetch():
    global allQueue, fetchQueue, issueQueue, instructionDependencyDAG
    global clockCount, isStalled, done, programCounter

    if not continueExecution(isStalled, programCounter, instructionDependencyDAG):
        return

    fetchQueue.append(mipsDefs.instructions[allQueue.pop(0)])
    log.debug("Fetched instruction " + str(fetchQueue[0].id) + " at clock cycle " + str(clockCount))

    scoreboard = createScoreboard(fetchQueue[0], clockCount)
    mipsDefs.resultMatrix.append(scoreboard)

def issue():
    global fetchQueue, issueQueue, readQueue, instructionDependencyDAG
    global clockCount, isStalled, done

    if len(fetchQueue) == 0:
        return

    issueQueue.append(fetchQueue.pop(0))
    currInst = issueQueue[0]

    if not continueExecution(isStalled, currInst.id, instructionDependencyDAG):
        return

    if not isUnitAvailable(currInst, instructionDependencyDAG):
        isStalled = True
        return

    if isWAW(currInst, instructionDependencyDAG):
        isStalled = True
        return

    occupyUnit(mipsDefs.units[currInst.unit], currInst.id)
    log.debug("Issued instruction " + str(issueQueue[0].id) + " at clock cycle " + str(clockCount))

def read():
    global readQueue, execQueue, writeQueue, instructionDependencyDAG
    global clockCount, isStalled, done

    if len(readQueue) == 0:
        return

    currInst = readQueue[0]
    if not continueExecution(isStalled, currInst.id, instructionDependencyDAG):
        return


def execute():
    global execQueue, writeQueue, instructionDependencyDAG
    global clockCount, isStalled, done

    if len(execQueue) == 0:
        return

    currInst = execQueue[0]
    if not continueExecution(isStalled, currInst.id, instructionDependencyDAG):
        return


def write():
    global writeQueue, instructionDependencyDAG
    global clockCount, isStalled, done, programCounter

    if len(writeQueue) == 0:
        return

    currInst = writeQueue[0]
    if not continueExecution(isStalled, currInst.id, instructionDependencyDAG):
        return

    programCounter += 1

def start():
    global clockCount, done, programCounter, allQueue
    res = []

    log.debug("\n")
    log.debug("Starting Pipeline...\n\n")

    allQueue = [i for i in range(1,len(mipsDefs.instructions)+1)]
    while not done:
        write()
        execute()
        read()
        issue()
        fetch()

        if len(allQueue) == 0:
            done = True

        clockCount += 1
        log.debug("\n")

    return res
