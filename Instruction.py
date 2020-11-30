import enum

id = 0

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
        self.label    = ""
        self.type     = InstructionType.INV
        self.id       = 0

    def createInstruction(self, instList):
        global id
        if instList[0].endswith(":"):
            self.hasLabel = True
            self.label = instList[0]
            instList = instList[1:]
        self.opcode = instList[0]
        self.operand1 = instList[1]
        self.operand2 = instList[2]
        if len(instList) == 4:
            self.operand3 = instList[3]

        id += 1
        self.id = id
