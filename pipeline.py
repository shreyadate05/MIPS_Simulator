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
iCacheMissQueue = []
iCacheMissClockCount = 0
res = []
dcacheEndCycle = 0

icache_bus_cc = 0
dcache_bus_cc = 0

busAccess = True

def fetch():
    global fetchQueue, issueQueue, iCacheMissClockCount, iCacheMissQueue, icache_bus_cc
    global clockCount, programCounter, iCachePenalty, busAccess, dcacheEndCycle

    if programCounter >= len(mipsDefs.instructions):
        return

    isCahceHit = isInstInICache(programCounter)
    if mipsDefs.instructions[programCounter].opcode != 'HLT':
        if not isCahceHit:
            mipsDefs.instructions[programCounter].iCache = 'M'
            mipsDefs.iCacheMisses += 1
            icache_bus_cc = clockCount
            log.debug(dcacheEndCycle)
        else:
            if mipsDefs.instructions[programCounter].iCache == 'X':
                mipsDefs.instructions[programCounter].iCache = 'H'
                mipsDefs.iCacheHits += 1

    if not isCahceHit:
        iCachePenalty = mipsDefs.iCachePenalty
        iCacheMissClockCount = clockCount
        return

    if len(issueQueue) != 0 and iCacheMissClockCount + iCachePenalty == clockCount:
        iCacheMissClockCount = 0
        iCachePenalty = 0

    if len(issueQueue) != 0:
        return

    if isCahceHit:
        if (iCacheMissClockCount + iCachePenalty == clockCount) or (iCacheMissClockCount == 0 and iCachePenalty == 0):
            issueQueue.append(mipsDefs.instructions[programCounter])
            if dcacheEndCycle == clockCount:
                busAccess = False
                log.debug("Setting bus access to false")
            if dcacheEndCycle > clockCount:
                busAccess = True
                log.debug("Setting bus access to true again.")
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
    log.debug(readQueue)
    log.debug("ret: ")
    log.debug(ret)

    if len(readQueue) == 0:
        return ret

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
            ret = resolveBranch(inst, inst.operand3)
            inst.IR = str(clockCount)
            unitsToFree.append(inst)
            addResult(inst, res)
            log.debug(res)
            log.debug("Read instruction " + str(inst.id) + ": " + inst.inst + " at clock cycle " + str(clockCount))
            branchInstToRemove.append(inst)
            continue

        inst.IR = str(clockCount)
        if inst.type != InstructionType.INV and inst.type != InstructionType.SPCL and inst.type != InstructionType.CTRL:
            occupiedRegisters[inst.operand1] = 1
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
    log.debug(readQueue)
    log.debug("ret: ")
    log.debug(ret)

    return ret


def execute():
    global execQueue, writeQueue, structDependencyDAG, rawDependencyDAG
    global clockCount, isStalled, done, busAccess, dcacheEndCycle, icache_bus_cc

    log.debug("Exec Queue Before: ")
    logQueue(execQueue)

    if len(execQueue) == 0:
        return

    instToWrite = []
    for i in range(len(execQueue)):
        inst = execQueue[i]
        canExec = False

        addresses = getAddresses(inst)
        log.debug("Addresses are: ")
        log.debug(addresses)
        cacheResolved = False
        if addresses == []:
            canExec = True
        else:
            if not inst.checkedDCache:
                dCacheHit = isInDataCache(inst, addresses, clockCount)
                if dCacheHit:
                    log.debug("data cache hit for inst " + str(inst.id) )
                    canExec = True
                else:
                    cacheResolved = False
                    canExec = False
                    log.debug("Cache Miss. Wait till clock cycle: ")
                    log.debug(str(inst.dCachePenalty + clockCount))
                    log.debug("dcacheEndCycle before: " + str(dcacheEndCycle))
                    log.debug("dCacheEndClock before: " + str(inst.dCacheEndClock))
                    if clockCount - icache_bus_cc < 12:
                        log.debug("Bus unavailable. Data cache end clock updated to ")
                        inst.dCacheEndClock += 10
                        dcacheEndCycle = inst.dCacheEndClock
                    else:
                        dcacheEndCycle = inst.dCacheEndClock
                    log.debug("dcacheEndCycle after: " + str(dcacheEndCycle))
            else:
                if inst.dCacheEndClock + mipsDefs.units[inst.unit].totalCycleCounts - 1 == clockCount:
                    if not busAccess:
                        inst.dCacheEndClock += 10
                        log.debug("Bus unavailable. Data cache end clock updated to ")
                        log.debug(inst.dCacheEndClock)
                        dcacheEndCycle = inst.dCacheEndClock
                        busAccess = True
                    else:
                        busAccess = True
                        inst.dCacheEndClock = 0
                        dcacheEndCycle = 0
                        log.debug("Latency handled. Now can start executing instruction")
                        cacheResolved = True
                        canExec = True
        if canExec:
            if cacheResolved or (mipsDefs.units[inst.unit].totalCycleCounts + int(mipsDefs.instructions[inst.id].IR) == clockCount):
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
    global clockCount, done, allQueue, doneQueue, unitsToFree, occupiedRegisters, regsToFree, finalOutputString, res, iCacheMissQueue
    global issueQueue, writeQueue, execQueue, readQueue, allQueue, programCounter, iCachePenalty, iCacheMissClockCount
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
        log.debug("I-Cache Miss Queue: ")
        log.debug(iCacheMissQueue)
        log.debug("D-Cache: ")
        log.debug(mipsDefs.dCache)

        write()
        execute()
        ret1 = read()
        ret2 = issue()
        fetch()

        if programCounter >= len(mipsDefs.instructions):
            done = True

        if ret1 != -1 :
            issueQueue.clear()
            readQueue.clear()
            iCacheMissQueue.append(ret1)
            ret1 = -1

        if ret2 != -1 :
            issueQueue.clear()
            readQueue.clear()
            iCacheMissQueue.append(ret1)
            ret2 = -1

        if len(iCacheMissQueue) != 0 and iCachePenalty == 0 and iCacheMissClockCount == 0:
            oldPC = programCounter
            programCounter = iCacheMissQueue.pop(0)
            mipsDefs.iCacheAccesses = len(mipsDefs.iCacheCheckQueue)
            for i in range(programCounter, oldPC+1):
                mipsDefs.instructions[i].isExecutionDone = False
                mipsDefs.instructions[i].isComplete = False
                mipsDefs.instructions[i].dCachePenalty = 0
                mipsDefs.instructions[i].dCacheStartClock = 0
                mipsDefs.instructions[i].dCacheEndClock = 0
                mipsDefs.instructions[i].checkedDCache = False
                mipsDefs.instructions[i].checkedICache = False
                mipsDefs.iCacheCheckQueue = []

        clockCount += 1
        log.debug("\n")

    # for maintaining count in result file
    if len(mipsDefs.iCacheCheckQueue) != 0:
        mipsDefs.iCacheAccesses += len(mipsDefs.iCacheCheckQueue)

    log.debug(res)
    resultString = ""
    res[1:].sort(key = lambda x: int(x[2]))
    for row in res:
        resultString += printResult(row) + "\n"
        print()
    mipsDefs.resultMatrix = res
    return resultString
