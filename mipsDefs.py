ansFile = ""
registers = {}    # reg: value
numOperands = {}  # opcode: num_of_operands
data = []
instructions = {} # id: <Instruction Object>
units = {}        # unit_name: <Unit Object>
labelMap = {}     # label: id of instruction at which label exists
resultMatrix = []
resultString = ""
programCounter = 1

mainMemoryAccessTime = 12

iCache_Block_Size = 0
iCache_Block_Count = 0
iCache = {}
iCachePenalty = mainMemoryAccessTime

iCacheMisses = 0
iCacheHits = 0
iCacheAccesses = 0
iCacheCheckQueue = []
iCacheHitsQueue = []
iCacheIndex = 0

dCache = {}
dCacheAccesses = 0
dCacheHits = 0

stop = False