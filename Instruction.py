import enum

id = 0

class InstructionType(enum.Enum):
    INV  = 0
    MEM  = 1
    ALU  = 2
    CTRL  = 3
    SPCL  = 4

class InstructionUnit(enum.Enum):
    INV  = 0
    INT  = 1
    ADD  = 2
    MUL  = 3
    DIV  = 4
    NON  = 5

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
        self.unit     = InstructionUnit.INV

    def assignInstType(self):
        mem = ['LW','SW','L.D','S.D','LD','SD','LI','LUI']
        alu = ['ADD.D','SUB.D','AND','OR', 'ANDI','ORI', 'DADD', 'DSUB', 'DADDI','DSUBI', 'MUL.D', 'DIV.D']
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

    def assignInstUnit(self):
        int = ['LW','SW','L.D','S.D','LD','SD','LI','LUI',
               'AND','OR', 'ANDI','ORI', 'DADD', 'DADDI','DSUB', 'DSUBI']
        add = ['ADD.D','SUB.D']
        mul = ['MUL.D']
        div = ['DIV.D']
        non = ['HLT','J', 'BEQ', 'BNE']

        if self.opcode in int:
            self.unit = InstructionUnit.INT
        if self.opcode in add:
            self.unit = InstructionUnit.ADD
        if self.opcode in mul:
            self.unit = InstructionUnit.MUL
        if self.opcode in div:
            self.unit = InstructionUnit.DIV
        if self.opcode in non:
            self.unit = InstructionUnit.NON

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
        self.assignInstUnit()
