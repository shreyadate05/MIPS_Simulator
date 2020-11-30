import sys
from simulator import startSimulator

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Invalid number of command line arguments")
    else:
        startSimulator(sys.argv)
