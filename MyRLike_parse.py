import sys
import types
import MyRLike_lex
tokens = MyRLike_lex.tokens
from ply import yacc
import pprint
from cuboSemantico import CS, checkValidOperators
import MemoryDirection as MD
import json

functionDirectory = {}
currentType = ''
currentVariableName = ''
currentFunction = ''
programName = ''
constantDirectory = {
    'int': {},
    'float': {},
    'char': {},
    'string': {}
}

# Cuadruplos
operandStack = []
typeStack = []
operatorStack = []
quadruples = []
temporals = []
jumpStack = []
quadCounter = 0
forControlStack = []
parameterCounter = 0
calledFunction = ''
memoryDirection = MD.virtualMemory()

# Arrays
currentDim = 0
currentR = 0
dimensionStack = []

def p_program(p):
    '''program      : PROGRAM ID save_program_data SEMI save_main_ip body end_function
                    | PROGRAM ID save_program_data SEMI vars_dec save_main_ip body end_function
                    | PROGRAM ID save_program_data SEMI vars_dec func_dec save_main_ip body end_function'''
    
    global functionDirectory
    
    print('\n')
    #pprint.pprint(functionDirectory)

# To save the # of quad where the main function begins.
def p_save_main_ip(p):
    '''save_main_ip : '''
    global jumpStack, quadCounter, quadruples

    # Fill the pending quadruple
    endOfTheJump = jumpStack.pop()
    currentQuad = quadruples[endOfTheJump]
    quadruple = (currentQuad[0], currentQuad[1], currentQuad[2], quadCounter)

    quadruples[endOfTheJump] = quadruple

def p_save_program_data(p):
    '''save_program_data : '''
    
    global programName, currentType, currentFunction, jumpStack, quadruples, quadCounter
    
    programName = p[-1]
    currentFunction = p[-1]
    currentType = 'program'

    functionDirectory[currentFunction] = {
        'type': currentType,
        'vars': {}
    }

    jumpStack.append(quadCounter)
    quadruple = ('goto', '', '', '') # Pending quadruple
    quadruples.append(quadruple)
    quadCounter = quadCounter + 1

    memoryDirection.resetLocalAndTempCounters()

    # Init size of the function, each field indicates the # of variables of that type
    # [# local ints, # local floats, # local chars, # temp ints, # temp floats, # temp chars,  # pointer ints, # pointer floats, # pointer chars]
    functionDirectory[currentFunction]['size'] = [0, 0, 0, 0, 0, 0, 0, 0, 0]


def p_set_main_current_function(p):
    '''set_main_current_function :   '''

    global currentFunction
    currentFunction = programName

def p_body(p):
    '''body         : MAIN set_main_current_function LPAREN RPAREN block'''
    pass

def p_block(p):
    '''block        : LBRACE statement RBRACE'''
    pass

def p_statement(p):
    '''statement    : statement statement
                    | assignment SEMI
                    | call SEMI
                    | return SEMI
                    | read SEMI
                    | write SEMI
                    | condition
                    | while_loop
                    | for_loop'''
    pass

def p_quad_generate_assignment(p):
    '''quad_generate_assignment : '''
    global operatorStack, operandStack, typeStack, temporals, quadruples, quadCounter, functionDirectory, currentFunction
    
    if (len(operatorStack) > 0):
        currentOperator = operatorStack[-1]
        if (currentOperator == '='):
            operatorStack.pop()
            
            rightOperand = operandStack.pop()
            rightType = typeStack.pop()
            leftOperand = operandStack.pop()
            leftType = typeStack.pop()

            resultType = checkValidOperators(rightOperand, rightType, leftOperand, leftType, currentOperator)

            quadruple = (currentOperator, rightOperand, '', leftOperand)
            quadCounter = quadCounter + 1
            
            quadruples.append(quadruple)

def p_assignment(p):
    '''assignment   : variable EQUALS quad_save_operator exp quad_generate_assignment'''

