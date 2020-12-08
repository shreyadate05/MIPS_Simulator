import mipsDefs
import re
from instruction import *
from unit import *
from logHelper import *

log = logging.getLogger("MIPS Helper   ")

# ----------------------------------------------------------------------------
# D-CACHE HELPERS
# ----------------------------------------------------------------------------
def updateDCacheHM(inst, w1, w2):
    if w1:
        inst.dCache[0] = 'H'
    else:
        inst.dCache[0] = 'M'

    if w2:
        inst.dCache[1] = 'H'
    else:
        inst.dCache[1] = 'M'
        log.debug("Data cache miss for instruction " + str(inst.id) + inst.inst)

def createDCache():
    mipsDefs.dCache[0] = [[-1,-1], [-2,-2]]
    mipsDefs.dCache[1] = [[-1,-1], [-2,-2]]

def getBlockAndSetNum(addr):
    blockNum = addr//16
    setNum = addr % 2
    log.debug("(Set Num, Block Num) for address: " + str(addr))
    log.debug("( " + str(setNum) + ", " + str(blockNum) + ")")
    return blockNum, setNum

def isBlockPresentInSet(set, block):
    if mipsDefs.dCache[set][0][0] == block:
        return True
    if mipsDefs.dCache[set][1][0] == block:
        return True
    return False

def updateCache(s, b, w, clock, inst):
    cc1 = mipsDefs.dCache[s][0][1]
    cc2 = mipsDefs.dCache[s][1][1]
    if cc1 <= cc2:
        mipsDefs.dCache[s][0][1] = clock
    else:
        mipsDefs.dCache[s][1][1] = clock

    if not w and cc1 <= cc2:
        mipsDefs.dCache[s][0][0] = b
        inst.dCachePenalty += 12

    if not w and cc1 > cc2:
        mipsDefs.dCache[s][1][0] = b
        inst.dCachePenalty += 12

def isInDataCache(inst, addresses, clockCycle):
    log.debug("D-Cache Before: ")
    log.debug(mipsDefs.dCache)

    inst.checkedDCache = True
    inst.dCacheStartClock = clockCycle
    log.debug(str(inst.dCacheStartClock))

    b1, s1 = getBlockAndSetNum(addresses[0])
    b2, s2 = getBlockAndSetNum(addresses[1])
    w1 = isBlockPresentInSet(s1, b1)
    w2 = isBlockPresentInSet(s2, b2)

    updateDCacheHM(inst, w1, w2)

    if s1 == s2 and b1 == b2:
        updateCache(s1, b1, w1, clockCycle, inst)
    else:
        updateCache(s1, b1, w1, clockCycle, inst)
        updateCache(s2, b2, w2, clockCycle, inst)

    log.debug("Instruction D-Cache Penalty: ")
    log.debug(str(inst.dCachePenalty))

    log.debug("D-Cache After: ")
    log.debug(mipsDefs.dCache)


def getAddresses(currInst):
    src = []
    if currInst.opcode == "LD" or currInst.opcode == "L.D" or currInst.opcode == "LW":
        base, offset = getBaseOffset(currInst.operand2)
        src.append(offset+base)
        src.append(offset+base+4)

    if currInst.opcode == "SD" or currInst.opcode == "S.D" or currInst.opcode == "SW":
        base, offset = getBaseOffset(currInst.operand2)
        src.append(base)
        src.append(offset+base)

    return src

# ----------------------------------------------------------------------------
# I-CACHE HELPERS
# ----------------------------------------------------------------------------
def printResult(res):
    s = ""
    for a, b, c, d, e, f, g, h, i, j, k, l in zip(res[::12], res[1::12], res[2::12], res[3::12], res[4::12], res[5::12], res[6::12], res[7::12], res[8::12], res[9::12],res[10::12], res[11::12]):
        s = '{:<25}{:<25}{:<25}{:<25}{:<25}{:<25}{:<25}{:<25}{:<25}{:<25}{:<25}{:<}'.format(a,b,c,d,e,f,g,h,i,j,k,l)
    return s

def addResult(currInst, res):
    row = []
    row.append(str(currInst.id))
    row.append(currInst.inst)
    row.append(currInst.IF)
    row.append(currInst.ID)
    row.append(currInst.IR)
    row.append(currInst.EX)
    row.append(currInst.WB)
    row.append(currInst.RAW)
    row.append(currInst.WAW)
    row.append(currInst.Struct)
    row.append(currInst.iCache)
    row.append("-".join(currInst.dCache))
    res.append(row)

