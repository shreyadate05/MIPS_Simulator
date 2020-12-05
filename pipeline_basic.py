from mipsHelper import *

log = logging.getLogger("MIPS Pipeline")

fetchQueue = []
issueQueue = []
readQueue = []
execQueue = []
writeQueue = []

clockCount = 1
programCounter = 0
isStalled = False
done = False

def fetch():
    global instructions, units, registers
    global fetchQueue, issueQueue, readQueue, execQueue, writeQueue
    global clockCount, isStalled, done
    log.debug("[ " + str(clockCount) + " ] FETCH")


def issue():
    global instructions, units, registers
    global fetchQueue, issueQueue, readQueue, execQueue, writeQueue
    global clockCount, isStalled, done
    log.debug("[ " + str(clockCount) + " ] ISSUE")


def read():
    global instructions, units, registers
    global fetchQueue, issueQueue, readQueue, execQueue, writeQueue
    global clockCount, isStalled, done
    log.debug("[ " + str(clockCount) + " ] READ")


def execute():
    global instructions, units, registers
    global fetchQueue, issueQueue, readQueue, execQueue, writeQueue
    global clockCount, isStalled, done
    log.debug("[ " + str(clockCount) + " ] EXECUTE")


def write():
    global instructions, units, registers
    global fetchQueue, issueQueue, readQueue, execQueue, writeQueue
    global clockCount, isStalled, done, programCounter
    log.debug("[ " + str(clockCount) + " ] WRITE")

    programCounter += 1

def start():
    global instructions, units, registers
    global fetchQueue, issueQueue, readQueue, execQueue, writeQueue
    global clockCount, isStalled, done
    res = []

    log.debug("\n")
    log.debug("Starting Pipeline...\n\n")

    while not done:
        fetch()
        issue()
        read()
        execute()
        write()

        clockCount += 1
        log.debug("\n------------------------------------------\n")

    return res
