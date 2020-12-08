from mipsHelper import *
import logging
import mipsDefs

log = logging.getLogger("MIPS Pipeline ")

fetchQueue = []
issueQueue = []
readQueue = []
execQueue = []
writeQueue = []
doneQueue = []
unitsToFree = []
regsToFree = []

clockCount = 1
iCachePenalty = 0
dCachePenalty = 0
done = False

occupiedRegisters = { }
mipsDefs.programCounter = 1
programCounter = 0
iCachePenalty = 0
iCacheMissClockCount = 0
res = []

def fetch():
    global fetchQueue, issueQueue, iCacheMissClockCount
    global clockCount, programCounter, iCachePenalty

    if programCounter >= len(mipsDefs.instructions):
        return

    isCahceHit = isInstInICache(programCounter)
    if not isCahceHit:
        mipsDefs.instructions[programCounter].iCache = 'M'
        mipsDefs.iCacheMisses += 1
    else:
        if mipsDefs.instructions[programCounter].iCache == 'X':
            mipsDefs.instructions[programCounter].iCache = 'H'
            mipsDefs.iCacheHits += 1

    if not isCahceHit:
        iCachePenalty = mipsDefs.iCachePenalty
        iCacheMissClockCount = clockCount
        return

    if len(issueQueue) != 0:
        return

    if isCahceHit:
        if (iCacheMissClockCount + iCachePenalty == clockCount) or (iCacheMissClockCount == 0 and iCachePenalty == 0):
            issueQueue.append(mipsDefs.instructions[programCounter])
            log.debug("Fetched instruction " + str(issueQueue[0].id) + ": " + issueQueue[0].inst + " at clock cycle " + str(clockCount))
            issueQueue[0].IF = str(clockCount)
            programCounter += 1
            iCachePenalty = 0
            iCacheMissClockCount = 0

    log.debug("iCachePenalty: ")
    log.debug(iCachePenalty)
    log.debug("iCacheMissClockCount: ")
    log.debug(iCacheMissClockCount)


def issue():
    global fetchQueue, issueQueue, readQueue, occupiedRegisters, programCounter, iCachePenalty
    global clockCount, finalOutputString, res, unitsToFree, iCacheMissClockCount

    log.debug("Issue Queue Before: ")
    logQueue(issueQueue)
    ret = -1

    if len(issueQueue) == 0:
        return ret

    currInst = issueQueue[0]

    if not isUnitAvailable(currInst):
        log.debug("Structural Hazard for instruction " + str(currInst.id) + ". Pipeline is stalled.")
        currInst.Struct = 'Y'
        return ret

    if isWAW(currInst, occupiedRegisters):
        log.debug("WAW hazard for instruction " + str(currInst.id) + ". Pipeline is stalled.")
        currInst.WAW = 'Y'
        return ret

    if currInst.type == InstructionType.CTRL and currInst.opcode == 'J':
        deLim = "-"
        ret = resolveBranch(currInst, currInst.operand1)
        currInst.ID = str(clockCount)
        unitsToFree.append(currInst)
        addResult(currInst, res)
        log.debug("Issued instruction " + str(issueQueue[0].id) + ": " + issueQueue[0].inst + " at clock cycle " + str(clockCount))
        issueQueue.pop(0)

    occupyUnit(currInst)
    log.debug("Issued instruction " + str(issueQueue[0].id) + ": " + issueQueue[0].inst+ " at clock cycle " + str(clockCount))
    currInst.ID = str(clockCount)
    if iCacheMissClockCount + iCachePenalty < clockCount:
        iCacheMissClockCount = clockCount
    readQueue.append(issueQueue.pop(0))
    log.debug("Issue Queue After: ")
    logQueue(issueQueue)
    return ret

def read():
    global readQueue, execQueue, writeQueue, occupiedRegisters
    global clockCount, unitsToFree, programCounter

    ret = -1
    log.debug("Read Queue Before: ")
    logQueue(readQueue)

    if len(readQueue) == 0:
        return ret

    instToExec = []
    branchInstToRemove = []
    ret = -1
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
            ret = resolveBranch(inst, inst.operand3)
            inst.IR = str(clockCount)
            unitsToFree.append(inst)
            addResult(inst, res)
            log.debug(res)
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

    log.debug("Read Queue After: ")
    logQueue(readQueue)
    return ret


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
        sourceOperands = getSourceOperands(inst)
        #print(sourceOperands)
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
    addResult(currInst, res)
    log.debug(res)
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
    global issueQueue, writeQueue, execQueue, readQueue, allQueue, programCounter
    log.debug("Starting Pipeline...\n\n")

    res.append(['ID', 'Instruction', 'FETCH', 'ISSUE', 'READ', 'EXECUTE', 'WRITE', 'RAW', 'WAW', 'STRUCT', 'I-Cache', 'D-Cache'])
    while not done:
        log.debug("Clock Cycle: " + str(clockCount))
        freeUnits(unitsToFree)
        freeRegisters(regsToFree, occupiedRegisters)
        log.debug("Occupied Registers Map: ")
        log.debug(occupiedRegisters)
        log.debug("Registers Map: ")
        log.debug(mipsDefs.registers)
        log.debug("Program Counter: ")
        log.debug(programCounter)
        log.debug("I-Cache: ")
        log.debug(mipsDefs.iCache)

        write()
        execute()
        ret1 = read()
        ret2 = issue()
        fetch()

        if programCounter == len(mipsDefs.instructions):
            done = True

        if ret1 != None and ret1 != -1 :
            issueQueue.clear()
            readQueue.clear()
            programCounter = ret1

        if ret2 != None and ret2 != -1 :
            issueQueue.clear()
            readQueue.clear()
            programCounter = ret2


        clockCount += 1
        log.debug("\n")

    log.debug(res)
    resultString = ""
    for row in res:
        resultString += printResult(row) + "\n"
        print()

    return resultString
