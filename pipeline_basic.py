import logging
from mipsDefs import *

log = logging.getLogger("MIPS Pipeline")

fetchQueue = []
issueQueue = []
readQueue = []
execQueue = []
writeQueue = []

def fetch():
    pass

def issue():
    pass

def read():
    pass

def execute():
    pass

def write():
    pass

def start():
    global instructions, units, registers
    res = []
    done = False

    while not done:
        fetch()
        issue()
        read()
        execute()
        write()

    return res
