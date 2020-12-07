from mipsHelper import *
from instruction import *
from scoreboard import *
import logging
import mipsDefs

log = logging.getLogger("MIPS Pipeline ")

allQueue   = []
fetchQueue = []
issueQueue = []
readQueue = []
execQueue = []
writeQueue = []

clockCount = 1
programCounter = 1
isStalled = False
done = False

def startMIPS():
    global clockCount, done, programCounter, allQueue
    global fetchQueue, issueQueue, readQueue, execQueue, writeQueue

    res = []
    log.debug("Starting MIPS Processor\n\n")

    allQueue = [i for i in range(1,len(mipsDefs.instructions)+1)]
    while not done:
        log.debug("Clock Cycle: " + str(clockCount))
        write()
        execute()
        read()
        issue()
        fetch()

        if len(allQueue) == 0:
            done = True

        clockCount += 1
        log.debug("\n")

    return res
