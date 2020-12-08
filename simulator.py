from mipsParser import *
from pipeline import *
from mipsHelper import *
import mipsDefs

log = logging.getLogger("MIPS Simulator")

def writeFile(res):
    text_file = open(mipsDefs.ansFile, "w")
    text_file.write(res)
    text_file.write("\nTotal number of I-Cache hits: " + str(mipsDefs.iCacheHits))
    text_file.write("\nTotal number of I-Cache misses: " + str(mipsDefs.iCacheMisses))
    text_file.close()

def initMemory():
    createICache()
    createDCache()

def initMIPS(argv):
    mipsDefs.ansFile = argv[4]
    mipsDefs.registers = getRegisters()
    mipsDefs.numOperands = getNumOperands()
    mipsDefs.instructions, mipsDefs.labelMap = parseInstFile(argv[1])
    mipsDefs.data = parseDataFile(argv[2])
    mipsDefs.units, mipsDefs.iCache_Block_Count, mipsDefs.iCache_Block_Size = parseConfFile(argv[3])

def startSimulator(argv):
    try:
        log.info("Starting simulator...")
        initMIPS(argv)
        initMemory()
        resultString = startMIPS()
        writeFile(resultString)
        print(resultString)
    except Exception as e:
        log.error("Something went wrong. \n", e)