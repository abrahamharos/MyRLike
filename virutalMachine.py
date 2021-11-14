import json
import sys
import MemoryDirection as MD
import pprint

functionDirectory = {}
constantDirectory = {}
quadruples = {}
programName = ''
varTable = {}
memoryDirection = MD.virtualMemory()
IP = 0
debug = True

def loadData(filename):
    global functionDirectory, constantDirectory, quadruples, programName

    try:
        f = open(filename,)
        data = json.load(f)

        functionDirectory = data['functionDirectory']
        constantDirectory = data['constantDirectory']
        quadruples = data['quadruples']
        programName = data['programName']
    except:
        print('An Error ocurred while opening the compiled file ' + filename)
        exit()

def mountGlobalMemory():
    global varTable

    varTable = {
        'g' : {
            'int': [None for _ in range(functionDirectory[programName]['size'][0])],
            'float': [None for _ in range(functionDirectory[programName]['size'][1])],
            'char': [None for _ in range(functionDirectory[programName]['size'][2])]
        },
        't' : {
            'int': [None for _ in range(functionDirectory[programName]['size'][3])],
            'float': [None for _ in range(functionDirectory[programName]['size'][4])],
            'char': [None for _ in range(functionDirectory[programName]['size'][5])]
        },
    }

def getValueFromMemoryAddress(operand):
    global varTable, constantDirectory

    opType = operand // MD.MAX_SLOTS
    opPosition = operand % MD.MAX_SLOTS

    scope = memoryDirection.inverseVirtualMemoryDirectionMap[opType][0]
    operandType = memoryDirection.inverseVirtualMemoryDirectionMap[opType][2:]

    if (scope == 'c'):
        result = constantDirectory[str(operand)]
    else:
        result = varTable[scope][operandType][opPosition]
    
    if (result == None):
        print('Error: Trying to get the value of a var that is not SET.')
        if (debug == True):
            print(scope)
            print(operandType)
            print(opPosition)
        exit()

    return result

def getMemoryFromMemoryAddress(operand):
    opType = operand // MD.MAX_SLOTS
    opPosition = operand % MD.MAX_SLOTS

    scope = memoryDirection.inverseVirtualMemoryDirectionMap[opType][0]
    operandType = memoryDirection.inverseVirtualMemoryDirectionMap[opType][2:]

    return [scope, operandType, opPosition]

def main(filename):
    global IP, varTable
    loadData(filename)
    mountGlobalMemory()
    
    # Pending: Mount everything in memory
    while(IP < len(quadruples)):
        currentQuad = quadruples[IP]
        
        operator = currentQuad[0]
        operand1 = currentQuad[1]
        operand2 = currentQuad[2]
        saveResult = currentQuad[3]

        # Operaciones Aritmeticas + - * /
        operacionesAritmeticas = ['+', '-', '*', '/']
        if(operator in operacionesAritmeticas):
            op1 = getValueFromMemoryAddress(operand1)
            op2 = getValueFromMemoryAddress(operand2)
            res = getMemoryFromMemoryAddress(saveResult)

            if (operator == '+'):
                varTable[res[0]][res[1]][res[2]] = op1 + op2
            if (operator == '-'):
                varTable[res[0]][res[1]][res[2]] = op1 - op2
            if (operator == '*'):
                varTable[res[0]][res[1]][res[2]] = op1 * op2
            if (operator == '/'):
                varTable[res[0]][res[1]][res[2]] = op1 / op2
            
        # Operaciones logicas <, >, ==, !=, ||, &, >=, <=
        operacionesLogicas = ['<', '>', '==', '!=', '||', '&', '>=', '<=']
        if (operator in operacionesLogicas):
            op1 = getValueFromMemoryAddress(operand1)
            op2 = getValueFromMemoryAddress(operand2)
            res = getMemoryFromMemoryAddress(saveResult)

            if (operator == '<'):
                if (op1 < op2):
                    tempRes = 1
                else:
                    tempRes = 0
                varTable[res[0]][res[1]][res[2]] = tempRes
            if (operator == '>'):
                if (op1 > op2):
                    tempRes = 1
                else:
                    tempRes = 0
                varTable[res[0]][res[1]][res[2]] = tempRes
            if (operator == '=='):
                if (op1 == op2):
                    tempRes = 1
                else:
                    tempRes = 0
                varTable[res[0]][res[1]][res[2]] = tempRes
            if (operator == '||'):
                if (op1 or op2):
                    tempRes = 1
                else:
                    tempRes = 0
                varTable[res[0]][res[1]][res[2]] = tempRes
            if (operator == '&'):
                if (op1 and op2):
                    tempRes = 1
                else:
                    tempRes = 0
                varTable[res[0]][res[1]][res[2]] = tempRes
            if (operator == '>='):
                if (op1 >= op2):
                    tempRes = 1
                else:
                    tempRes = 0
                varTable[res[0]][res[1]][res[2]] = tempRes
            if (operator == '<='):
                if (op1 <= op2):
                    tempRes = 1
                else:
                    tempRes = 0
                varTable[res[0]][res[1]][res[2]] = tempRes

        # Asignaciones =
        if (operator == '='):
            op1 = getValueFromMemoryAddress(operand1)
            res = getMemoryFromMemoryAddress(saveResult)

            varTable[res[0]][res[1]][res[2]] = op1

        # Operaciones READ, WRITE

        # Saltos goto, gotof

        # Funciones ERA, GOSUB, PARAMETER, ENDFUNC, RETURN


        IP = IP + 1
    pprint.pprint(varTable)

if __name__ == '__main__':
    if(len(sys.argv) < 2):
        print("Please provide a valid filename as parameter\n Example: ovejota.myRLike")
        exit()

    main(sys.argv[1])