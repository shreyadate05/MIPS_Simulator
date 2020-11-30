import sys
from MIPSParser import parseInstFile
from MIPSParser import parseDataFile
from MIPSParser import parseConfFile

ansFile = ""
data = []
instructions = []

def initMIPS(argv):
    global ansFile
    ansFile = argv[4]
    instructions = parseInstFile(argv[1])
    data = parseDataFile(argv[2])
    configs = parseConfFile(argv[3])

def startSimulator(argv):
    try:
        initMIPS(argv)
    except Exception as e:
        print("Something went wrong. \n", e)