def p_array_dim_stack_push(p):
    '''array_dim_stack_push : '''
    global functionDirectory, currentFunction, programName, operandStack, operatorStack, typeStack, currentVariableName, currentDim, dimensionStack

    currentDim = 0
    dimensionStack.append(currentVariableName)
    operatorStack.append('(')
    
    currentVariable = p[-1]

    # Check if currentVariable exist in the currentFunction Scope
    # If not, check for the global one.
    if not(currentVariable in functionDirectory[currentFunction]['vars'].keys()):
        if (currentVariable in functionDirectory[programName]['vars'].keys()):
            currentVariableName = currentVariable
        else:
            print("Array \'" + currentVariable + "\' does not exist")
            exit()
    else:
        currentVariableName = currentVariable

def p_array_quad_verify(p):
    '''array_quad_verify : '''
    global operandStack, quadruples, quadCounter, functionDirectory, currentFunction, currentDim, currentVariableName
    currentDim = currentDim + 1

    inferiorLimit = 0
    superiorLimit = functionDirectory[currentFunction]['vars'][currentVariableName]['dim'][currentDim]['limit'] - 1

    quadruple = ('verify', operandStack[-1], inferiorLimit, superiorLimit) # Pending quadruple
    quadruples.append(quadruple)
    quadCounter = quadCounter + 1

def p_array_quad_multiply(p):
    '''array_quad_multiply : '''

    global operandStack, typeStack, quadruples, quadCounter, functionDirectory, currentFunction, currentVariableName, currentDim

    mdim = functionDirectory[currentFunction]['vars'][currentVariableName]['dim'][currentDim]['m']
    
    currentType = typeStack.pop()
    if (currentType != 'int'):
        print('Error: Type mismatch')
        print('You can only access arrays with integer values')
        exit()
    temporal = memoryDirection.newTempVirtualDirection(currentType)

    quadruple = ('*', operandStack.pop(), mdim, temporal) # Pending quadruple
    quadruples.append(quadruple)
    quadCounter = quadCounter + 1
    
    operandStack.append(temporal)
    typeStack.append(currentType)

def p_array_quad_sum_d(p):
    '''array_quad_sum_d :'''

    global operandStack, typeStack, quadruples, quadCounter, functionDirectory, currentFunction

    aux2 = operandStack.pop()
    aux2Type = typeStack.pop()
    aux1 = operandStack.pop()
    aux1Type = typeStack.pop()

    resultType = checkValidOperators(aux1, aux1Type, aux2, aux2Type, '+')

    if (resultType != 'int'):
        print('Error: Type mismatch')
        print('You can only access arrays with integer values')
        exit()
    temporal = memoryDirection.newTempVirtualDirection(resultType)

    quadruple = ('+', aux1, aux2, temporal) # Pending quadruple
    quadruples.append(quadruple)
    quadCounter = quadCounter + 1

    operandStack.append(temporal)
    typeStack.append(currentType)

def p_array_sum_base(p):
    '''array_sum_base :'''

    global currentDim, functionDirectory, currentFunction, currentVariableName, operandStack, operatorStack, typeStack, quadCounter, quadruples
    
    # Verify that all dimensions were accessed.
    nDimensions = len(functionDirectory[currentFunction]['vars'][currentVariableName]['dim'])
    if (currentDim != nDimensions):
        print('Error: Trying to access dimensions that does not exists')
        print('the current array has ' + str(nDimensions) + " dimensions and you\' are trying to access " + str(currentDim))
        exit()

    aux1 = operandStack.pop()
    aux1Type = typeStack.pop()
    arrType = functionDirectory[currentFunction]['vars'][currentVariableName]['type']

    baseAddress = functionDirectory[currentFunction]['vars'][currentVariableName]['virDir']
    tempPointer = memoryDirection.newTempPointer(arrType)

    quadruple = ('+', aux1, baseAddress, tempPointer) # Pending quadruple
    quadruples.append(quadruple)
    quadCounter = quadCounter + 1

    operandStack.append(tempPointer) # Contains address
    typeStack.append(arrType)
    
    if(operatorStack[-1] != '('):
        print('Error: calculating exp inside array')
        exit()
    operatorStack.pop()

def p_md_variable(p):
    '''md_variable  : LBRACKET exp array_quad_verify RBRACKET array_quad_multiply array_quad_sum_d md_variable
                    | LBRACKET exp array_quad_verify RBRACKET array_sum_base'''
    pass

