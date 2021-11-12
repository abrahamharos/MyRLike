MAX_SLOTS = 3000

# global, local, temporal and constants
virtualMemoryDirectionMap = {
    'g_int': {
        'initialDirection': 2000,
        'counter': 0
    },
    'g_float': {
        'initialDirection': 5000,
        'counter': 0
    },
    'g_char': {
        'initialDirection': 8000,
        'counter': 0
    },
    'l_int': {
        'initialDirection': 10000,
        'counter': 0
    },
    'l_float': {
        'initialDirection': 13000,
        'counter': 0
    },
    'l_char': {
        'initialDirection': 16000,
        'counter': 0
    },
    't_int': {
        'initialDirection': 19000,
        'counter': 0
    },
    't_float': {
        'initialDirection': 21000,
        'counter': 0
    },
    't_char': {
        'initialDirection': 24000,
        'counter': 0
    },
    'c_int': {
        'initialDirection': 27000,
        'counter': 0
    },
    'c_float': {
        'initialDirection': 30000,
        'counter': 0
    },
    'c_char': {
        'initialDirection': 33000,
        'counter': 0
    },
    'c_string': {
        'initialDirection': 36000,
        'counter': 0
    },
}

def newVirtualDirection(currentType, currentFunction, programName):
    prefix = 'l_'
    if currentFunction == programName:
        prefix = 'g_'

    auxMemory = virtualMemoryDirectionMap[prefix + currentType]
    result = auxMemory['initialDirection'] + auxMemory['counter']

    if(auxMemory['counter'] > MAX_SLOTS - 1):
        print('Error: Too many variables declared (max is ' + str(MAX_SLOTS) + ')')
        exit()
    
    auxMemory['counter'] = auxMemory['counter'] + 1

    return result

def newTempVirtualDirection(currentType):
    auxMemory = virtualMemoryDirectionMap['t_' + currentType]
    result = auxMemory['initialDirection'] + auxMemory['counter']

    if(auxMemory['counter'] > MAX_SLOTS - 1):
        print('Error: Too many variables declared (max is ' + str(MAX_SLOTS) + ')')
        exit()
    
    auxMemory['counter'] = auxMemory['counter'] + 1

    return result

def newConstVirtualDirection(currentType):
    auxMemory = virtualMemoryDirectionMap['c_' + currentType]
    result = auxMemory['initialDirection'] + auxMemory['counter']

    if(auxMemory['counter'] > MAX_SLOTS - 1):
        print('Error: Too many variables declared (max is ' + str(MAX_SLOTS) + ')')
        exit()
    
    auxMemory['counter'] = auxMemory['counter'] + 1

    return result

def resetLocalAndTempCounters():
    virtualMemoryDirectionMap['l_int']['counter'] = 0
    virtualMemoryDirectionMap['l_float']['counter'] = 0
    virtualMemoryDirectionMap['l_char']['counter'] = 0

    virtualMemoryDirectionMap['t_int']['counter'] = 0
    virtualMemoryDirectionMap['t_float']['counter'] = 0
    virtualMemoryDirectionMap['t_char']['counter'] = 0