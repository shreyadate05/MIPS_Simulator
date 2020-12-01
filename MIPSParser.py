import logging
from Instruction import InstructionUnit
from InstructionHelper import isInstructionValid
from InstructionHelper import getInstructionObject
from InstructionHelper import printInstruction
from utils import parseFile

log = logging.getLogger("mipsParser.py")

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
        print(addData)
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

# INPUT:  List of strings comprising of opcodes and operands in an instruction
# OUTPUT: Instruction object formed from given input Instruction List
def parseInstruction(inst):
    instList = inst.split()
    if not isInstructionValid(instList):
        log.error("Invalid Instruction " + inst)
        raise Exception("Invalid Instruction " + inst)
    return getInstructionObject(instList)

def logInstructionsMap(instructions):
    for k, v in instructions.items():
        log.debug(str(k) + ":")
        printInstruction(v)

def logLabelMap(labelMap):
    for k, v in labelMap.items():
        log.debug(k + ":" + str(v))

# INPUT:  file containing all instructions
# OUTPUT: Map of of Instruction ID to Instruction Data object formed from given input Instruction List
# OUTPUT: Map of of Instruction Label to Instruction Id
def parseInstFile(instFile):
    instFileList = parseFile(instFile)
    instructions = { }
    labelMap = {}

    for inst in instFileList:
        log.info("Parsing instruction " + inst)
        inst = parseInstruction(inst)
        instructions[inst.id] = inst
        if inst.hasLabel:
            labelMap[inst.label] = inst.id

    logInstructionsMap(instructions)
    logLabelMap(labelMap)

    return instructions,labelMap

# INPUT:  file containing all input data
# OUTPUT: List of words in data
def parseDataFile(dataFile):
    data = parseFile(dataFile)
    return data

def parseConfFile(confFile):
    configs = parseFile(confFile)
    numUnits, unitCycles = getNumUnitsCycles(configs)
    print(numUnits)
    print(unitCycles)
    return numUnits, unitCycles
