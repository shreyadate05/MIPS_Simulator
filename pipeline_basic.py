from mipsHelper import *
import logging
import mipsDefs

log = logging.getLogger("MIPS Pipeline")

fetchQueue = []
issueQueue = []
readQueue = []
execQueue = []
writeQueue = []

clockCount = 1
programCounter = 0
isStalled = False
done = False

instructionDependencyDAG = {}

def fetch():
    global fetchQueue, issueQueue, instructionDependencyDAG
    global clockCount, isStalled, done
    log.debug("[ " + str(clockCount) + " ] FETCH")

    if not continueExecution(isStalled, programCounter, instructionDependencyDAG):
        return

    if len(fetchQueue) != 0:
        issueQueue.append(fetchQueue.pop(0))

    fetchQueue.append(mipsDefs.instructions[programCounter])
    fetchQueue[0].pipeStage = PipeStage.FETCH


def issue():
    global fetchQueue, issueQueue, readQueue, instructionDependencyDAG
    global clockCount, isStalled, done
    log.debug("[ " + str(clockCount) + " ] ISSUE")

    if len(issueQueue) == 0:
        return

    currInst = issueQueue[0]

    if not continueExecution(isStalled, currInst.id, instructionDependencyDAG):
        return

    if not isUnitAvailable(currInst):
        updateInstructionDependencyDAG(instructionDependencyDAG, currInst.id, mipsDefs.units[currInst.unit].instructionsOccupying)
        return

    occupyUnit(mipsDefs.units[currInst.unit], currInst.id)


def read():
    global readQueue, execQueue, writeQueue, instructionDependencyDAG
    global clockCount, isStalled, done
    log.debug("[ " + str(clockCount) + " ] READ")

    if len(readQueue) == 0:
        return

    currInst = readQueue[0]
    if not continueExecution(isStalled, currInst.id, instructionDependencyDAG):
        return


def execute():
    global execQueue, writeQueue, instructionDependencyDAG
    global clockCount, isStalled, done
    log.debug("[ " + str(clockCount) + " ] EXECUTE")

    if len(execQueue) == 0:
        return

    currInst = execQueue[0]
    if not continueExecution(isStalled, currInst.id, instructionDependencyDAG):
        return


def write():
    global writeQueue, instructionDependencyDAG
    global clockCount, isStalled, done, programCounter
    log.debug("[ " + str(clockCount) + " ] WRITE")

    if len(writeQueue) == 0:
        return

    currInst = writeQueue[0]
    if not continueExecution(isStalled, currInst.id, instructionDependencyDAG):
        return


    programCounter += 1

def start():
    global clockCount, done
    res = []

    log.debug("\n")
    log.debug("Starting Pipeline...\n\n")

    while not done:
        fetch()
        issue()
        read()
        execute()
        write()

        clockCount += 1
        log.debug("\n")

    return res
