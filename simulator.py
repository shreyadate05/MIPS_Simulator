import sys
from InstructionHelper import parseInstruction
from utils import parseFile

instFile = ""
dataFile = ""
confFile = ""
ansFile = ""

def parseInstFile(instFile):
    instructions = parseFile(instFile)
    print(instructions)

def parseDataFile(dataFile):
    data = parseFile(dataFile)
    print(data)

def parseConfFile(confFile):
    configs = parseFile(confFile)
    print(configs)

def init(argv):
    global instFile, dataFile, confFile, ansFile
    instFile = argv[1]
    dataFile = argv[2]
    confFile = argv[3]
    ansFile = argv[4]
    parseInstFile(instFile)
    parseDataFile(dataFile)
    parseConfFile(confFile)

def startSimulator(argv):
    try:
        init(argv)

    except:
        print("Something went wrong. Exiting")
        return -1