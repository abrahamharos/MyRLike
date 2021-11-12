MAX_SLOTS = 3000
INITIAL_DIR = 3000

class virtualMemory:
    def __init__(self):
        initialDirections = [i for i in range(INITIAL_DIR ,INITIAL_DIR + MAX_SLOTS * 13, MAX_SLOTS)]
        
        self.virtualMemoryDirectionMap = {
            'g_int': {
                'initialDirection': initialDirections[0],
                'counter': 0
            },
            'g_float': {
                'initialDirection': initialDirections[1],
                'counter': 0
            },
            'g_char': {
                'initialDirection': initialDirections[2],
                'counter': 0
            },
            'l_int': {
                'initialDirection': initialDirections[3],
                'counter': 0
            },
            'l_float': {
                'initialDirection': initialDirections[4],
                'counter': 0
            },
            'l_char': {
                'initialDirection': initialDirections[5],
                'counter': 0
            },
            't_int': {
                'initialDirection': initialDirections[6],
                'counter': 0
            },
            't_float': {
                'initialDirection': initialDirections[7],
                'counter': 0
            },
            't_char': {
                'initialDirection': initialDirections[8],
                'counter': 0
            },
            'c_int': {
                'initialDirection': initialDirections[9],
                'counter': 0
            },
            'c_float': {
                'initialDirection': initialDirections[10],
                'counter': 0
            },
            'c_char': {
                'initialDirection': initialDirections[11],
                'counter': 0
            },
            'c_string': {
                'initialDirection': initialDirections[12],
                'counter': 0
            },
        }

        self.inverseVirtualMemoryDirectionMap = {
            initialDirections[0]: 'g_int',
            initialDirections[1]: 'g_float',
            initialDirections[2]: 'g_char',
            initialDirections[3]: 'l_int',
            initialDirections[4]: 'l_float',
            initialDirections[5]: 'l_char',
            initialDirections[6]: 't_int',
            initialDirections[7]: 't_float',
            initialDirections[8]: 't_char',
            initialDirections[9]: 'c_int',
            initialDirections[10]: 'c_float',
            initialDirections[11]: 'c_char',
            initialDirections[12]: 'c_string',
        }
        print(self.inverseVirtualMemoryDirectionMap)
        
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