def p_quad_save_vars(p):
    '''quad_save_vars : '''
    global functionDirectory, currentFunction, programName, operandStack, operatorStack, typeStack, currentVariableName
    
    currentVariable = p[-1]

    # Check if currentVariable exist in the currentFunction Scope
    # If not, check for the global one.
    if not(currentVariable in functionDirectory[currentFunction]['vars'].keys()):
        if (currentVariable in functionDirectory[programName]['vars'].keys()):
            operandStack.append(functionDirectory[programName]['vars'][currentVariable]['virDir'])
            typeStack.append(functionDirectory[programName]['vars'][currentVariable]['type'])
        else:
            print("Variable \'" + currentVariable + "\' does not exist")
            exit()
    else:
        operandStack.append(functionDirectory[currentFunction]['vars'][currentVariable]['virDir'])
        typeStack.append(functionDirectory[currentFunction]['vars'][currentVariable]['type'])

def p_variable(p):
    '''variable     : ID quad_save_vars
                    | ID array_dim_stack_push md_variable'''
    pass

def p_quad_generate(p):
    '''quad_generate : '''
    global operatorStack, operandStack, typeStack, temporals, quadruples, quadCounter
    
    validOperators = ['||', '&', '<', '<=', '>', '>=', '!=', '==', '+', '-', '*', '/']
    if (len(operatorStack) > 0):
        currentOperator = operatorStack[-1]
        if (currentOperator in validOperators):
            operatorStack.pop()
            
            rightOperand = operandStack.pop()
            rightType = typeStack.pop()
            leftOperand = operandStack.pop()
            leftType = typeStack.pop()
            
            resultType = checkValidOperators(rightOperand, rightType, leftOperand, leftType, currentOperator)

            result = memoryDirection.newTempVirtualDirection(resultType)
            quadruple = (currentOperator, leftOperand, rightOperand, result)
            quadCounter = quadCounter + 1
            
            quadruples.append(quadruple)
            operandStack.append(result)
            typeStack.append(resultType)

def p_exp(p):
    '''exp          : t_exp quad_generate OR quad_save_operator exp
                    | t_exp quad_generate'''

def p_t_exp(p):
    '''t_exp        : g_exp quad_generate AND quad_save_operator t_exp
                    | g_exp quad_generate '''

def p_g_exp(p):
    '''g_exp        : m_exp quad_generate
                    | m_exp quad_generate LT quad_save_operator g_exp
                    | m_exp quad_generate GT quad_save_operator g_exp
                    | m_exp quad_generate EQ quad_save_operator g_exp
                    | m_exp quad_generate NE quad_save_operator g_exp
                    | m_exp quad_generate GTE quad_save_operator g_exp
                    | m_exp quad_generate LTE quad_save_operator g_exp'''
            
def p_m_exp(p):
    '''m_exp        : t quad_generate
                    | t quad_generate PLUS quad_save_operator m_exp
                    | t quad_generate MINUS quad_save_operator m_exp'''

# TODO
def p_quad_save_operator(p):
    '''quad_save_operator : '''
    global operandStack, operatorStack, typeStack

    currentOperator = p[-1]
    operatorStack.append(currentOperator)

def p_t(p):
    '''t            : f
                    | f quad_generate TIMES quad_save_operator t
                    | f quad_generate DIVIDE quad_save_operator t'''

def p_quad_save_int(p):
    '''quad_save_int :  '''
    global operandStack, typeStack
    
    currentValue = p[-1]
    if (currentValue not in constantDirectory['int'].keys()):
        constantDirectory['int'][currentValue] = memoryDirection.newConstVirtualDirection('int')

    operandStack.append(constantDirectory['int'][currentValue])
    typeStack.append('int')

def p_quad_save_float(p):
    '''quad_save_float : '''
    global operandStack, typeStack
    
    currentValue = p[-1]
    if (currentValue not in constantDirectory['float'].keys()):
        constantDirectory['float'][currentValue] = memoryDirection.newConstVirtualDirection('float')

    operandStack.append(constantDirectory['float'][currentValue])
    typeStack.append('float')

def p_quad_save_char(p):
    '''quad_save_char : '''
    global operandStack, typeStack
    
    currentValue = p[-1]
    if (currentValue not in constantDirectory['char'].keys()):
        constantDirectory['char'][currentValue] = memoryDirection.newConstVirtualDirection('char')

    operandStack.append(constantDirectory['char'][currentValue])
    typeStack.append('char')

