from mipsParser import *
from pipeline_basic import *
from pipeline import *
from mipsHelper import *
import mipsDefs

log = logging.getLogger("MIPS Simulator")

def triggerPipeline():
    mipsDefs.resultMatrix = start()
    log.debug(mipsDefs.resultMatrix)

def initMIPS(argv):
    mipsDefs.ansFile = argv[4]
    mipsDefs.registers = getRegisters()
    mipsDefs.numOperands = getNumOperands()
    mipsDefs.instructions, mipsDefs.labelMap = parseInstFile(argv[1])
    mipsDefs.data = parseDataFile(argv[2])
    mipsDefs.units, mipsDefs.iBlocks, mipsDefs.iBlockSize = parseConfFile(argv[3])

def startSimulator(argv):
    try:
        log.info("Starting simulator...")
        initMIPS(argv)
        triggerPipeline()
        #startMIPS()
    except Exception as e:
        log.error("Something went wrong. \n", e)