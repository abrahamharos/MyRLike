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
        
        operand0 = currentQuad[0]
        operand1 = currentQuad[1]
        operand2 = currentQuad[2]
        operand3 = currentQuad[3]

        # Operaciones Aritmeticas + - * /
        operacionesAritmeticas = ['+', '-', '*', '/']
        if(operand0 in operacionesAritmeticas):
            op1 = getValueFromMemoryAddress(operand1)
            op2 = getValueFromMemoryAddress(operand2)
            res = getMemoryFromMemoryAddress(operand3)

            if (operand0 == '+'):
                varTable[res[0]][res[1]][res[2]] = op1 + op2
            if (operand0 == '-'):
                varTable[res[0]][res[1]][res[2]] = op1 - op2
            if (operand0 == '*'):
                varTable[res[0]][res[1]][res[2]] = op1 * op2
            if (operand0 == '/'):
                varTable[res[0]][res[1]][res[2]] = op1 / op2
            
        # Operaciones logicas <, >, ==, !=, ||, &, >=, <=
        operacionesLogicas = ['<', '>', '==', '!=', '||', '&', '>=', '<=']
        if (operand0 in operacionesLogicas):
            op1 = getValueFromMemoryAddress(operand1)
            op2 = getValueFromMemoryAddress(operand2)
            res = getMemoryFromMemoryAddress(operand3)

            if (operand0 == '<'):
                if (op1 < op2):
                    tempRes = 1
                else:
                    tempRes = 0
                varTable[res[0]][res[1]][res[2]] = tempRes
            if (operand0 == '>'):
                if (op1 > op2):
                    tempRes = 1
                else:
                    tempRes = 0
                varTable[res[0]][res[1]][res[2]] = tempRes
            if (operand0 == '=='):
                if (op1 == op2):
                    tempRes = 1
                else:
                    tempRes = 0
                varTable[res[0]][res[1]][res[2]] = tempRes
            if (operand0 == '||'):
                if (op1 or op2):
                    tempRes = 1
                else:
                    tempRes = 0
                varTable[res[0]][res[1]][res[2]] = tempRes
            if (operand0 == '&'):
                if (op1 and op2):
                    tempRes = 1
                else:
                    tempRes = 0
                varTable[res[0]][res[1]][res[2]] = tempRes
            if (operand0 == '>='):
                if (op1 >= op2):
                    tempRes = 1
                else:
                    tempRes = 0
                varTable[res[0]][res[1]][res[2]] = tempRes
            if (operand0 == '<='):
                if (op1 <= op2):
                    tempRes = 1
                else:
                    tempRes = 0
                varTable[res[0]][res[1]][res[2]] = tempRes

        # Asignaciones =
        if (operand0 == '='):
            op1 = getValueFromMemoryAddress(operand1)
            res = getMemoryFromMemoryAddress(operand3)
            varTable[res[0]][res[1]][res[2]] = op1

        # Operaciones READ, WRITE
        if (operand0 == 'READ'):
            res = getMemoryFromMemoryAddress(operand3)
            tempInput = input()
            if (res[1] == 'int'):
                try:
                    temp = int(tempInput)
                except:
                    print('Error: expected value type: INT')
                    exit()
            if (res[1] == 'float'):
                try:
                    temp = float(tempInput)
                except:
                    print('Error: expected value type: FLOAT')
                    exit()
            if (res[1] == 'char'):
                try:
                    temp = str(tempInput)
                    if(len(temp) > 1):
                        print('Error: expected a single character')
                        exit()
                except:
                    print('Error: expected value type: CHAR')
                    exit()
                
            # Check type
            varTable[res[0]][res[1]][res[2]] = temp

        if (operand0 == 'WRITE'):
            # This allows to print Null value (for debugging)
            # TODO: for strings trim the "" 
            res = getValueFromMemoryAddress(operand3)
            print(res)

        # Saltos goto, gotof
        if (operand0 == 'goto'):
            IP = int(operand3)
            continue
        
        if (operand0 == 'gotof'):
            res = getValueFromMemoryAddress(operand1)
            if (res == 0):
                IP = int(operand3)
                continue


        # Funciones ERA, GOSUB, PARAMETER, ENDFUNC, RETURN

        IP = IP + 1

if __name__ == '__main__':
    if(len(sys.argv) < 2):
        print("Please provide a valid filename as parameter\n Example: ovejota.myRLike")
        exit()

    main(sys.argv[1])