def p_quad_close_parenthesis(p):
    '''quad_close_parenthesis : '''
    global operatorStack
    
    currentOperator = operatorStack[-1]
    if (currentOperator == '('):
        operatorStack.pop()

def p_f(p):
    '''f            : LPAREN quad_save_operator exp RPAREN quad_close_parenthesis
                    | variable
                    | call
                    | INT quad_save_int
                    | FLOAT quad_save_float
                    | CHAR quad_save_char'''
    pass

def p_function_parameter(p):
    '''function_parameter : '''
    
    global operandStack, typeStack, functionDirectory, calledFunction, parameterCounter, quadCounter, quadruples

    argument = operandStack.pop()
    argumentType = typeStack.pop()

    nParameters = len(functionDirectory[calledFunction]['parameters'])
    if(parameterCounter >= nParameters):
        print("ERROR when calling function \'" + calledFunction + "\'\nExpected: " + str(nParameters) + " parameters")
        print("Received: " + str(parameterCounter + 1))
        exit()

    # Verify argument type against parameter table
    expectedParameterType = functionDirectory[calledFunction]['parameters'][parameterCounter]

    if (argumentType != expectedParameterType):
        print("ERROR when calling function \'" + calledFunction + "\'\nExpected: \'" + expectedParameterType + "\' as paremeter")
        print("Received: \'" + argumentType + "\'")
        exit()

    quadruple = ('PARAMETER', '', argument, parameterCounter)
    quadruples.append(quadruple)
    quadCounter = quadCounter + 1
    
    parameterCounter = parameterCounter + 1

def p_call_param(p):
    '''call_param   : call_param COMMA call_param
                    | exp function_parameter'''
    pass

def p_function_verify_ERA(p):
    '''function_verify_ERA : '''

    global functionDirectory, quadruples, quadCounter, parameterCounter, calledFunction

    calledFunction = p[-1]

    # verify that function exists
    if(calledFunction not in functionDirectory.keys()):
        print("ERROR: Function named \'" + calledFunction + "\' does not exist")
        exit()
    
    # generate ERA action
    functionSize = functionDirectory[calledFunction]['size']
    quadruple = ('ERA', '', '', functionSize)
    quadruples.append(quadruple)
    quadCounter = quadCounter + 1

    # Start parameter counter
    parameterCounter = 0

def p_function_end_call(p):
    '''function_end_call : '''

    global functionDirectory, calledFunction, parameterCounter, quadruples, quadCounter

    # Verify that all parameters were provided
    nParameters = len(functionDirectory[calledFunction]['parameters'])
    if(parameterCounter < nParameters):
        print("ERROR when calling function \'" + calledFunction + "\'\nExpected: " + str(nParameters) + " parameters")
        print("Received: " + str(parameterCounter))
        exit()
    
    # generate GOSUB quadruple
    initialDirection = functionDirectory[calledFunction]['initialDirection']
    quadruple = ('GOSUB', '', calledFunction, initialDirection)
    quadruples.append(quadruple)
    quadCounter = quadCounter + 1

def p_call(p):
    '''call         : ID function_verify_ERA LPAREN call_param RPAREN function_end_call
                    | ID function_verify_ERA LPAREN RPAREN function_end_call'''
    pass

def p_quad_generate_read(p):
    '''quad_generate_read : '''

    global quadruples, quadCounter

    readVariable = operandStack.pop()
    readVariableType = typeStack.pop()
    quadruple = ('READ', '', '', readVariable)
    quadruples.append(quadruple)
    quadCounter = quadCounter + 1

def p_read(p):
    '''read         : READ LPAREN variable quad_generate_read RPAREN'''
    pass

def p_quad_insert_string(p):
    '''quad_insert_string : '''
    global typeStack, operandStack

    typeStack.append('STRING')

    currentValue = p[-1]
    if (currentValue not in constantDirectory['string'].keys()):
        constantDirectory['string'][currentValue] = memoryDirection.newConstVirtualDirection('string')

    operandStack.append(constantDirectory['string'][currentValue])

def p_write_param(p):
    '''write_param  : write_param COMMA write_param
                    | exp quad_generate_write
                    | STRING quad_insert_string quad_generate_write'''
    pass

