import logging

log = logging.getLogger("MIPS Simulator")

def logPrevAndCurrStall(prevStallVal, currStallVal):
    if prevStallVal:
        log.debug("Previous Stall: True")
    else:
        log.debug("Previous Stall: False")

    if currStallVal:
        log.debug("Current Stall: True")
    else:
        log.debug("Curren Stall: False")

def logIsStalled(isStalled):
    if isStalled:
        log.debug("Pipeline is stalled")
    else:
        log.debug("Pipeline is not stalled")

def logQueue(q):
    if len(q) == 0:
        return
    s = []
    for i in q:
        s.append(str(i.id))
    log.debug(", ".join(s))

def logUnitAvailability(instruction, ans):
    if not ans:
        log.debug("Unit " + instruction.unit + " is not available for instruction " + str(instruction.id))
