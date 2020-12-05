from mipsParser import *
from mipsHelper import *
from pipeline import *
from mipsDefs import *

log = logging.getLogger("MIPS Simulator")

def initMIPS(argv):
    global ansFile, data, instructions, labelMap, numUnits, unitCycles, registers, numOperands
    ansFile = argv[4]
    registers = getRegisters()
    numOperands = getNumOperands()
    instructions, labelMap = parseInstFile(argv[1])
    data = parseDataFile(argv[2])
    units = parseConfFile(argv[3])

def startSimulator(argv):
    try:
        log.info("Starting simulator...")
        initMIPS(argv)
        triggerPipeline()
    except Exception as e:
        log.error("Something went wrong. \n", e)