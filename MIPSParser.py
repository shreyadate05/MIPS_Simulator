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

# INPUT:  file containing all configs for functional units
# OUTPUT: Map of of Instruction Unit to number of units available
# OUTPUT: Map of of Instruction Unit to latency in cycles for each unit
def parseConfFile(confFile):
    configs = parseFile(confFile)
    numUnits, unitCycles = getNumUnitsCycles(configs)
    units  = getUnits(numUnits, unitCycles)
    iBlocks, iBlockSize = getICacheConfigs(configs[len(configs)-1])
    return units, iBlocks, iBlockSize

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
        log.debug("Parsing instruction " + strInst)
        inst = parseInstruction(inst)
        printInstruction(inst)
        log.debug("\n")
        instructions[inst.id] = inst
        if inst.hasLabel:
            labelMap[inst.label] = inst.id

        if inst.type == InstructionType.CTRL and inst.operand3 not in labelMap.keys():
            log.error("Invalid label in instruction " + strInst)
            raise Exception("Invalid label in instruction " + strInst)

    log.debug("Total Number of instructions: " + str(len(instructions)) + "\n")

    logLabelMap(labelMap)
    log.debug("Total Number of labels: " + str(len(labelMap)) + "\n")

    return instructions,labelMap