def createICache():
    size = mipsDefs.iCache_Block_Count
    for i in range(size):
        mipsDefs.iCache[i] = []
    for key in mipsDefs.iCache:
        mipsDefs.iCache[key] = [-1 for i in range(size)]

def isInstInICache(pc):
    blockNumber = pc // mipsDefs.iCache_Block_Size

    if blockNumber >= mipsDefs.iCache_Block_Size:
        blockNumber = pc % mipsDefs.iCache_Block_Size

    if pc not in mipsDefs.iCache[blockNumber]:
        log.debug("I-Cache miss for instruction: " + str(pc))
        addToInstCache(pc, blockNumber)
        return False

    return True

def addToInstCache(pc, blockNumber):
    mipsDefs.iCache[blockNumber] = [i for i in range(pc, pc+mipsDefs.iCache_Block_Size)]


# ----------------------------------------------------------------------------
# PIPELINE HELPERS
# ----------------------------------------------------------------------------

def getBaseOffset(operand):
    base = 0
    offset = 0
    if '(' in operand:
        reg = re.search('\(([^)]+)', operand).group(1)
        base = mipsDefs.registers[reg]
    opList = [c for c in operand]
    index = opList.index('(')
    offsetList = "".join(opList[:index])
    offset = int(offsetList)
    return base, offset

def runInstruction(currInst):
    if currInst.opcode == "ADD.D" or currInst.opcode == "DADD":
        src1 = int(mipsDefs.registers[currInst.operand2])
        src2 = int(mipsDefs.registers[currInst.operand3])
        mipsDefs.registers[currInst.operand1] = src1 + src2

    if currInst.opcode == "DADDI":
        src1 = int(mipsDefs.registers[currInst.operand2])
        src2 = int(currInst.operand3)
        mipsDefs.registers[currInst.operand1] = src1 + src2

    if currInst.opcode == "DSUBI":
        src1 = int(mipsDefs.registers[currInst.operand2])
        src2 = int(currInst.operand3)
        mipsDefs.registers[currInst.operand1] = src1 - src2

    if currInst.opcode == "SUB.D" or currInst.opcode == "DSUB":
        src1 = mipsDefs.registers[currInst.operand2]
        src2 = mipsDefs.registers[currInst.operand3]
        mipsDefs.registers[currInst.operand1] = src1 - src2

    if currInst.opcode == "MUL.D":
        src1 = mipsDefs.registers[currInst.operand2]
        src2 = mipsDefs.registers[currInst.operand3]
        mipsDefs.registers[currInst.operand1] = src1 * src2

    if currInst.opcode == "DIV.D":
        src1 = mipsDefs.registers[currInst.operand2]
        src2 = mipsDefs.registers[currInst.operand3]
        mipsDefs.registers[currInst.operand1] = src1 // src2

    if currInst.opcode == "AND":
        src1 = mipsDefs.registers[currInst.operand2]
        src2 = mipsDefs.registers[currInst.operand3]
        mipsDefs.registers[currInst.operand1] = src1 and src2

    if currInst.opcode == "OR":
        src1 = mipsDefs.registers[currInst.operand2]
        src2 = mipsDefs.registers[currInst.operand3]
        mipsDefs.registers[currInst.operand1] = src1 and src2

    if currInst.opcode == "ANDI":
        src1 = int(mipsDefs.registers[currInst.operand2])
        src2 = int(currInst.operand3)
        mipsDefs.registers[currInst.operand1] = src1 and src2

    if currInst.opcode == "ORI":
        src1 = int(mipsDefs.registers[currInst.operand2])
        src2 = int(currInst.operand3)
        mipsDefs.registers[currInst.operand1] = src1 and src2

    if currInst.opcode == "LI" or currInst.opcode == "LUI":
        mipsDefs.registers[currInst.operand1] = int(currInst.operand2)

    if currInst.opcode == "LD" or currInst.opcode == "L.D" or currInst.opcode == "LW":
        base, offset = getBaseOffset(currInst.operand2)
        mipsDefs.registers[currInst.operand1] = base + offset
        log.debug("(Base, Offset): ")
        log.debug("(" + str(base) + ", " + str(offset) + ")")

    if currInst.opcode == "SD" or currInst.opcode == "S.D" or currInst.opcode == "SW":
        base, offset = getBaseOffset(currInst.operand2)
        val = base + offset
        mipsDefs.registers[currInst.operand1] = val
        log.debug("(Base, Offset): ")
        log.debug("(" + str(base) + ", " + str(offset) + ")")

