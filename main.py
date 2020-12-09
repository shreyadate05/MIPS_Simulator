import logging
import sys
from simulator import startSimulator

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='debug.log',
                    filemode='w')

log = logging.getLogger("MAIN          ")
log.info("STARTING MIPS SIMULATOR")

def parseCmd(argv):
    if len(argv) != 5:
       log.error("Invalid number of command line arguments")
    else:
        return argv

def test_case_1():
    argv = [0 for i in range(5)]
    argv[0] = ".\\test_cases\\test_case_1\\main.py"
    argv[1] = ".\\test_cases\\test_case_1\\inst.txt"
    argv[2] = ".\\test_cases\\test_case_1\\data.txt"
    argv[3] = ".\\test_cases\\test_case_1\\config.txt"
    argv[4] = "test_case_1_solution.txt"
    return argv

def test_case_2():
    argv = [0 for i in range(5)]
    argv[0] = ".\\test_cases\\test_case_2\\main.py"
    argv[1] = ".\\test_cases\\test_case_2\\inst.txt"
    argv[2] = ".\\test_cases\\test_case_2\\data.txt"
    argv[3] = ".\\test_cases\\test_case_2\\config.txt"
    argv[4] = "test_case_2_solution.txt"
    return argv


def test_case_3():
    argv = [0 for i in range(5)]
    argv[0] = ".\\test_cases\\test_case_3\\main.py"
    argv[1] = ".\\test_cases\\test_case_3\\inst.txt"
    argv[2] = ".\\test_cases\\test_case_3\\data.txt"
    argv[3] = ".\\test_cases\\test_case_3\\config.txt"
    argv[4] = "test_case_3_solution.txt"
    return argv


def example():
    argv = [0 for i in range(5)]
    argv[0] = ".\\test_cases\\example\\main.py"
    argv[1] = ".\\test_cases\\example\\inst.txt"
    argv[2] = ".\\test_cases\\example\\data.txt"
    argv[3] = ".\\test_cases\\example\\conf.txt"
    argv[4] = "project_example_solution.txt"
    return argv


if __name__ == '__main__':
    #argv = example()
    #argv = test_case_1()
    #argv = test_case_2()
    argv = test_case_3()
    startSimulator(argv)
    #startSimulator(sys.argv)
