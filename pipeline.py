from mipsHelper import *
import logging
import mipsDefs

log = logging.getLogger("MIPS Pipeline ")

allQueue   = []
fetchQueue = []
issueQueue = []
readQueue = []
execQueue = []
writeQueue = []
doneQueue = []
unitsToFree = []
regsToFree = []

clockCount = 1
done = False

occupiedRegisters = { }
mipsDefs.programCounter = 1
res = []

def fetch():
    global allQueue, fetchQueue, issueQueue
    global clockCount

    print("PC: ", mipsDefs.programCounter)

    if len(issueQueue) != 0:
        return

    if len(allQueue) == 0:
        return

    if mipsDefs.programCounter >= len(mipsDefs.instructions):
        return

    issueQueue.append(mipsDefs.instructions[mipsDefs.programCounter])
    log.debug("Fetched instruction " + str(issueQueue[0].id) + ": " + issueQueue[0].inst+ " at clock cycle " + str(clockCount))
    issueQueue[0].IF = str(clockCount)
    mipsDefs.programCounter += 1

def issue():
    global fetchQueue, issueQueue, readQueue, occupiedRegisters
    global clockCount, finalOutputString, res, unitsToFree, allQueue

    log.debug("Issue Queue Before: ")
    logQueue(issueQueue)

    if len(issueQueue) == 0:
        return


    currInst = issueQueue[0]

    if currInst.opcode == "HLT":
        return

    if not isUnitAvailable(currInst):
        log.debug("Structural Hazard for instruction " + str(currInst.id) + ". Pipeline is stalled.")
        currInst.Struct = 'Y'
        return

    if isWAW(currInst, occupiedRegisters):
        log.debug("WAW hazard for instruction " + str(currInst.id) + ". Pipeline is stalled.")
        currInst.WAW = 'Y'
        return

    if currInst.type == InstructionType.CTRL and currInst.opcode == 'J':
        deLim = "-"
        resolveBranch(currInst, currInst.operand1)
        currInst.ID = str(clockCount)
        unitsToFree.append(currInst)
        finalOutputString = str(currInst.id) + deLim + currInst.inst + deLim + currInst.IF + deLim + currInst.ID + deLim + currInst.IR + deLim + currInst.EX + deLim + currInst.WB + deLim + currInst.RAW + deLim + currInst.WAW + deLim + currInst.Struct + "\n"
        res.append(finalOutputString)
        log.debug("Issued instruction " + str(issueQueue[0].id) + ": " + issueQueue[0].inst + " at clock cycle " + str(clockCount))
        issueQueue.pop(0)

    occupyUnit(currInst)
    log.debug("Issued instruction " + str(issueQueue[0].id) + ": " + issueQueue[0].inst+ " at clock cycle " + str(clockCount))
    currInst.ID = str(clockCount)

    readQueue.append(issueQueue.pop(0))
    log.debug("Issue Queue After: ")
    logQueue(issueQueue)



def read():
    global readQueue, execQueue, writeQueue, occupiedRegisters
    global clockCount, unitsToFree

    branchResolved = False

    log.debug("Read Queue Before: ")
    logQueue(readQueue)

    if len(readQueue) == 0:
        return

    instToExec = []
    branchInstToRemove = []
    for i in range(len(readQueue)):
        inst = readQueue[i]
        if isWAW(inst, occupiedRegisters):
            log.debug("WAW hazard for instruction " + str(inst.id) + ". Pipeline is stalled.")
            inst.WAW = 'Y'
            continue

        if isRAW(inst, occupiedRegisters):
            inst.RAW = 'Y'
            log.debug("RAW hazard for instruction " + str(inst.id) + ". Pipeline is stalled.")
            continue

        if inst.type == InstructionType.CTRL:
            deLim = "-"
            branchResolved = True
            resolveBranch(inst, inst.operand3)
            inst.IR = str(clockCount)
            unitsToFree.append(inst)
            finalOutputString = str(inst.id) + deLim + inst.inst + deLim + inst.IF + deLim + inst.ID + deLim + inst.IR + deLim + inst.EX + deLim + inst.WB + deLim + inst.RAW + deLim + inst.WAW + deLim + inst.Struct + "\n"
            res.append(finalOutputString)
            log.debug("Read instruction " + str(inst.id) + ": " + inst.inst + " at clock cycle " + str(clockCount))
            branchInstToRemove.append(inst)
            continue

        if inst.type != InstructionType.INV and inst.type != InstructionType.SPCL and inst.type != InstructionType.CTRL:
            occupiedRegisters[inst.operand1] = 1
        inst.IR = str(clockCount)
        log.debug("Read instruction " + str(inst.id) + ": " + inst.inst+ " at clock cycle " + str(clockCount))
        instToExec.append(inst)

    for i in range(len(branchInstToRemove)):
        inst = branchInstToRemove[i]
        readQueue.remove(inst)

    for i in range(len(instToExec)):
        inst = instToExec[i]
        execQueue.append(inst)
        readQueue.remove(inst)

    if branchResolved:
        issueQueue.clear()
        readQueue.clear()

    log.debug("Read Queue After: ")
    logQueue(readQueue)


