# Author: Johnathan Picek
# Term Project - Smart Thermostat Language Prototype
# STPLexer.py
# CPSC 46000-003 - Programming Languages
# Professor Dr. Eric Chou

# lexer definitions
# just a slightly modified version of calclex.py
# and test output if run as __main__

import ply.lex as lex

tokens = (
    'ID',
    'COMMAND',
    'TARGET',
    'NUMBER',
)

keywords = {
    'ALL'       : 'TARGET',
    'NOW'       : 'TARGET',
    'SLEEP'     : 'TARGET',
    'WAKE'      : 'TARGET',
    'AWAY'      : 'TARGET',
    'HOME'      : 'TARGET',

    'BOUNDARY'  : 'COMMAND',
    'SET'       : 'COMMAND',
    'CLEAR'     : 'COMMAND',

    '_SYSPROPS' : 'COMMAND',
    '_SCHED'    : 'COMMAND',

    'SAFETY_TEMP_MIN' : 'NUMBER',
    'SAFETY_TEMP_MAX' : 'NUMBER',
}

## LEXER ##
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    # assign t.type to keyword dict value if exists
    # otherwise, t.type remains 'ID'
    t.type = keywords.get(t.value,'ID')    # Check for reserved words
    if t.type == 'ID':
        print(t.value, " not a valid command.")
        t.lexer.skip(1)
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

data = '''SET SLEEP 68
        SET NOW 72
        BOUNDARY 0 6
        BOUNDARY 3 22
        _SYSPROPS
        _SCHED
        CLEAR'''

lexer = lex.lex()
lexer.input(data)

if __name__ == "__main__":
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)