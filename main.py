import sys

instFile = ""
dataFile = ""
configFile = ""
ansFile = ""

def startSimulator(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Invalid number of command line arguments")
        return -1


    startSimulator('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
