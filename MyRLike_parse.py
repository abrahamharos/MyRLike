import sys
import MyRLike_lex
tokens = MyRLike_lex.tokens
from ply import yacc

tokenlist = []
preclist = []

def p_program(p):
    '''program      : PROGRAM ID SEMI body
                    | PROGRAM ID SEMI vars_dec body
                    | PROGRAM ID SEMI vars_dec func_dec body'''
    pass

def p_body(p):
    '''body         : MAIN LPAREN RPAREN block'''
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

def p_variable(p):
    '''variable     : ID
                    | ID md_variable'''
    pass

def p_exp(p):
    '''exp          : t_exp OR exp
                    | t_exp'''
    pass

def p_t_exp(p):
    '''t_exp        : g_exp AND t_exp
                    | g_exp'''
    pass

def p_g_exp(p):
    '''g_exp        : m_exp
                    | m_exp LT m_exp
                    | m_exp GT m_exp
                    | m_exp EQ m_exp
                    | m_exp NE m_exp'''
    pass

def p_m_exp(p):
    '''m_exp        : t
                    | t PLUS t
                    | t MINUS t'''
    pass

def p_t(p):
    '''t            : f
                    | f TIMES f
                    | f DIVIDE f'''
    pass

def p_f(p):
    '''f            : LPAREN exp RPAREN
                    | variable
                    | call
                    | INT
                    | FLOAT
                    | CHAR'''
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
    pass

def p_vars_md_id(p):
    '''vars_md_id   : LBRACKET INT RBRACKET vars_md_id
                    | LBRACKET INT RBRACKET'''
    pass

def p_vars_id_dec(p):
    '''vars_id_dec  : vars_id_dec COMMA vars_id_dec
                    | ID
                    | ID vars_md_id'''
    pass

def p_vars_body(p):
    '''vars_body    : vars_body vars_body
                    | type vars_id_dec SEMI'''
    pass

def p_vars_dec(p):
    '''vars_dec     : VARS vars_body'''
    pass

def p_func_params(p):
    '''func_params  :   func_params COMMA func_params
                    |   type ID'''
    pass

def p_func_type(p):
    '''func_type    :   type
                    |   VOID'''
    pass

def p_func_dec(p):
    '''func_dec     :   func_dec func_dec
                    |   FUNC func_type ID LPAREN RPAREN block
                    |   FUNC func_type ID LPAREN func_params RPAREN block'''
    pass

def p_return(p):
    '''return       :   RETURN LPAREN exp RPAREN'''
    pass

def p_error(t):
    print("ERROR")
    exit()


# To call the parser run MyRLike_parse.py with the name of the txt file
# Example:
# python3 MyRLike_parse.py testValid.txt
def main():
    parser = yacc.yacc()

    validProgram = open(sys.argv[1]).read()

    yacc.parse(validProgram)
    print("Valid tokens and sintax")

if __name__ == '__main__':
    main()