def p_quad_generate_write(p):
    '''quad_generate_write : '''

    global operandStack, typeStack, quadruples, quadCounter

    currentOperand = operandStack.pop()
    typeStack.pop()

    quadruple = ('WRITE', '', '', currentOperand)
    quadruples.append(quadruple)
    quadCounter = quadCounter + 1


def p_write(p):
    '''write        : WRITE LPAREN write_param RPAREN'''
    pass

def p_quad_generate_jump_gotof(p):
    '''quad_generate_jump_gotof : '''

    global jumpStack, operandStack, typeStack, operatorStack, quadCounter, quadruples

    currentExpType = typeStack.pop()
    if (currentExpType != 'int'):
        print('Error: Type mismatch')
        print('You can only evaluate integer values in an IF expression')
        exit()
    
    result = operandStack.pop()

    quadruple = ('gotof', result, '', '') # Pending quadruple
    quadruples.append(quadruple)
    quadCounter = quadCounter + 1

    jumpStack.append(quadCounter - 1)


def p_quad_generate_jump_fill(p):
    '''quad_generate_jump_fill : '''

    global jumpStack, quadCounter, quadruples

    # Fill the pending quadruple
    endOfTheJump = jumpStack.pop()
    currentQuad = quadruples[endOfTheJump]
    quadruple = (currentQuad[0], currentQuad[1], currentQuad[2], quadCounter)

    quadruples[endOfTheJump] = quadruple

def p_quad_generate_goto(p):
    '''quad_generate_goto : '''
    
    global jumpStack, quadCounter, quadruples
    
    quadruple = ('goto', '', '', '') # Pending quadruple
    quadruples.append(quadruple)
    quadCounter = quadCounter + 1

    jumpWhenFinishTrue = jumpStack.pop()
    jumpStack.append(quadCounter - 1)

    # Fill the pending quadruple
    currentQuad = quadruples[jumpWhenFinishTrue]
    quadruple = (currentQuad[0], currentQuad[1], currentQuad[2], quadCounter)

    quadruples[jumpWhenFinishTrue] = quadruple


def p_condition(p):
    '''condition    : IF LPAREN exp RPAREN quad_generate_jump_gotof block quad_generate_jump_fill
                    | IF LPAREN exp RPAREN quad_generate_jump_gotof block ELSE quad_generate_goto block quad_generate_jump_fill'''

def p_quad_generate_save_jump(p):
    '''quad_generate_save_jump  : '''

    global jumpStack,quadCounter
    jumpStack.append(quadCounter)

def p_quad_generate_goto_return(p):
    '''quad_generate_goto_return : '''

    global jumpStack, quadCounter, quadruples
    
    # Fill the pending quadruples
    endOfTheJump = jumpStack.pop()
    returnJump = jumpStack.pop()

    # Generate quad goto return
    quadruple = ('goto', '', '', returnJump) # Pending quadruple
    quadruples.append(quadruple)
    quadCounter = quadCounter + 1

    # Fill the pending quadruple
    currentQuad = quadruples[endOfTheJump]
    quadruple = (currentQuad[0], currentQuad[1], currentQuad[2], quadCounter)

    quadruples[endOfTheJump] = quadruple
    
def p_while_loop(p):
    '''while_loop   : WHILE quad_generate_save_jump LPAREN exp RPAREN quad_generate_jump_gotof DO block quad_generate_goto_return'''
    pass

def p_quad_generate_is_int(p):
    '''quad_generate_is_int   :   '''

    global operandStack, typeStack

    currentExpType = typeStack[-1]
    if (currentExpType != 'int'):
        print('Error: Type mismatch')
        print('You can only use integer values for control variables in a FOR loop')
        exit()

def p_quad_generate_control_variable(p):
    '''quad_generate_control_variable   :   '''

    global operandStack, typeStack, operatorStack, quadCounter, quadruples, forControlStack

    currentExp = operandStack.pop()
    currentExpType = typeStack.pop()
    if (currentExpType != 'int'):
        print('Error: Type mismatch')
        print('You can only assign integer values for control variables in a FOR loop')
        exit()

    controlVariable = operandStack.pop()
    controlVariableType = typeStack.pop()
    currentOperator = '='
    forControlStack.append(controlVariable)

    checkValidOperators(currentExp, currentExpType, controlVariable, controlVariableType, currentOperator)
    
    # generate control varibale assignment quad
    quadruple = ('=', currentExp, '', controlVariable) # Pending quadruple
    quadruples.append(quadruple)
    quadCounter = quadCounter + 1

