import logging
from instruction import *

log = logging.getLogger("MIPS Simulator")

def logInstructionsMap(instructions):
    for k, v in instructions.items():
        log.debug(str(k) + ":")
        printInstruction(v)

def logLabelMap(labelMap):
    log.debug("Label map <label: instruction id> is: ")
    for k, v in labelMap.items():
        log.debug(k + ":" + str(v))

def printInstruction(I):
    log.debug("Opcode: " + I.opcode)
    log.debug("Operand 1: " + I.operand1)
    log.debug("Operand 2: " + I.operand2)
    log.debug("Operand 3: " + I.operand3)
    log.debug("label: " + I.label)
    log.debug("id: " + str(I.id))
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

    if I.unit == InstructionUnit.INV:
        log.debug("unit: INV")
    if I.unit == InstructionUnit.INT:
        log.debug("unit: INT")
    if I.unit == InstructionUnit.ADD:
        log.debug("unit: ADD")
    if I.unit == InstructionUnit.MUL:
        log.debug("unit: MUL")
    if I.unit == InstructionUnit.DIV:
        log.debug("unit: DIV")
    if I.unit == InstructionUnit.NON:
        log.debug("unit: NON")




