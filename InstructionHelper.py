import logging
from Instruction import Instruction
from Instruction import InstructionType
from Instruction import InstructionUnit

log = logging.getLogger("instructionHelper.py")

# map of instruction opcode to valid number of operands it can have
numOperandsMap = {
    'LW': [2],
    'SW': [2],
    'L.D': [2],
    'S.D': [2],
    'LD': [2],
    'SD': [2],
    'LI': [2],
    'LUI': [2],
    'DADD': [3],
    'DADDI': [3],
    'DSUB': [3],
    'DSUBI': [3],
    'ADD.D': [3],
    'MUL.D': [3],
    'DIV.D': [3],
    'SUB.D': [3],
    'AND': [3],
    'ANDI': [3],
    'OR': [3],
    'ORI': [3],
    'J': [1],
    'BEQ': [3],
    'BNE': [3],
    'HLT': [0]
}

# INPUT:  List of strings comprising of opcodes and operands in an instruction
# OUTPUT: Instruction object for the input instruction
def getInstruction(instList):
    i = Instruction()
    i.createInstruction(instList)
    return i

def isOpcodeValid(sOpcode):
    return sOpcode in numOperandsMap.keys()

def isNumberOfOperandsValid(instList):
    return len(instList[1:]) in numOperandsMap[instList[0]]

# INPUT:  List of strings comprising of opcodes and operands in an instruction
# OUTPUT: True/False
def isInstructionValid(instList):
    tempInst = instList
    print(instList)
    if instList[0].endswith(":"):
        tempInst = tempInst[1:]
    if not isOpcodeValid(tempInst[0]):
        log.error("Invalid Opcode for Instruction " + " ".join(instList))
        raise Exception("Invalid Opcode for Instruction " + " ".join(instList))
    if not isNumberOfOperandsValid(tempInst):
        log.error("Invalid number of operands for Instruction " + " ".join(instList))
        raise Exception("Invalid number of operands for Instruction " + " ".join(instList))
    return True

# INPUT:  String containing 1 instruction (eg. LW
# OUTPUT: Instruction object (calling object) initialized
def getInstructionAsList(sInstruction):
    sInstruction = sInstruction.replace(',','')
    sInstruction = sInstruction.replace('\t','')
    instParts =  sInstruction.split(" ")
    return instParts

def printInstruction(I):
    log.debug("Opcode: " + I.opcode)
    log.debug("Operand 1: " + I.operand1)
    log.debug("Operand 2: " + I.operand2)
    log.debug("Operand 3: " + I.operand3)
    log.debug("label: " + I.label)
    log.debug("id: " + str(I.id))
    if I.hasLabel:
        log.debug("hasLabel: True")
    else:
        log.debug("hasLabel: False")
    if I.type == InstructionType.INV:
        log.debug("type: INV")
    if I.type == InstructionType.MEM:
        log.debug("type: MEM")
    if I.type == InstructionType.ALU:
        log.debug("type: ALU")
    if I.type == InstructionType.CTRL:
        log.debug("type: CTRL")
    if I.type == InstructionType.SPCL:
        log.debug("type: SPCL")

    if I.unit == InstructionUnit.INV:
        log.debug("unit: INV")
    if I.unit == InstructionUnit.INT:
        log.debug("unit: INT")
    if I.unit == InstructionUnit.ADD:
        log.debug("unit: ADD")
    if I.unit == InstructionUnit.MUL:
        log.debug("unit: MUL")
    if I.unit == InstructionUnit.DIV:
        log.debug("unit: DIV")
    if I.unit == InstructionUnit.NON:
        log.debug("unit: NON")