def p_quad_generate_final_control_variable(p):
    '''quad_generate_final_control_variable :   '''
    global operandStack, typeStack, operatorStack, quadCounter, quadruples, forControlStack

    currentExp = operandStack[-1]
    currentExpType = typeStack[-1]
    if (currentExpType != 'int'):
        print('Error: Type mismatch')
        print('You can only assign integer values for stop conditions in a FOR loop')
        exit()

    stopCondition = memoryDirection.newTempVirtualDirection(currentExpType)

    # generate stop condition variable assignment quad
    quadruple = ('=', currentExp, '', stopCondition) # Pending quadruple
    quadruples.append(quadruple)
    quadCounter = quadCounter + 1

    controlVariable = forControlStack[-1]
    result = memoryDirection.newTempVirtualDirection(currentExpType)

    # generate stop condition variable assignment quad
    quadruple = ('<', controlVariable, stopCondition, result)
    quadruples.append(quadruple)
    quadCounter = quadCounter + 1

    jumpStack.append(quadCounter - 1)

    # generate stop condition variable assignment quad
    quadruple = ('gotof', result, '', '')
    quadruples.append(quadruple)
    quadCounter = quadCounter + 1

    jumpStack.append(quadCounter - 1)

def p_quad_generate_end_for_iteration(p):
    '''quad_generate_end_for_iteration  :   '''

    global operandStack, typeStack, operatorStack, quadCounter, quadruples, forControlStack

    controlVariable = forControlStack.pop()

    result = memoryDirection.newTempVirtualDirection('int')

    if (1 not in constantDirectory['int'].keys()):
        constantDirectory['int'][1] = memoryDirection.newConstVirtualDirection('int')

    quadruple = ('+', controlVariable, constantDirectory['int'][1], result)
    quadruples.append(quadruple)
    quadCounter = quadCounter + 1

    quadruple = ('=', result, '', controlVariable)
    quadruples.append(quadruple)
    quadCounter = quadCounter + 1

    # Fill the pending quadruples
    endOfTheJump = jumpStack.pop()
    returnJump = jumpStack.pop()

    # Generate quad goto return
    quadruple = ('goto', '', '', returnJump) # Pending quadruple
    quadruples.append(quadruple)
    quadCounter = quadCounter + 1

    # Fill the pending quadruple
    currentQuad = quadruples[endOfTheJump]
    quadruple = (currentQuad[0], currentQuad[1], currentQuad[2], quadCounter)

    quadruples[endOfTheJump] = quadruple
    
    operandStack.pop()
    typeStack.pop()

def p_for_loop(p):
    '''for_loop     : FOR variable quad_generate_is_int EQUALS exp quad_generate_control_variable TO exp quad_generate_final_control_variable DO block quad_generate_end_for_iteration'''
    pass

def p_type(p):
    '''type         : TYPEINT
                    | TYPEFLOAT
                    | TYPECHAR'''
    
    global currentType
    currentType = p[1]

def p_array_save_limit(p):
    '''array_save_limit : '''

    global functionDirectory, currentFunction, currentVariableName, currentDim, currentR

    superiorLimit = p[-1]
    functionDirectory[currentFunction]['vars'][currentVariableName]['dim'][currentDim] = {
        'limit': superiorLimit
    }
    currentR = (superiorLimit + 1) * currentR
    currentDim = currentDim + 1

def p_array_calculate_m(p):
    '''array_calculate_m : '''
    global functionDirectory, currentFunction, currentVariableName, currentDim, currentR, currentType

    dimensions = functionDirectory[currentFunction]['vars'][currentVariableName]['dim']

    arrSize = currentR

    functionDirectory[currentFunction]['vars'][currentVariableName]['virDir'] = memoryDirection.newVirtualDirection(currentType, currentFunction, programName, arrSize)

    for i in range(0, len(dimensions)):
        mdim = int(currentR / (dimensions[i + 1]['limit'] + 1))
        functionDirectory[currentFunction]['vars'][currentVariableName]['dim'][i + 1]['m'] = mdim
        currentR = mdim

    # Update function size
    typeOrder = {'int':0, 'float':1, 'char':2}
    index = typeOrder[currentType]
    functionDirectory[currentFunction]['size'][index] = functionDirectory[currentFunction]['size'][index] + arrSize

