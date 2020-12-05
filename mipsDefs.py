ansFile = ""
registers = {}
numOperands = {}
data = []
instructions = {} # id: <Instruction Object>
units = {}        # unit_name: <Unit Object>
labelMap = {}     # label: id of instruction at which label exists
numUnits = {}     # InstructionUnit : number of units present
unitCycles = {}   # InstructionUnit : latency in cycles for each unit

