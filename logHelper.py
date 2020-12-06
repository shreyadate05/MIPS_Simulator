import logging

log = logging.getLogger("MIPS Simulator")

def logUnitAvailability(instruction, ans):
    if ans:
        log.debug("[Instruction " + str(instruction.id) + "] Unit " + instruction.unit + " is available." )
    else:
        log.debug("[Instruction " + str(instruction.id) + "] Unit " + instruction.unit + " is not available.")