def p_vars_md_id(p):
    '''vars_md_id   : LBRACKET INT array_save_limit RBRACKET vars_md_id
                    | LBRACKET INT array_save_limit RBRACKET array_calculate_m'''

def p_array_init_dim(p):
    '''array_init_dim : '''

    global functionDirectory, currentFunction, currentType, currentVariableName, programName, currentDim, currentR
    localVariableName = p[-1]
    
    if localVariableName in functionDirectory[currentFunction]['vars']:
        # Throw Multiple declaration error
        print("Variable " + localVariableName + " declared multiple times in the same scope")
        exit()
    else:
        functionDirectory[currentFunction]['vars'][localVariableName] = {
            'type': currentType,
        }
    
    currentVariableName = localVariableName

    currentDim = 1
    currentR = 1

    functionDirectory[currentFunction]['vars'][currentVariableName]['dim'] = {
        currentDim: {}
    }


def p_vars_id_dec(p):
    '''vars_id_dec  : vars_id_dec COMMA vars_id_dec
                    | ID save_variable_name
                    | ID array_init_dim vars_md_id'''

def p_save_variable_name(p):
    '''save_variable_name : '''
    
    global functionDirectory, currentFunction, currentType, currentVariableName, programName
    localVariableName = p[-1]
    
    if localVariableName in functionDirectory[currentFunction]['vars']:
        # Throw Multiple declaration error
        print("Variable " + localVariableName + " declared multiple times in the same scope")
        exit()
    else:
        functionDirectory[currentFunction]['vars'][localVariableName] = {
            'type': currentType,
            'virDir': memoryDirection.newVirtualDirection(currentType, currentFunction, programName, 1)
        }
    
        # Update function size
        typeOrder = {'int':0, 'float':1, 'char':2}
        index = typeOrder[currentType]
        functionDirectory[currentFunction]['size'][index] = functionDirectory[currentFunction]['size'][index] + 1
    
    currentVariableName = localVariableName

def p_vars_body(p):
    '''vars_body    : vars_body vars_body
                    | type vars_id_dec SEMI'''

def p_vars_dec(p):
    '''vars_dec     : VARS save_VARTable vars_body'''

def p_save_VARTable(p):
    '''save_VARTable : '''

    global currentFunction, functionDirectory
    
    # Check if current_function already has a var table.
    # If not, initialize one.
    if not("vars" in functionDirectory[currentFunction].keys()):
        functionDirectory[currentFunction]['vars'] = {}

def p_count_fucntion_parameter(p):
    '''count_function_parameter : '''
    global functionDirectory, currentFunction, currentType

    functionDirectory[currentFunction]['parameters'].append(currentType)


def p_func_params(p):
    '''func_params  :   func_params COMMA func_params
                    |   save_VARTable type ID save_variable_name count_function_parameter'''

def p_func_type(p):
    '''func_type    :   type
                    |   VOID'''
    
    # When p[1] is set it means that is a void function since
    # other types are being handle in p_type
    if (p[1]):
        global currentType
        currentType = p[1]

def p_del_var_table(p):
    '''del_var_table : '''

    global functionDirectory, currentFunction

    # Delete VARS table since is not longer needed
    del functionDirectory[currentFunction]['vars']

def p_end_func(p):
    '''end_function : del_var_table'''
    global functionDirectory, currentFunction, quadruples, quadCounter

    if(currentFunction != programName):
        # Generate ENDFUNC quadruple
        quadruple = ('ENDFUNC', '', '', '') # Pending quadruple
        quadruples.append(quadruple)
        quadCounter = quadCounter + 1

    # Update size of the function with the space used by temporal variables
    tempCounters = memoryDirection.getTempCounters()
    functionDirectory[currentFunction]['size'][3] = tempCounters[0]
    functionDirectory[currentFunction]['size'][4] = tempCounters[1]
    functionDirectory[currentFunction]['size'][5] = tempCounters[2]
    functionDirectory[currentFunction]['size'][6] = tempCounters[3]
    functionDirectory[currentFunction]['size'][7] = tempCounters[4]
    functionDirectory[currentFunction]['size'][8] = tempCounters[5]

