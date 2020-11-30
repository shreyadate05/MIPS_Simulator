import sys
from InstructionHelper import parseInstruction
from utils import parseFile

def parseInstruction(inst):
    pass

def parseInstFile(instFile):
    instList = parseFile(instFile)
    instructions = []
    for inst in instList:
        inst = parseInstruction(inst)
        instructions.append(inst)
    return instructions

def parseDataFile(dataFile):
    data = parseFile(dataFile)
    return data

def parseConfFile(confFile):
    configs = parseFile(confFile)
    return configs
