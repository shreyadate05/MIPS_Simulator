import logging

log = logging.getLogger("instructionHelper.py")

# map of instruction opcode to valid number of operands it can have
instructionMap = {
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

def isOpcodeValid(sOpcode):
    return sOpcode in instructionMap.keys()

def isNumberOfOperandsValid(instList):
    return len(instList[1:]) in instructionMap[instList[0]]

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


