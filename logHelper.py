import logging

log = logging.getLogger("MIPS Simulator")

def formResultString(res):
    s = ""
    for a, b, c, d, e, f, g, h, i, j, k, l in zip(res[::12], res[1::12], res[2::12], res[3::12], res[4::12], res[5::12], res[6::12], res[7::12], res[8::12], res[9::12],res[10::12], res[11::12]):
        s = '{:<25}{:<25}{:<25}{:<25}{:<25}{:<25}{:<25}{:<25}{:<25}{:<25}{:<25}{:<}'.format(a,b,c,d,e,f,g,h,i,j,k,l)
    return s

def logResult(res):
    log.debug(res)
    resultString = ""
    res[1:].sort(key = lambda x: int(x[2]))
    for row in res:
        resultString += formResultString(row) + "\n"
    print(resultString)
    return resultString

def logStateAtClockStart(clockCount, registers, programCounter, iCache, iCacheMissQueue, dCache):
    log.debug("Clock Cycle: " + str(clockCount))
    log.debug("Registers Map: ")
    log.debug(registers)
    log.debug("Program Counter: ")
    log.debug(programCounter)
    log.debug("I-Cache: ")
    log.debug(iCache)
    log.debug("I-Cache Miss Queue: ")
    log.debug(iCacheMissQueue)
    log.debug("D-Cache: ")
    log.debug(dCache)


def logQueue(q):
    if len(q) == 0:
        return
    s = []
    for i in q:
        s.append(str(i.id))
    log.debug(", ".join(s))

def logUnitAvailability(instruction, ans):
    if not ans:
        log.debug("Unit " + instruction.unit + " is not available for instruction " + str(instruction.id))
