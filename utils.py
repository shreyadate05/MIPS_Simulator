import sys

def parseFile(sFilename):
    file = open(sFilename)
    data = file.readlines()
    for i in range(len(data)):
        data[i] = data[i].replace("\n", "")
    return data