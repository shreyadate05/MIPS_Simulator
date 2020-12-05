from mipsParser import *
from mipsHelper import *
from pipeline_basic import *
from mipsDefs import *

log = logging.getLogger("MIPS Simulator")

def triggerPipeline():
    global resultMatrix
    resultMatrix = start()
    log.debug(resultMatrix)

def initMIPS(argv):
    global ansFile, registers, numOperands,  data, instructions, labelMap, units
    global iBlockSize, iBlocks
    ansFile = argv[4]
    registers = getRegisters()
    numOperands = getNumOperands()
    instructions, labelMap = parseInstFile(argv[1])
    data = parseDataFile(argv[2])
    units, iBlocks, iBlockSize = parseConfFile(argv[3])

def startSimulator(argv):
    try:
        log.info("Starting simulator...")
        initMIPS(argv)
        triggerPipeline()
    except Exception as e:
        log.error("Something went wrong. \n", e)