import logging
from mipsHelper import *
from logHelper import *
from utils import *

log = logging.getLogger("MIPS Parser")

# INPUT:  file containing all input data
# OUTPUT: List of words in data
def parseDataFile(dataFile):
    data = parseFile(dataFile)
    return data

# INPUT:  List of strings comprising of unit, num_units, cycles
# OUTPUT: Map of unit:num_units and unit:cycles
def getNumUnitsCycles(configs):
    numUnits = {}
    unitCycles = {}
    configs = [x.lower() for x in configs]

    adder = [s for s in configs if "adder" in s]
    if adder:
        addData = adder[0].split(":")
        addData = addData[1].split(",")
        numUnits[InstructionUnit.ADD] = int(addData[0])
        unitCycles[InstructionUnit.ADD] = int(addData[1])

    multiplier = [s for s in configs if "multiplier" in s]
    if multiplier:
        mulData = multiplier[0].split(":")
        mulData = mulData[1].split(",")
        numUnits[InstructionUnit.MUL] = int(mulData[0])
        unitCycles[InstructionUnit.MUL] = int(mulData[1])

    divider = [s for s in configs if "divider" in s]
    if divider:
        divData = divider[0].split(":")
        divData = divData[1].split(",")
        numUnits[InstructionUnit.DIV] = int(divData[0])
        unitCycles[InstructionUnit.DIV] = int(divData[1])

    return numUnits, unitCycles

# INPUT:  file containing all configs for functional units
# OUTPUT: Map of of Instruction Unit to number of units available
# OUTPUT: Map of of Instruction Unit to latency in cycles for each unit
def parseConfFile(confFile):
    configs = parseFile(confFile)
    numUnits, unitCycles = getNumUnitsCycles(configs)
    log.debug("Map of <unit: number of units available> is: ")
    log.debug(numUnits)
    log.debug("Map of <unit: latency in number of cycles> is: ")
    log.debug(unitCycles)
    return numUnits, unitCycles

# INPUT:  List of strings comprising of opcodes and operands in an instruction
# OUTPUT: Instruction object formed from given input Instruction List
def parseInstruction(inst):
    instList = inst.split()
    instList = [str.replace(',', '') for str in instList]
    if not isInstructionValid(instList):
        log.error("Invalid Instruction " + inst)
        raise Exception("Invalid Instruction " + inst)
    return getInstructionObject(instList)

# INPUT:  file containing all instructions
# OUTPUT: Map of of Instruction ID to Instruction Data object formed from given input Instruction List
# OUTPUT: Map of of Instruction Label to Instruction Id
def parseInstFile(instFile):
    instFileList = parseFile(instFile)
    instructions = { }
    labelMap = {}

    for inst in instFileList:
        strInst = inst
        log.info("Parsing instruction " + strInst)
        inst = parseInstruction(inst)
        instructions[inst.id] = inst
        if inst.hasLabel:
            labelMap[inst.label] = inst.id

        if inst.type == InstructionType.CTRL and inst.operand3 not in labelMap.keys():
            log.error("Invalid label in instruction " + strInst)
            raise Exception("Invalid label in instruction " + strInst)

    logInstructionsMap(instructions)
    logLabelMap(labelMap)
    return instructions,labelMap
