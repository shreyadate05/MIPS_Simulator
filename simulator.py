import sys
from InstructionHelper import parseInstruction
from utils import parseFile

ansFile = ""
data = []

def parseInstFile(instFile):
    instructions = parseFile(instFile)
    for inst in instructions:
        inst = parseInstruction(inst)
    print(instructions)

def parseDataFile(dataFile):
    global data
    data = parseFile(dataFile)

def parseConfFile(confFile):
    configs = parseFile(confFile)
    print(configs)

def init(argv):
    global ansFile
    ansFile = argv[4]
    parseInstFile(argv[1])
    parseDataFile(argv[2])
    parseConfFile(argv[3])

def startSimulator(argv):
    try:
        init(argv)
    except:
        print("Something went wrong. Exiting")
        return -1