def p_func_dec(p):
    '''func_dec     :   func_dec func_dec
                    |   FUNC func_type ID save_function_data LPAREN RPAREN vars_dec block end_function
                    |   FUNC func_type ID save_function_data LPAREN func_params RPAREN vars_dec block end_function
                    |   FUNC func_type ID save_function_data LPAREN RPAREN block end_function
                    |   FUNC func_type ID save_function_data LPAREN func_params RPAREN block end_function'''

def p_save_function_data(p):
    '''save_function_data : '''

    global functionDirectory, programName

    localFunctionName = p[-1]

    # Check if functionDirectory already has a function with the same name
    # If not, initialize one.
    if localFunctionName in functionDirectory.keys():
        # Throw Multiple declaration error
        print("Function " + localFunctionName + " declared multiple times")
        exit()

    global currentType, currentFunction, quadCounter
    
    currentFunction = localFunctionName

    functionDirectory[currentFunction] = {
        'type': currentType
    }

    memoryDirection.resetLocalAndTempCounters()

    # Save initial direction (instruction pointer) of the function
    functionDirectory[currentFunction]['initialDirection'] = quadCounter

    # Init size of the function, each field indicates the # of variables of that type
    # [# local ints, # local floats, # local chars, # temp ints, # temp floats, # temp chars,  # pointer ints, # pointer floats, # pointer chars]
    functionDirectory[currentFunction]['size'] = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    # Init parameter array.
    functionDirectory[currentFunction]['parameters'] = []

def p_quad_generate_return(p):
    '''quad_generate_return : '''

    global functionDirectory, currentFunction, quadruples, quadCounter, typeStack, operandStack

    currentExpType = typeStack.pop()
    functionReturnType = functionDirectory[currentFunction]['type']
    if (currentExpType != functionReturnType):
        print('Error: Type mismatch')
        print('You can only return ' + functionReturnType + ' in the ' + currentFunction + ' function')
        print('received type: ' + currentExpType)
        exit()
    
    result = operandStack.pop()

    if(currentFunction != programName):
        # Generate RETURN quadruple
        quadruple = ('RETURN', '', '', result)
        quadruples.append(quadruple)
        quadCounter = quadCounter + 1


def p_return(p):
    '''return       :   RETURN LPAREN exp quad_generate_return RPAREN'''
    pass

def p_error(t):
    print("Syntax error at '%s'" % t.value)
    sys.exit(1)

# To flip key => value and delete sectioning
def transform_constant_directory():    
    aux = constantDirectory['int'].copy()
    aux.update(constantDirectory['float'])
    aux.update(constantDirectory['char'])
    aux.update(constantDirectory['string'])

    result = dict((x,y) for y,x in aux.items())

    return result

# To call the parser run MyRLike_parse.py with the name of the txt file
# Example:
# python3 MyRLike_parse.py testValid.txt
def main(programFileName, exportedFileName):
    programFileName = open(programFileName).read()

    parser = yacc.yacc()

    yacc.parse(programFileName)
    result = "Valid tokens and sintax"
    print(result)

    # print(operandStack)
    # print(typeStack)

    print('\n\n')
    pprint.pprint(functionDirectory)

    print('******* Cuadruplos generados *******')
    counter = 0
    for quad in quadruples:
        print(str(counter) + ' -\t' + str(quad))
        counter = counter + 1

    print('\n\n')
    print(constantDirectory)

    tConstantDirectory = transform_constant_directory()

    # Export compiled file that will be use for the Virtual Machine
    try:
        data = json.dumps({
            'programName': programName,
            'functionDirectory': functionDirectory,
            'constantDirectory': tConstantDirectory,
            'quadruples': quadruples
        })

        compiledFile = open(exportedFileName, "w")
        compiledFile.write(data)
        compiledFile.close()

        print('File compiled succesfully as ' + exportedFileName)
    except:
        print('An Error ocurred while saving the compiled file')
        exit()
        
    return result

if __name__ == '__main__':
    if(len(sys.argv) < 3):
        print("Please provide a valid filename as parameter\n Example: tests/parser/valid1.txt")
        print("And the name of the exported file\n Example: ovejota.myRLike")
        exit()

    main(sys.argv[1], sys.argv[2])