def execute():
    global execQueue, writeQueue, structDependencyDAG, rawDependencyDAG
    global clockCount, isStalled, done

    log.debug("Exec Queue Before: ")
    logQueue(execQueue)

    if len(execQueue) == 0:
        return

    instToWrite = []
    for i in range(len(execQueue)):
        inst = execQueue[i]
        if mipsDefs.units[inst.unit].totalCycleCounts + int(mipsDefs.instructions[inst.id].IR) == clockCount:
            inst.isExecutionDone = True
            inst.EX = str(clockCount)
            runInstruction(inst)
            log.debug("Executed instruction " + str(inst.id) + ": " + inst.inst + " at clock cycle " + str(clockCount))
            instToWrite.append(inst)
        else:
            log.debug("Currently executing instruction " + str(inst.id) + ": " + inst.inst + " at clock cycle " + str(clockCount))

    for i in range(len(instToWrite)):
        inst = instToWrite[i]
        writeQueue.append(inst)
        execQueue.remove(inst)

    log.debug("Exec Queue After: ")
    logQueue(execQueue)


def write():
    global writeQueue, doneQueue, unitsToFree
    global clockCount, done, res
    deLim = " - "

    log.debug("Write Queue Before: ")
    logQueue(writeQueue)

    if len(writeQueue) == 0:
        return

    currInst = writeQueue[0]
    currInst.WB = str(clockCount)
    finalOutputString = str(currInst.id) + deLim + currInst.inst + deLim + currInst.IF + deLim + currInst.ID + deLim + currInst.IR + deLim + currInst.EX + deLim + currInst.WB + deLim + currInst.RAW + deLim + currInst.WAW + deLim + currInst.Struct + "\n"
    res.append(finalOutputString)
    log.debug("Write Back completed for instruction " + str(currInst.id) + ": " + currInst.inst + " at clock cycle " + str(clockCount))
    log.debug("Completed instruction: ")
    log.debug(currInst)
    unitsToFree.append(currInst)
    if currInst.type != InstructionType.INV and currInst.type != InstructionType.SPCL and currInst.type != InstructionType.CTRL:
        regsToFree.append(currInst.operand1)
    doneQueue.append(writeQueue.pop(0))

    log.debug("Write Queue After")
    logQueue(writeQueue)


def startMIPS():
    global clockCount, done, allQueue, doneQueue, unitsToFree, occupiedRegisters, regsToFree, finalOutputString, res
    global issueQueue, writeQueue, execQueue, readQueue, allQueue
    log.debug("Starting Pipeline...\n\n")

    allQueue = [i for i in range(1,len(mipsDefs.instructions)+1)]
    while not done:
        log.debug("Clock Cycle: " + str(clockCount))
        log.debug("allQueue is: ")
        log.debug(allQueue)
        freeUnits(unitsToFree)
        freeRegisters(regsToFree, occupiedRegisters)
        log.debug("Occupied Registers Map: ")
        log.debug(occupiedRegisters)
        log.debug("Registers Map: ")
        log.debug(mipsDefs.registers)
        log.debug("Program Counter: ")
        log.debug(mipsDefs.programCounter)

        write()
        execute()
        read()
        issue()
        fetch()

        if len(issueQueue) == 0 and len(readQueue) == 0 and len(execQueue) == 0 and len(writeQueue) == 0:
            done = True

        clockCount += 1
        log.debug("\n")

    log.debug(res)
    for row in res:
        print(row)
        print()

    return res
