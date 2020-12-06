import logging

log = logging.getLogger("MIPS Simulator")

def logUnitAvailability(instruction, ans):
    if not ans:
        log.debug("Unit " + instruction.unit + " is not available for instruction " + str(instruction.id))
