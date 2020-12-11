from mipsParser import *
from pipeline import *
from mipsHelper import *
import mipsDefs

log = logging.getLogger("MIPS Simulator")

def writeFile():
    text_file = open(mipsDefs.ansFile, "w")
    text_file.write(mipsDefs.resultString)
    text_file.write("\nTotal number of I-Cache accesses: " + str(mipsDefs.iCacheAccesses))
    text_file.write("\nTotal number of I-Cache hits    : " + str(mipsDefs.iCacheAccesses - mipsDefs.iCacheMisses))
    text_file.write("\nTotal number of D-Cache accesses: " + str(mipsDefs.dCacheAccesses*2))
    text_file.write("\nTotal number of D-Cache hits    : " + str(mipsDefs.dCacheHits+1))
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
    mipsDefs.mainMemoryAccessTime = 3*mipsDefs.iCache_Block_Size
    mipsDefs.iCachePenalty = mipsDefs.mainMemoryAccessTime

def startSimulator(argv):
    try:
        log.info("Starting simulator...")
        initMIPS(argv)
        initMemory()
        startMIPS()
        writeFile()
    except Exception as e:
        log.error("Something went wrong. \n", e)