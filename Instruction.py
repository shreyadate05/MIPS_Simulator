import enum

id = 0

class InstructionType(enum.Enum):
    INV  = 0
    MEM  = 1
    ALU  = 2
    CTRL  = 3
    SPCL  = 4

class Instruction:
    def __init__(self):
        self.opcode   = ""
        self.operand1 = ""
        self.operand2 = ""
        self.operand3 = ""
        self.hasLabel = False
        self.label    = ""
        self.type     = InstructionType.INV
        self.id       = 0

    def assignInstType(self):
        mem = ['LW','SW','L.D','S.D','LD','SD','LI','LUI']
        alu = ['ADD.D','SUB.D','AND','OR', 'DADDI','DSUBI', 'ANDI','ORI']
        ctrl = ['J', 'BEQ', 'BNE']
        spcl = ['HLT']
        if self.opcode in mem:
            self.type = InstructionType.MEM
        if self.opcode in alu:
            self.type = InstructionType.ALU
        if self.opcode in ctrl:
            self.type = InstructionType.CTRL
        if self.opcode in spcl:
            self.type = InstructionType.SPCL

    def createInstruction(self, instList):
        global id
        id += 1
        self.id = id
        if instList[0].endswith(":"):
            self.hasLabel = True
            self.label = instList[0][:-1]
            instList = instList[1:]
        self.opcode = instList[0]
        if len(instList) > 1:
            self.operand1 = instList[1]
        if len(instList) > 2:
            self.operand2 = instList[2]
        if len(instList) > 3:
            self.operand3 = instList[3]
        self.assignInstType()
