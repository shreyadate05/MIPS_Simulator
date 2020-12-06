import enum

id = 0

class InstructionType(enum.Enum):
    INV  = 0
    MEM  = 1
    ALU  = 2
    CTRL  = 3
    SPCL  = 4

class PipeStage(enum.Enum):
    INIT  = 0
    FETCH  = 1
    ISSUE  = 2
    READ  = 3
    EXEC  = 4
    WRITE = 5

class Instruction:
    def __init__(self):
        self.id       = 0
        self.inst     = ""
        self.opcode   = ""
        self.operand1 = ""
        self.operand2 = ""
        self.operand3 = ""
        self.hasLabel = False
        self.label    = ""
        self.type     = InstructionType.INV
        self.unit     = ""
        self.isComplete = False
        self.isExecutionDone = False
        self.isReadDone = False
        self.pipeStage = PipeStage.INIT

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def assignInstType(self):
        mem = ['LW','SW','LI','LUI']
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
        int = ['LI','LUI','AND','OR', 'ANDI','ORI', 'DADD', 'DADDI','DSUB', 'DSUBI']
        mem = ['L.D','S.D','LD','SD','LW','SW']
        add = ['ADD.D','SUB.D']
        mul = ['MUL.D']
        div = ['DIV.D']
        branch = ['HLT','J', 'BEQ', 'BNE']

        if self.opcode in int:
            self.unit = "INTEGER"
        if self.opcode in mem:
            self.unit = "MEMORY"
        if self.opcode in add:
            self.unit = "ADDER"
        if self.opcode in mul:
            self.unit = "MULTIPLIER"
        if self.opcode in div:
            self.unit = "DIVIDER"
        if self.opcode in branch:
            self.unit = "BRANCH"

    def createInstruction(self, instList):
        global id
        id += 1
        self.id = id
        self.inst = " ".join(instList)
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
