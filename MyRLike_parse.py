import sys
import MyRLike_lex
tokens = MyRLike_lex.tokens
from ply import yacc
import pprint
from cuboSemantico import CS

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
cuadruplos = []
tmpCounter = 0

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

def p_assignment(p):
    '''assignment   : variable EQUALS exp'''
    pass

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

# TODO
def p_quad_save_or(p):
    '''quad_save_or : '''
    global operandStack, operatorStack, typeStack

    currentOperator = p[-1]
    operatorStack.append(currentOperator)

def p_exp(p):
    '''exp          : t_exp OR quad_save_operator exp
                    | t_exp'''

def p_t_exp(p):
    '''t_exp        : g_exp AND quad_save_operator t_exp
                    | g_exp'''

def p_g_exp(p):
    '''g_exp        : m_exp
                    | m_exp LT quad_save_operator g_exp
                    | m_exp GT quad_save_operator g_exp
                    | m_exp EQ quad_save_operator g_exp
                    | m_exp NE quad_save_operator g_exp
                    | m_exp GTE quad_save_operator g_exp
                    | m_exp LTE quad_save_operator g_exp'''

def p_m_exp(p):
    '''m_exp        : t
                    | t PLUS quad_save_operator m_exp
                    | t MINUS quad_save_operator m_exp'''

# TODO
def p_quad_save_operator(p):
    '''quad_save_operator : '''
    global operandStack, operatorStack, typeStack

    currentOperator = p[-1]
    operatorStack.append(currentOperator)
    print(operatorStack)

def p_t(p):
    '''t            : f
                    | f TIMES quad_save_operator t
                    | f DIVIDE quad_save_operator t'''

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

def p_f(p):
    '''f            : LPAREN exp RPAREN
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

def p_read_param(p):
    '''read_param   : read_param COMMA read_param
                    | variable'''
    pass

def p_read(p):
    '''read         : READ LPAREN read_param RPAREN'''
    pass

def p_write_param(p):
    '''write_param  : write_param COMMA write_param
                    | exp
                    | STRING'''
    pass

def p_write(p):
    '''write        : WRITE LPAREN write_param RPAREN'''
    pass

def p_condition(p):
    '''condition    : IF LPAREN exp RPAREN block
                    | IF LPAREN exp RPAREN block ELSE block'''
    pass

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
    return result

if __name__ == '__main__':
    if(len(sys.argv) < 2):
        print("Please provide a valid filename as parameter\n Example: tests/parser/valid1.txt")
        exit()

    main(sys.argv[1])