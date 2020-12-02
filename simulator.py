import logging
from mipsParser import *
from mipsHelper import *

log = logging.getLogger("MIPS Simulator")
ansFile = ""
registers = getRegisters()
numOperands = getNumOperands()
data = []
instructions = {} # id: <Instruction Object>
labelMap = {}     # label: id of instruction at which label exists
numUnits = {}     # InstructionUnit : number of units present
unitCycles = {}   # InstructionUnit : latency in cycles for each unit


def initMIPS(argv):
    global ansFile, data, instructions, labelMap, numUnits, unitCycles
    ansFile = argv[4]
    instructions, labelMap = parseInstFile(argv[1])
    data = parseDataFile(argv[2])
    numUnits, unitCycles = parseConfFile(argv[3])

def startSimulator(argv):
    try:
        log.info("Starting simulator...")
        initMIPS(argv)
    except Exception as e:
        log.error("Something went wrong. \n", e)