import json
import sys
from typing import get_args

from numpy.lib.polynomial import polyfit
import MemoryDirection as MD
import pprint
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

MAX_STACK = 5000

functionDirectory = {}
constantDirectory = {}
quadruples = {}
programName = ''
globalVarTable = {}
memoryDirection = MD.virtualMemory()
stackCounter = 0
debug = True
executionStack = []

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

def isPointer(operand):
    return isinstance(operand, list)

def getValueFromMemoryAddress(currVarTable, operand):
    global constantDirectory, globalVarTable

    if (isPointer(operand)):
        return getValueFromMemoryAddress(currVarTable, getValueFromMemoryAddress(currVarTable, operand[0]))

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
            print(len(globalVarTable['g']['int']))
            pprint.pprint(currVarTable['p']['int'])
        exit()

    return result

def getMemoryFromMemoryAddress(currVarTable, operand):
    if (isPointer(operand)):
        result = getMemoryFromMemoryAddress(currVarTable, getValueFromMemoryAddress(currVarTable, operand[0]))
        return result
    else:
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
            res = getMemoryFromMemoryAddress(varTable, operand3)

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
            res = getMemoryFromMemoryAddress(varTable, operand3)

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
            res = getMemoryFromMemoryAddress(varTable, operand3)
            result = op1
            assignTo(res, varTable, result)

        # Operaciones READ, WRITE
        if (operand0 == 'READ'):
            res = getMemoryFromMemoryAddress(varTable, operand3)
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
            res = getValueFromMemoryAddress(varTable, operand3)
            if (isinstance(res, str)):
                print(res[1:len(res) - 1])
            else:
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
            executionStack.append(calledFunctionVarTable)
            
        if (operand0 == 'PARAMETER'):
            # Assign parameter values to the current function memory
            res = getValueFromMemoryAddress(varTable, operand2)
            mem = getMemoryFromMemoryAddress(varTable, operand2)

            calledFunctionVarTable = executionStack[-1]
            calledFunctionVarTable['l'][mem[1]][operand3] = res

        if (operand0 == 'GOSUB'):
            calledFunction = operand2
            if (len(executionStack) >= MAX_STACK):
                print('Error: Stack Overflow')
                print('Maximum # calls allowed: ' + str(MAX_STACK))
                exit()
            calledFunctionVarTable = executionStack[-1]
            result = execute(operand3, calledFunctionVarTable)
            
            # save returned value from the function on global var table
            if (functionDirectory[calledFunction]['type'] != 'void'):
                auxNextQuad = quadruples[IP + 1]
                if(auxNextQuad[0] == '='):
                    auxMemory = getMemoryFromMemoryAddress(varTable, auxNextQuad[1])
                    assignTo(auxMemory, varTable, result)

        if (operand0 == 'RETURN'):
            result = getValueFromMemoryAddress(varTable, operand3)
            res = getMemoryFromMemoryAddress(varTable, operand3)
            executionStack.pop()
            return result

        if(operand0 == 'ENDFUNC'):
            executionStack.pop()
            return

        # Array's code ['verify'] and pointer access
        if(operand0 == 'verify'):
            value = getValueFromMemoryAddress(varTable, operand1)
            if (value < operand2 or value > operand3):
                print('Error: index out of bounds')
                exit()

        # Special functions (media, moda, varianza, regresionSimple, plotXY)
        if (operand0 == 'media'):
            numberList = [getValueFromMemoryAddress(varTable, operand2[0] + i) for i in range(0, operand2[1])]

            res = getMemoryFromMemoryAddress(varTable, operand3)
            assignTo(res, varTable, np.mean(numberList))
            
        if (operand0 == 'moda'):
            numberList = [getValueFromMemoryAddress(varTable, operand2[0] + i) for i in range(0, operand2[1])]

            res = getMemoryFromMemoryAddress(varTable, operand3)
            mode = stats.mode(numberList)
            assignTo(res, varTable, mode[0][0])

            
        if (operand0 == 'varianza'):
            numberList = [getValueFromMemoryAddress(varTable, operand2[0] + i) for i in range(0, operand2[1])]

            res = getMemoryFromMemoryAddress(varTable, operand3)
            assignTo(res, varTable, np.var(numberList))

        if(operand0 == 'regresionSimple'):
            xList = np.array([getValueFromMemoryAddress(varTable, operand3[0] + i) for i in range(0, operand3[1])])
            yList = np.array([getValueFromMemoryAddress(varTable, operand2[0] + i) for i in range(0, operand2[1])])

            m, b = polyfit(xList, yList, 1)

            plt.plot(xList, yList, 'o')
            plt.plot(xList, m * xList + b)
            plt.show()
        
        if(operand0 == 'plotXY'):
            xList = np.array([getValueFromMemoryAddress(varTable, operand3[0] + i) for i in range(0, operand3[1])])
            yList = np.array([getValueFromMemoryAddress(varTable, operand2[0] + i) for i in range(0, operand2[1])])

            plt.plot(xList, yList, 'o')
            plt.show()


        IP = IP + 1

def main(filename):
    global globalVarTable, programName
    
    loadData(filename)
    mountGlobalMemory()

    currVarTable = mountMemory(programName)
    IP = 0
    execute(IP, currVarTable)


if __name__ == '__main__':
    if(len(sys.argv) < 2):
        print("Please provide a valid filename as parameter\n Example: ovejota.myRLike")
        exit()

    main(sys.argv[1])