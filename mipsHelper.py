import mipsDefs
import re
from instruction import *
from unit import *
from logHelper import *

log = logging.getLogger("MIPS Helper   ")

# ----------------------------------------------------------------------------
# PIPELINE HELPERS
# ----------------------------------------------------------------------------
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

