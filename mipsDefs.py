ansFile = ""
registers = {}    # reg: value
numOperands = {}  # opcode: num_of_operands
data = []
instructions = {} # id: <Instruction Object>
units = {}        # unit_name: <Unit Object>
labelMap = {}     # label: id of instruction at which label exists
resultMatrix = []
iBlockSize = 0
iBlocks = 0

programCounter = 1