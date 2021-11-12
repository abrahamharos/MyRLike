MAX_SLOTS = 3000
INITIAL_DIR = 0

class virtualMemory:
    def __init__(self):
        self.virtualMemoryDirectionMap = {
            'g_int': {
                'initialDirection': INITIAL_DIR + MAX_SLOTS * 0,
                'counter': 0
            },
            'g_float': {
                'initialDirection': INITIAL_DIR + MAX_SLOTS * 1,
                'counter': 0
            },
            'g_char': {
                'initialDirection': INITIAL_DIR + MAX_SLOTS * 2,
                'counter': 0
            },
            'l_int': {
                'initialDirection': INITIAL_DIR + MAX_SLOTS * 3,
                'counter': 0
            },
            'l_float': {
                'initialDirection': INITIAL_DIR + MAX_SLOTS * 4,
                'counter': 0
            },
            'l_char': {
                'initialDirection': INITIAL_DIR + MAX_SLOTS * 5,
                'counter': 0
            },
            't_int': {
                'initialDirection': INITIAL_DIR + MAX_SLOTS * 6,
                'counter': 0
            },
            't_float': {
                'initialDirection': INITIAL_DIR + MAX_SLOTS * 7,
                'counter': 0
            },
            't_char': {
                'initialDirection': INITIAL_DIR + MAX_SLOTS * 8,
                'counter': 0
            },
            'c_int': {
                'initialDirection': INITIAL_DIR + MAX_SLOTS * 9,
                'counter': 0
            },
            'c_float': {
                'initialDirection': INITIAL_DIR + MAX_SLOTS * 10,
                'counter': 0
            },
            'c_char': {
                'initialDirection': INITIAL_DIR + MAX_SLOTS * 11,
                'counter': 0
            },
            'c_string': {
                'initialDirection': INITIAL_DIR + MAX_SLOTS * 12,
                'counter': 0
            },
        }

    def newVirtualDirection(self, currentType, currentFunction, programName):
        prefix = 'l_'
        if currentFunction == programName:
            prefix = 'g_'

        auxMemory = self.virtualMemoryDirectionMap[prefix + currentType]
        result = auxMemory['initialDirection'] + auxMemory['counter']

        if(auxMemory['counter'] > MAX_SLOTS - 1):
            print('Error: Too many variables declared (max is ' + str(MAX_SLOTS) + ')')
            exit()
        
        auxMemory['counter'] = auxMemory['counter'] + 1

        return result

    def newTempVirtualDirection(self, currentType):
        auxMemory = self.virtualMemoryDirectionMap['t_' + currentType]
        result = auxMemory['initialDirection'] + auxMemory['counter']

        if(auxMemory['counter'] > MAX_SLOTS - 1):
            print('Error: Too many variables declared (max is ' + str(MAX_SLOTS) + ')')
            exit()
        
        auxMemory['counter'] = auxMemory['counter'] + 1

        return result

    def newConstVirtualDirection(self, currentType):
        auxMemory = self.virtualMemoryDirectionMap['c_' + currentType]
        result = auxMemory['initialDirection'] + auxMemory['counter']

        if(auxMemory['counter'] > MAX_SLOTS - 1):
            print('Error: Too many variables declared (max is ' + str(MAX_SLOTS) + ')')
            exit()
        
        auxMemory['counter'] = auxMemory['counter'] + 1

        return result

    def resetLocalAndTempCounters(self):
        self.virtualMemoryDirectionMap['l_int']['counter'] = 0
        self.virtualMemoryDirectionMap['l_float']['counter'] = 0
        self.virtualMemoryDirectionMap['l_char']['counter'] = 0

        self.virtualMemoryDirectionMap['t_int']['counter'] = 0
        self.virtualMemoryDirectionMap['t_float']['counter'] = 0
        self.virtualMemoryDirectionMap['t_char']['counter'] = 0

    def getTempCounters(self):
        iCounter = self.virtualMemoryDirectionMap['t_int']['counter']
        fCounter = self.virtualMemoryDirectionMap['t_float']['counter']
        cCounter = self.virtualMemoryDirectionMap['t_char']['counter'] = 0

        result = [iCounter, fCounter, cCounter]

        return result