def resolveBranch(currInst, label):
    if label not in mipsDefs.labelMap.keys():
        return
    if currInst.opcode == 'BEQ' and mipsDefs.registers[currInst.operand1] == mipsDefs.registers[currInst.operand2]:
        return mipsDefs.labelMap[label]
    if currInst.opcode == 'BNE' and mipsDefs.registers[currInst.operand1] != mipsDefs.registers[currInst.operand2]:
        return mipsDefs.labelMap[label]


def freeUnits(unitsToFree):
    for inst in unitsToFree:
        freeUnit(inst)
        unitsToFree.remove(inst)

def freeUnit(currInst):
    mipsDefs.units[currInst.unit].availableUnits = mipsDefs.units[currInst.unit].totalUnits
    mipsDefs.units[currInst.unit].availableCycleCounts = mipsDefs.units[currInst.unit].totalCycleCounts
    mipsDefs.units[currInst.unit].instructionsOccupying = []

def freeRegisters(regsToFree, occupiedRegisters):
    for reg in regsToFree:
        occupiedRegisters.pop(reg)
        regsToFree.remove(reg)

def isUnitAvailable(currInst):
    requiredUnit = currInst.unit
    ans = mipsDefs.units[requiredUnit].availableUnits != 0
    logUnitAvailability(currInst, ans)
    return ans

def isWAW(currInst, occupiedRegisters):
    if currInst.type == InstructionType.INV or currInst.type == InstructionType.SPCL or currInst.type == InstructionType.CTRL:
        return False

    ans = False
    destinationReg = currInst.operand1
    if destinationReg in occupiedRegisters.keys():
        ans = True
    return ans

def isRAW(currInst, occupiedRegisters):
    ans = False
    src1 = currInst.operand2
    src2 = currInst.operand3
    if currInst.type == InstructionType.CTRL:
        src1 = currInst.operand1
        src2 = currInst.operand2
    if src1 in occupiedRegisters.keys() or src2 in occupiedRegisters.keys():
        ans = True
    return ans

def occupyUnit(currInst):
    mipsDefs.units[currInst.unit].availableUnits -= 1
    if currInst.id not in mipsDefs.units[currInst.unit].instructionsOccupying:
        mipsDefs.units[currInst.unit].instructionsOccupying.append(currInst.id)
    log.debug("Instruction " + str(currInst.id) + " is occupying unit " + mipsDefs.units[currInst.unit].name)

# ----------------------------------------------------------------------------
# INITIALIZE DATA HELPERS
# ----------------------------------------------------------------------------

def getNumOperands():
    # map of instruction opcode to valid number of operands it can have
    numOperandsMap = {
    'LW':[2], 'SW':[2], 'L.D':[2], 'S.D':[2], 'LD':[2], 'SD':[2], 'LI':[2], 'LUI': [2],
    'DADD':[3], 'DADDI':[3], 'DSUB':[3], 'DSUBI':[3], 'ADD.D':[3], 'SUB.D': [3], 'MUL.D':[3], 'DIV.D':[3],
    'AND':[3], 'ANDI':[3], 'OR':[3], 'ORI':[3],
    'J':[1], 'BEQ':[3], 'BNE': [3], 'HLT':[0]
    }
    return numOperandsMap

def getRegisters():
    registers =  {
        'R0': 0, 'R1': 0, 'R2': 0, 'R3': 0, 'R4': 0, 'R5': 0, 'R6': 0, 'R7': 0,
        'R8': 0, 'R9': 0, 'R10': 0, 'R11': 0, 'R12': 0, 'R13': 0, 'R14': 0, 'R15': 0,
        'R16': 0, 'R17': 0, 'R18': 0, 'R19': 0, 'R20': 0, 'R21': 0, 'R22': 0, 'R23': 0,
        'R24': 0, 'R25': 0, 'R26': 0, 'R27': 0, 'R28': 0, 'R29': 0, 'R30': 0, 'R31': 0,

        'F0': 0, 'F1': 0, 'F2': 0, 'F3': 0, 'F4': 0, 'F5': 0, 'F6': 0, 'F7': 0,
        'F8': 0, 'F9': 0, 'F10': 0, 'F11': 0, 'F12': 0, 'F13': 0, 'F14': 0, 'F15': 0,
        'F16': 0, 'F17': 0, 'F18': 0, 'F19': 0, 'F20': 0, 'F21': 0, 'F22': 0, 'F23': 0,
        'F24': 0, 'F25': 0, 'F26': 0, 'F27': 0, 'F28': 0, 'F29': 0, 'F30': 0, 'F31': 0,
    }
    return registers

