import logging
from MIPSParser import parseInstFile
from MIPSParser import parseDataFile
from MIPSParser import parseConfFile

log = logging.getLogger("simulator.py")
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
        log.info("Starting simulator...")
        initMIPS(argv)
    except Exception as e:
        log.error("Something went wrong. \n", e)