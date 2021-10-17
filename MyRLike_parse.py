import sys
import types
import MyRLike_lex
tokens = MyRLike_lex.tokens
from ply import yacc
import pprint
from cuboSemantico import CS, checkValidOperators

# TODO: Move this declaration/functions to a separate file.
# TODO: Delete VAR tables once parser finish
functionDirectory = {}
currentType = ''
currentVariableName = ''
currentFunction = ''
programName = ''

# Cuadruplos
operandStack = []
typeStack = []
operatorStack = []
quadruples = []
temporals = []
tmpCounter = 0
jumpStack = []
quadCounter = 0

def p_program(p):
    '''program      : PROGRAM ID save_program_data SEMI body
                    | PROGRAM ID save_program_data SEMI vars_dec body
                    | PROGRAM ID save_program_data SEMI vars_dec func_dec body'''
    
    global functionDirectory
    
    print('\n')
    #pprint.pprint(functionDirectory)

def p_save_program_data(p):
    '''save_program_data : '''
    
    global programName, currentType, currentFunction
    
    programName = p[-1]
    currentFunction = p[-1]
    currentType = 'program'

    functionDirectory[currentFunction] = {
        'type': currentType
    }

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
    global operatorStack, operandStack, typeStack, temporals, tmpCounter, quadruples, quadCounter
    
    if (len(operatorStack) > 0):
        currentOperator = operatorStack[-1]
        if (currentOperator == '='):
            operatorStack.pop()
            
            rightOperand = operandStack.pop()
            rightType = typeStack.pop()
            leftOperand = operandStack.pop()
            leftType = typeStack.pop()
            
            resultType = checkValidOperators(rightOperand, rightType, leftOperand, leftType, currentOperator)

            # TODO: replace t+str() for memory spaces
            quadruple = (currentOperator, rightOperand, '', leftOperand)
            quadCounter = quadCounter + 1
            
            quadruples.append(quadruple)

def p_assignment(p):
    '''assignment   : variable EQUALS quad_save_operator exp quad_generate_assignment'''

def p_md_variable(p):
    '''md_variable  : LBRACKET INT RBRACKET md_variable
                    | LBRACKET INT RBRACKET'''
    pass

def p_quad_save_vars(p):
    '''quad_save_vars : '''
    global functionDirectory, currentFunction, programName, operandStack, operatorStack, typeStack
    
    currentVariable = p[-1]

    # Check if currentVariable exist in the currentFunction Scope
    # If not, check for the global one.
    if not(currentVariable in functionDirectory[currentFunction]['vars'].keys()):
        if (currentVariable in functionDirectory[programName]['vars'].keys()):
            operandStack.append(currentVariable)
            typeStack.append(functionDirectory[programName]['vars'][currentVariable]['type'])
        else:
            print("Variable \'" + currentVariable + "\' does not exist")
            exit()
    else:
        operandStack.append(currentVariable)
        typeStack.append(functionDirectory[currentFunction]['vars'][currentVariable]['type'])

# TODO: Save arrays in VARS directory
def p_variable(p):
    '''variable     : ID quad_save_vars
                    | ID md_variable'''
    pass

def p_quad_generate(p):
    '''quad_generate : '''
    global operatorStack, operandStack, typeStack, temporals, tmpCounter, quadruples, quadCounter
    
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

            # TODO: replace t+str() for memory spaces
            result = 't' +  str(tmpCounter)
            quadruple = (currentOperator, leftOperand, rightOperand, result)
            tmpCounter = tmpCounter + 1
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

    operandStack.append(currentValue)
    typeStack.append('int')

def p_quad_save_float(p):
    '''quad_save_float : '''
    global operandStack, typeStack
    
    currentValue = p[-1]

    operandStack.append(currentValue)
    typeStack.append('float')

def p_quad_save_char(p):
    '''quad_save_char : '''
    global operandStack, typeStack
    
    currentValue = p[-1]

    operandStack.append(currentValue)
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

def p_call_param(p):
    '''call_param   : call_param COMMA call_param
                    | exp'''
    pass

def p_call(p):
    '''call         : ID LPAREN call_param RPAREN'''
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
    operandStack.append(p[-1])

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

def p_while_loop(p):
    '''while_loop   : WHILE LPAREN exp RPAREN DO block'''
    pass

def p_for_loop(p):
    '''for_loop     : FOR variable EQUALS exp TO exp DO block'''
    pass

def p_type(p):
    '''type         : TYPEINT
                    | TYPEFLOAT
                    | TYPECHAR'''
    
    global currentType
    currentType = p[1]

def p_vars_md_id(p):
    '''vars_md_id   : LBRACKET INT RBRACKET vars_md_id
                    | LBRACKET INT RBRACKET'''
    pass

def p_vars_id_dec(p):
    '''vars_id_dec  : vars_id_dec COMMA vars_id_dec
                    | ID save_variable_name
                    | ID save_variable_name vars_md_id'''

def p_save_variable_name(p):
    '''save_variable_name : '''
    
    global functionDirectory, currentFunction, currentType, currentVariableName
    localVariableName = p[-1]
    
    if localVariableName in functionDirectory[currentFunction]['vars']:
        # Throw Multiple declaration error
        print("Variable " + localVariableName + " declared multiple times in the same scope")
        exit()
    else:
        functionDirectory[currentFunction]['vars'][localVariableName] = {
            'type': currentType
        }

def p_vars_body(p):
    '''vars_body    : vars_body vars_body
                    | type vars_id_dec SEMI'''
    pass

def p_vars_dec(p):
    '''vars_dec     : VARS save_VARTable vars_body'''

def p_save_VARTable(p):
    '''save_VARTable : '''

    global currentFunction, functionDirectory
    
    # Check if current_function already has a var table.
    # If not, initialize one.
    if not("vars" in functionDirectory[currentFunction].keys()):
        functionDirectory[currentFunction]['vars'] = {}

def p_func_params(p):
    '''func_params  :   func_params COMMA func_params
                    |   save_VARTable type ID save_variable_name'''

def p_func_type(p):
    '''func_type    :   type
                    |   VOID'''
    
    # When p[1] is set it means that is a void function since
    # other types are being handle in p_type
    if (p[1]):
        global currentType
        currentType = p[1]

def p_func_dec(p):
    '''func_dec     :   func_dec func_dec
                    |   FUNC func_type ID save_function_data LPAREN RPAREN vars_dec block
                    |   FUNC func_type ID save_function_data LPAREN func_params RPAREN vars_dec block
                    |   FUNC func_type ID save_function_data LPAREN RPAREN block
                    |   FUNC func_type ID save_function_data LPAREN func_params RPAREN block'''

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

    global currentType, currentFunction
    
    currentFunction = localFunctionName

    functionDirectory[currentFunction] = {
        'type': currentType
    }

def p_return(p):
    '''return       :   RETURN LPAREN exp RPAREN'''
    pass

def p_error(t):
    print("Syntax error at '%s'" % t.value)
    sys.exit(1)


# To call the parser run MyRLike_parse.py with the name of the txt file
# Example:
# python3 MyRLike_parse.py testValid.txt
def main(fileName):
    fileName = open(fileName).read()

    parser = yacc.yacc()

    yacc.parse(fileName)
    result = "Valid tokens and sintax"
    print(result)

    print('******* Cuadruplos generados *******')
    counter = 0
    for quad in quadruples:
        print(str(counter) + ' -\t' + str(quad))
        counter = counter + 1
    
    return result

if __name__ == '__main__':
    if(len(sys.argv) < 2):
        print("Please provide a valid filename as parameter\n Example: tests/parser/valid1.txt")
        exit()

    main(sys.argv[1])