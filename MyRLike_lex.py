# ----------------------------------------------------------------------
# MyRLike_lex.py
#
# Token specifications for symbols in MyRLike 2021.
# ----------------------------------------------------------------------
from ply import lex

# Reserved words
tokens = [
    # Literals (id, cteI, cteF, cteS)
    'ID', 'INT', 'FLOAT', 'STRING', 'CHAR',

    # Operators (+, -, *, /, <, >, ==, !=, ||, &, >=, <=)
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LT', 'GT', 'EQ', 'NE', 'OR', 'AND', 'GTE', 'LTE',

    # Assignment (=)
    'EQUALS',

    # Delimeters ( ) { } [ ] , ;
    'LPAREN', 'RPAREN',
    'LBRACE', 'RBRACE',
    'LBRACKET', 'RBRACKET',
    'COMMA', 'SEMI',

    # Conditional statements (if, else)
    'IF', 'ELSE',

    # Loops (for, do, to, while)
    'FOR', 'DO', 'TO', 'WHILE',

    # Operations (read, write)
    'READ', 'WRITE',

    # Declaration (Program, VARS, int, float, main, func, void, return)
    'PROGRAM', 'VARS', 'TYPEINT', 'TYPEFLOAT', 'TYPECHAR', 'MAIN', 'FUNC', 'VOID', 'RETURN',
]

reserverd = {
    'if':       'IF',
    'else':     'ELSE',
    'for':      'FOR',
    'do':       'DO',
    'to':       'TO',
    'while':    'WHILE',
    'read':     'READ',
    'write':    'WRITE',
    'Program':  'PROGRAM',
    'VARS':     'VARS',
    'int':      'TYPEINT',
    'float':    'TYPEFLOAT',
    'char':     'TYPECHAR',
    'main':     'MAIN',
    'func':     'FUNC',
    'void':     'VOID',
    'return':   'RETURN',
}

# Completely ignored characters (whitespace, tab and new line)
t_ignore = ' \t\n'

# Operators
t_PLUS             = r'\+'
t_MINUS            = r'-'
t_TIMES            = r'\*'
t_DIVIDE           = r'/'
t_LT               = r'<'
t_GT               = r'>'
t_EQ               = r'=='
t_NE               = r'!='
t_OR               = r'\|\|'
t_AND              = r'&'
t_GTE              = r'>='
t_LTE              = r'<='

# Assignment operators
t_EQUALS           = r'='

# Delimeters
t_LPAREN           = r'\('
t_RPAREN           = r'\)'
t_LBRACE           = r'\{'
t_RBRACE           = r'\}'
t_LBRACKET         = r'\['
t_RBRACKET         = r'\]'
t_COMMA            = r','
t_SEMI             = r';'

# Char definition
t_CHAR = r'\'([A-Za-z]|[0-9])\''

# String literal
t_STRING = r'\"([^\\\n]|(\\.))*?\"'

# Literals
# Identifiers
def t_ID(t):
    r'[A-Za-z][A-Za-z0-9]*'
    t.type = reserverd.get(t.value, 'ID')
    return t

# Floating literal
def t_FLOAT(t):
    r'(-)?\d+\.\d+'
    t.value = float(t.value)
    return t

# Integer literal
def t_INT(t):
    r'(-)?\d+'
    t.value = int(t.value)
    return t

 # Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lex.lex()
if __name__ == "__main__":
    lex.runmain()