# INPUT:  Maps <unit_name: number_of_units> and <unit_name: cycles_for_unit>
# OUTPUT: Map <unit_name: unit object>
def getUnits(numUnits, unitCycles):
    units = {}
    units["ADDER"] = createAdderUnit()
    units["MULTIPLIER"] = createMultiplierUnit()
    units["DIVIDER"] = createDividerUnit()
    units["INTEGER"] = createIntegerUnit()
    units["MEMORY"] = createMemoryUnit()
    units["BRANCH"] = createBranchUnit()
    units["HALT"] = createHaltUnit()

    for key in numUnits:
        units[key].totalUnits = numUnits[key]
        units[key].availableUnits = units[key].totalUnits
        units[key].totalCycleCounts = unitCycles[key]
        units[key].availableCycleCounts = units[key].totalCycleCounts

    for key in units:
        log.debug(units[key])

    return units

# INPUT:  List of strings comprising of opcodes and operands in an instruction
# OUTPUT: Instruction object for the input instruction
def getInstructionObject(instList):
    i = Instruction()
    i.createInstruction(instList)
    return i

# INPUT:  List of strings comprising of unit, num_units, cycles
# OUTPUT: Map of unit:num_units and unit:cycles
def getNumUnitsCycles(configs):
    numUnits = {}
    unitCycles = {}
    configs = [x.lower() for x in configs]

    adder = [s for s in configs if "adder" in s]
    if adder:
        addData = adder[0].split(":")
        addData = addData[1].split(",")
        numUnits["ADDER"] = int(addData[0])
        unitCycles["ADDER"] = int(addData[1])

    multiplier = [s for s in configs if "multiplier" in s]
    if multiplier:
        mulData = multiplier[0].split(":")
        mulData = mulData[1].split(",")
        numUnits["MULTIPLIER"] = int(mulData[0])
        unitCycles["MULTIPLIER"] = int(mulData[1])

    divider = [s for s in configs if "divider" in s]
    if divider:
        divData = divider[0].split(":")
        divData = divData[1].split(",")
        numUnits["DIVIDER"] = int(divData[0])
        unitCycles["DIVIDER"] = int(divData[1])

    return numUnits, unitCycles


def getICacheConfigs(icache):
    icacheTemp = icache.split(",")
    iBlocks = icacheTemp[0].split(":")[1]
    iBlockSize = icacheTemp[1]
    log.debug("I-Cache number of blocks: " + str(iBlocks))
    log.debug("I-Cache block size      : " + str(iBlockSize))
    return iBlocks, iBlockSize

# ----------------------------------------------------------------------------
# ERROR HANDLING HELPERS
# ----------------------------------------------------------------------------

# INPUT:  List of strings comprising of opcodes and operands in an instruction
# OUTPUT: True/False
def isInstructionValid(instList):
    instList = [x.upper() for x in instList]
    tempInst = instList
    if instList[0].endswith(":"):
        tempInst = tempInst[1:]

    if not isOpcodeValid(tempInst[0]):
        log.error("Invalid Opcode for Instruction " + " ".join(instList))
        raise Exception("Invalid Opcode for Instruction " + " ".join(instList))

    if not isNumberOfOperandsValid(tempInst):
        log.error("Invalid number of operands for Instruction " + " ".join(instList))
        raise Exception("Invalid number of operands for Instruction " + " ".join(instList))

    if not areOperandsValid(tempInst[0], tempInst[1:]):
        log.error("Invalid operands for Instruction " + " ".join(instList))
        raise Exception("Invalid number of operands for Instruction " + " ".join(instList))

    return True

# INPUT:  Opcode strings
# OUTPUT: True/False if opcodes is valid
def isOpcodeValid(sOpcode):
    return sOpcode in getNumOperands().keys()

def isImmediateValue(op):
    try:
        if '(' in op:
            reg = re.search('\(([^)]+)', op).group(1)
            return reg in getRegisters()
        else:
            op = int(op)
        return True
    except:
        return False

# INPUT:  List of Operand strings
# OUTPUT: True/False if operand is valid
def areOperandsValid(opCode, operandList):
    ans = True
    if opCode in ['BNE', 'BE', 'J', 'HLT']:
        return True

    for op in operandList:
        if op in getRegisters().keys() or isImmediateValue(op):
            ans = ans and True
        else:
            ans = False
    return ans

# INPUT:  List of strings comprising of opcodes and operands in an instruction
# OUTPUT: True/False if operands are valid
def isNumberOfOperandsValid(instList):
    return len(instList[1:]) in getNumOperands()[instList[0]]

