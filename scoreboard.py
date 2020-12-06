class Scoreboard:
    def __init__(self):
        self.id = 0
        self.instruction = ""
        self.IF = 0
        self.ID = 0
        self.IR = 0
        self.EX = 0
        self.WB = 0
        self.WAW = 'N'
        self.RAW = 'N'
        self.Struct = 'N'

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)