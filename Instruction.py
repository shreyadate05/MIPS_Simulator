import enum

id = -1

class InstructionType(enum.Enum):
    INV  = 0
    MEM  = 1
    ALU  = 2
    CTRL  = 3
    SPCL  = 4

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
        self.isExecutionDone = False
        self.isComplete = False

        self.IF = '0'
        self.ID = '0'
        self.IR = '0'
        self.EX = '0'
        self.WB = '0'
        self.Struct = 'N'
        self.WAW = 'N'
        self.RAW = 'N'
        self.iCache = 'X'
        self.dCache = ['X', 'X']

        self.dCachePenalty = 0
        self.dCacheStartClock = 0
        self.dCacheEndClock = 0
        self.checkedDCache = False
        self.checkICache = False

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def assignInstType(self):
        mem = ['LW','SW','LI','LUI', 'L.D', 'LD', 'S.D', 'SD']
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
        branch = ['J', 'BEQ', 'BNE']
        halt = ['HLT']

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
        if self.opcode in halt:
            self.unit = "HALT"


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
