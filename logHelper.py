import logging
from instruction import *

log = logging.getLogger("MIPS Simulator")

def logInstructionsMap(instructions):
    for k, v in instructions.items():
        log.debug(str(k) + ":")
        printInstruction(v)

def logLabelMap(labelMap):
    log.debug("Label map <label: instruction id> is: ")
    log.debug(labelMap)

def printUnit(units):
    log.debug("\nMap of <unit_name: unit_object> is: \n")
    for key in units:
        log.debug(key + ":")
        unit = units[key]
        log.debug("name: " + unit.name)
        log.debug("totalUnits: " + str(unit.totalUnits))
        log.debug("availableUnits: " + str(unit.availableUnits))
        log.debug("totalCycleCounts: " + str(unit.totalCycleCounts))
        log.debug("availableCycleCounts: " + str(unit.availableCycleCounts))
        log.debug("instructionsOccupying: " + " ".join(unit.instructionsOccupying))
        log.debug("\n")

def printInstruction(I):
    log.debug("id: " + str(I.id))
    log.debug("Opcode: " + I.opcode)
    log.debug("Operand 1: " + I.operand1)
    log.debug("Operand 2: " + I.operand2)
    log.debug("Operand 3: " + I.operand3)
    log.debug("label: " + I.label)
    log.debug("unit: " + I.unit)

    if I.isComplete:
        log.debug("isComplete: True")
    else:
        log.debug("isComplete: False")

    if I.hasLabel:
        log.debug("hasLabel: True")
    else:
        log.debug("hasLabel: False")

    if I.type == InstructionType.INV:
        log.debug("type: INV")
    if I.type == InstructionType.MEM:
        log.debug("type: MEM")
    if I.type == InstructionType.ALU:
        log.debug("type: ALU")
    if I.type == InstructionType.CTRL:
        log.debug("type: CTRL")
    if I.type == InstructionType.SPCL:
        log.debug("type: SPCL")

    if I.pipeStage == PipeStage.INIT:
        log.debug("pipeStage: INIT")
    if I.pipeStage == PipeStage.FETCH:
        log.debug("pipeStage: FETCH")
    if I.pipeStage == PipeStage.ISSUE:
        log.debug("pipeStage: ISSUE")
    if I.pipeStage == PipeStage.READ:
        log.debug("pipeStage: READ")
    if I.pipeStage == PipeStage.EXEC:
        log.debug("pipeStage: EXEC")
    if I.pipeStage == PipeStage.WRITE:
        log.debug("pipeStage: WRITE")





