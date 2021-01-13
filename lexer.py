import ply.lex as lex

# List of token names.   This is always required
tokens = (
    'ID',
   'NUMBER',
   'PLUS',
   'MINUS',
   'MULTI',
   'DIVIDE',
   'LPAREN',
   'RPAREN',
    'LBR',
    'RBR',
    'SEP',
    'OR',
    'AND',
    'NEG',
    'EQ',
    'NEQ',
    'LT',
    'BT',
    'LTE',
    'BTE',
    'POW',
    'ENDL',
    'IF',
    'ELSE',
    'THEN',
    'WHILE',
    'RETURN',
    'COMMA',
    'ASSIGN'
)
# Regular expression rules for simple tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_MULTI   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBR = r'\{'
t_RBR = r'\}'
t_SEP = r';'
t_OR = r'\|\|'
t_AND = r'&&'
t_NEG = r'\-\-'
t_EQ = r'\=\='
t_NEQ = r'/='
t_LT = r'<'
t_BT = r'>'
t_LTE = r'<='
t_BTE = r'>='
t_POW = r'\*\*'
t_IF = r'if'
t_WHILE = r'while'
t_ELSE = r'else'
t_THEN = r'then'
t_RETURN = r'return'
t_COMMA = r','
t_ASSIGN = r'='

keywords = {'if':'IF', 'while':'WHILE', 'return':'RETURN', 'else':'ELSE', 'then':'THEN'}

# A regular expression rule with some action code
def t_NUMBER(t):
    r'0|[1-9][0-9]*'
    try:
        t.value = int(t.value)
    except ValueError:
        print('Line %d: Number %s is too large!' % (t.lineno,t.value))
        t.value = 0
    return t

def t_ID(t):
    r'[a-z][a-zA-Z_0-9]*'
    if t.value in keywords:
        t.type = keywords.get(t.value)
    return t

# Define a rule so we can track line numbers
def t_ENDL(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])

# Build the lexer
lex.lex()

