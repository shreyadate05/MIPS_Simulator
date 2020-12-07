ansFile = ""
registers = {}    # reg: value
numOperands = {}  # opcode: num_of_operands
data = []
instructions = {} # id: <Instruction Object>
units = {}        # unit_name: <Unit Object>
labelMap = {}     # label: id of instruction at which label exists
resultMatrix = []
programCounter = 1

mainMemoryAccessTime = 12

iCache_Block_Size = 0
iCache_Block_Count = 0
iCache = {}
iCachePenalty = mainMemoryAccessTime