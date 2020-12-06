import logging

log = logging.getLogger("MIPS Simulator")

def logIsStalled(isStalled):
    if not isStalled:
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
