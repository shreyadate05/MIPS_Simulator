class Unit:
    def __init__(self):
        self.name = ""
        self.totalUnits = 0
        self.availableUnits = 0
        self.totalCycleCounts = 0
        self.availableCycleCounts = 0
        self.instructionsOccupying = []

def createAdderUnit():
    adder = Unit()
    adder.name = "ADDER"
    adder.totalUnits = 0
    adder.availableUnits = adder.totalUnits
    adder.totalCycleCounts = 0
    adder.availableCycleCounts = adder.totalCycleCounts
    adder.instructionsOccupying = []
    return adder

def createMultiplierUnit():
    multiplier = Unit()
    multiplier.name = "MULTIPLIER"
    multiplier.totalUnits = multiplier.totalUnits
    multiplier.availableUnits = 0
    multiplier.totalCycleCounts = 0
    multiplier.availableCycleCounts = multiplier.totalCycleCounts
    multiplier.instructionsOccupying = []
    return multiplier

def createDividerUnit():
    divider = Unit()
    divider.name = "DIVIDER"
    divider.totalUnits = 0
    divider.availableUnits = divider.totalUnits
    divider.totalCycleCounts = 0
    divider.availableCycleCounts = divider.totalCycleCounts
    divider.instructionsOccupying = []
    return divider

def createIntegerUnit():
    integer = Unit()
    integer.name = "INTEGER"
    integer.totalUnits = 1
    integer.availableUnits = integer.totalUnits
    integer.totalCycleCounts = 1
    integer.availableCycleCounts = integer.totalCycleCounts
    integer.instructionsOccupying = []
    return integer

def createMemoryUnit():
    memory = Unit()
    memory.name = "MEMORY"
    memory.totalUnits = 1
    memory.availableUnits = memory.totalUnits
    memory.totalCycleCounts = 2
    memory.availableCycleCounts = memory.totalCycleCounts
    memory.instructionsOccupying = []
    return memory

def createBranchUnit():
    branch = Unit()
    branch.name = "BRANCH"
    branch.totalUnits = 1
    branch.availableUnits = branch.totalUnits
    branch.totalCycleCounts = 0
    branch.availableCycleCounts = branch.totalCycleCounts
    branch.instructionsOccupying = []
    return branch