import logging

log = logging.getLogger("MIPS Simulator")

def logUnitAvailability(instruction, ans):
    if ans:
        log.debug("Unit " + instruction.unit + " is available for instruction " + str(instruction.id))
    else:
        log.debug("Unit " + instruction.unit + " is not available for instruction " + str(instruction.id))
