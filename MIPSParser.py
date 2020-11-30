import sys
from InstructionHelper import getInstructionAsList
from InstructionHelper import isInstructionValid
from utils import parseFile

# INPUT:  List of strings comprising of opcodes and operands in an instruction
# OUTPUT: Instruction object formed from given input Instruction List
def parseInstruction(inst):
    instList = getInstructionAsList(inst)
    if not isInstructionValid(instList):
        raise Exception("Invalid Instruction " + inst)

# INPUT:  file containing all instructions
# OUTPUT: List of Instruction object formed from given input Instruction List
def parseInstFile(instFile):
    instFileList = parseFile(instFile)
    instructions = []
    for inst in instFileList:
        inst = parseInstruction(inst)
        instructions.append(inst)
    return instructions

# INPUT:  file containing all input data
# OUTPUT: List of words in data
def parseDataFile(dataFile):
    data = parseFile(dataFile)
    return data

def parseConfFile(confFile):
    configs = parseFile(confFile)
    return configs
