
def isValidOpcode(sOpcode):
    pass

# INPUT:  String containing 1 instruction (eg. LW
# OUTPUT: Instruction object (calling object) initialized
def parseInstruction(sInstruction):
    sInstruction = sInstruction.replace(',', '')
    sInstruction = sInstruction.replace('\t', '')
    instParts =  sInstruction.split(" ")
    print(instParts)



