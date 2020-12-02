import sys
import logging
import datetime
from simulator import startSimulator

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='debug.log',
                    filemode='w')

log = logging.getLogger("MAIN")
log.info("STARTING MIPS SIMULATOR")

if __name__ == '__main__':
    if len(sys.argv) != 5:
        log.error("Invalid number of command line arguments")
    else:
        startSimulator(sys.argv)
