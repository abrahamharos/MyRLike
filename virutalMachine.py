import json
import sys
import MemoryDirection as MD
import pprint

MAX_STACK = 5000

functionDirectory = {}
constantDirectory = {}
quadruples = {}
programName = ''
globalVarTable = {}
memoryDirection = MD.virtualMemory()
stackCounter = 0
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
    global functionDirectory, programName, globalVarTable

    globalVarTable = {
        'g' : {
            'int': [None for _ in range(functionDirectory[programName]['size'][0])],
            'float': [None for _ in range(functionDirectory[programName]['size'][1])],
            'char': [None for _ in range(functionDirectory[programName]['size'][2])]
        },
    }

def mountMemory(functionName):
    global functionDirectory

    currVarTable = {
        'l' : {
            'int': [None for _ in range(functionDirectory[functionName]['size'][0])],
            'float': [None for _ in range(functionDirectory[functionName]['size'][1])],
            'char': [None for _ in range(functionDirectory[functionName]['size'][2])]
        },
        't' : {
            'int': [None for _ in range(functionDirectory[functionName]['size'][3])],
            'float': [None for _ in range(functionDirectory[functionName]['size'][4])],
            'char': [None for _ in range(functionDirectory[functionName]['size'][5])]
        },
        'p' : {
            'int': [None for _ in range(functionDirectory[functionName]['size'][6])],
            'float': [None for _ in range(functionDirectory[functionName]['size'][7])],
            'char': [None for _ in range(functionDirectory[functionName]['size'][8])]
        },
    }

    return currVarTable

def getValueFromMemoryAddress(currVarTable, operand):
    global constantDirectory, globalVarTable

    opType = operand // MD.MAX_SLOTS
    opPosition = operand % MD.MAX_SLOTS

    scope = memoryDirection.inverseVirtualMemoryDirectionMap[opType][0]
    operandType = memoryDirection.inverseVirtualMemoryDirectionMap[opType][2:]

    if (scope == 'c'):
        result = constantDirectory[str(operand)]
    elif (scope == 'g'):
        result = globalVarTable[scope][operandType][opPosition]
    else:
        result = currVarTable[scope][operandType][opPosition]
    
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

def assignTo(memoryDirection, varTable, result):
    global globalVarTable

    if (memoryDirection[0] == 'g'):
        globalVarTable[memoryDirection[0]][memoryDirection[1]][memoryDirection[2]] = result
    else:
        varTable[memoryDirection[0]][memoryDirection[1]][memoryDirection[2]] = result

def execute(IP, varTable):
    global stackCounter

    calledFunction = ''
    calledFunctionVarTable = {}

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
            op1 = getValueFromMemoryAddress(varTable, operand1)
            op2 = getValueFromMemoryAddress(varTable, operand2)
            res = getMemoryFromMemoryAddress(operand3)

            if (operand0 == '+'):
                result = op1 + op2
                assignTo(res, varTable, result)
            if (operand0 == '-'):
                result = op1 - op2
                assignTo(res, varTable, result)
            if (operand0 == '*'):
                result = op1 * op2
                assignTo(res, varTable, result)
            if (operand0 == '/'):
                result = op1 / op2
                assignTo(res, varTable, result)
            
        # Operaciones logicas <, >, ==, !=, ||, &, >=, <=
        operacionesLogicas = ['<', '>', '==', '!=', '||', '&', '>=', '<=']
        if (operand0 in operacionesLogicas):
            op1 = getValueFromMemoryAddress(varTable, operand1)
            op2 = getValueFromMemoryAddress(varTable, operand2)
            res = getMemoryFromMemoryAddress(operand3)

            if (operand0 == '<'):
                if (op1 < op2):
                    tempRes = 1
                else:
                    tempRes = 0
                result = tempRes
                assignTo(res, varTable, result)
            if (operand0 == '>'):
                if (op1 > op2):
                    tempRes = 1
                else:
                    tempRes = 0
                result = tempRes
                assignTo(res, varTable, result)
            if (operand0 == '=='):
                if (op1 == op2):
                    tempRes = 1
                else:
                    tempRes = 0
                result = tempRes
                assignTo(res, varTable, result)
            if (operand0 == '||'):
                if (op1 or op2):
                    tempRes = 1
                else:
                    tempRes = 0
                result = tempRes
                assignTo(res, varTable, result)
            if (operand0 == '&'):
                if (op1 and op2):
                    tempRes = 1
                else:
                    tempRes = 0
                result = tempRes
                assignTo(res, varTable, result)
            if (operand0 == '>='):
                if (op1 >= op2):
                    tempRes = 1
                else:
                    tempRes = 0
                result = tempRes
                assignTo(res, varTable, result)
            if (operand0 == '<='):
                if (op1 <= op2):
                    tempRes = 1
                else:
                    tempRes = 0
                result = tempRes
                assignTo(res, varTable, result)

        # Asignaciones =
        if (operand0 == '='):
            op1 = getValueFromMemoryAddress(varTable, operand1)
            res = getMemoryFromMemoryAddress(operand3)
            result = op1
            assignTo(res, varTable, result)

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
            result = temp
            assignTo(res, varTable, result)

        if (operand0 == 'WRITE'):
            # This allows to print Null value (for debugging)
            # TODO: for strings trim the "" 
            res = getValueFromMemoryAddress(varTable, operand3)
            print(res)

        # Saltos goto, gotof
        if (operand0 == 'goto'):
            IP = int(operand3)
            continue
        
        if (operand0 == 'gotof'):
            res = getValueFromMemoryAddress(varTable, operand1)
            if (res == 0):
                IP = int(operand3)
                continue

        # Funciones ERA, PARAMETER, GOSUB, ENDFUNC, RETURN
        if (operand0 == 'ERA'):
            # Mount function memory
            calledFunctionVarTable = mountMemory(operand3)
            
        if (operand0 == 'PARAMETER'):
            # Assign parameter values to the current function memory
            res = getValueFromMemoryAddress(varTable, operand2)
            mem = getMemoryFromMemoryAddress(operand2)

            calledFunctionVarTable['l'][mem[1]][operand3] = res

        if (operand0 == 'GOSUB'):
            calledFunction = operand2
            stackCounter = stackCounter + 1
            if (stackCounter >= MAX_STACK):
                print('Error: Stack Overflow')
                print('Maximum # calls allowed: ' + str(MAX_STACK))
                exit()
            result = execute(operand3, calledFunctionVarTable)
            
            # save returned value from the function on global var table
            if (functionDirectory[calledFunction]['type'] != 'void'):
                auxNextQuad = quadruples[IP + 1]
                if(auxNextQuad[0] == '='):
                    auxMemory = getMemoryFromMemoryAddress(auxNextQuad[1])
                    assignTo(auxMemory, varTable, result)

                    del calledFunctionVarTable

        if (operand0 == 'RETURN'):
            result = getValueFromMemoryAddress(varTable, operand3)
            res = getMemoryFromMemoryAddress(operand3)
            stackCounter = stackCounter - 1
            return result

        if(operand0 == 'ENDFUNC'):
            stackCounter = stackCounter - 1
            return

        
        IP = IP + 1

def main(filename):
    global globalVarTable, programName
    
    loadData(filename)
    mountGlobalMemory()

    currVarTable = mountMemory(programName)
    IP = 0
    pprint.pprint(functionDirectory[programName])
    execute(IP, currVarTable)


if __name__ == '__main__':
    if(len(sys.argv) < 2):
        print("Please provide a valid filename as parameter\n Example: ovejota.myRLike")
        exit()

    main(sys.argv[1])