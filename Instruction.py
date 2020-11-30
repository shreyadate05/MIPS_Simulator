import enum

class InstructionType(enum.Enum):
    INV  = 0
    MEM  = 1
    ALU  = 2
    CTRL = 3
    SPCL = 4

class Instruction:
    def __init__(self):
        self.opcode   = None
        self.operand1 = None
        self.operand2 = None
        self.operand3 = None
        self.hasLabel = False
        self.type     = InstructionType.INV
