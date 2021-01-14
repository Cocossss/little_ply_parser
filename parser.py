import ply.yacc as yacc
from lexer import tokens
from print_ast import print_ast
import sys


assis = {}

def p_prog(p):
    '''prog : functions'''
    p[0] = p[1]

def p_functions(p):
    '''functions : functions function
                | function'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_function(p):
    '''function : ID LPAREN args RPAREN LBR instructions RBR'''
    p[0] = ['func', p[1], p[3], p[6]]
    assis.clear()

def p_args(p):
    '''args : expr
            | args COMMA ID
            | args COMMA expr
            | '''

    if len(p) == 1:
        p[0] = []
    elif len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[0] = p[1] + [p[3]]

def p_instructions(p):
    '''instructions : instructions instruction SEP
                    | instruction SEP
                    | '''
    if len(p) == 3:
        if 'opt' in p[1]:
            p[1].remove('opt')
            p[0] = p[1]
        else:
            p[0] = [p[1]]
    elif len(p) == 4:
        if 'opt' in p[2]:
            p[2].remove('opt')
            p[0] = p[1] + p[2]
        else:
            p[0] = p[1] + [p[2]]
    else:
        p[0] = []


def p_instruction(p):
    '''instruction : assi
                    | return
                    | while
                    | if'''
    p[0] = p[1]

def p_assi(p):
    '''assi : ID ASSIGN expr'''
    p[0] = ['assignment', p[1], p[3]]
    val = None
    if isinstance(p[3], list):
        if p[3][0] == 'bin_op':
            val = p[3][4]
        elif p[3][0] == 'un_op':
            val = p[3][3]
    elif isinstance(p[3], int):
        val = p[3]
    elif isinstance(p[3], str):
        val = None
    assis[p[1]] = val

def p_return(p):
    '''return : RETURN expr'''
    p[0] = ['return', p[2]]

def p_while(p):
    '''while : WHILE expr LBR instructions RBR'''
    p[0] = ['while', p[2], p[4]]

def p_if(p):
    '''if : IF expr THEN LBR instructions RBR ELSE LBR instructions RBR'''
    p[0] = ['if', p[2], p[5], p[9]]
    val = None
    if isinstance(p[2], list):
        if p[2][0] == 'bin_op':
            val = p[2][4]
        elif p[2][0] == 'un_op':
            val = p[2][3]
    elif isinstance(p[2], int):
        val = p[2]
    if val != None:
        if val != 0:
            p[0] = p[5] + ['opt']
        elif val == 0:
            p[0] = p[9] + ['opt']




def p_expr(p):
    '''expr : term1 OR expr
            | term1'''
    if len(p) == 4:
        val = None
        left = None
        right = None
        if isinstance(p[1], list):
            if p[1][0] == 'bin_op':
                left = p[1][4]
            elif p[1][0] == 'un_op':
                left = p[1][3]
        elif isinstance(p[1], int):
            left = p[1]
        elif isinstance(p[1], str):
            if p[1] in assis:
                left = assis[p[1]]
        if isinstance(p[3], list):
            if p[3][0] == 'bin_op':
                right = p[3][4]
            elif p[3][0] == 'un_op':
                right = p[3][3]
        elif isinstance(p[3], int):
            right = p[3]
        elif isinstance(p[3], str):
            if p[3] in assis:
                right = assis[p[3]]

        if isinstance(left, int) and isinstance(right, int):
            val = left or right
        p[0] = ['bin_op', p[2], p[1], p[3], val] #'(' + str(p[1]) + str(p[2]) + str(p[3]) + ')'
    else:
        p[0] = p[1] #str(p[1])

def p_term1(p):
    '''term1 : term2 AND term1
            | term2'''
    if len(p) == 4:
        val = None
        left = None
        right = None
        if isinstance(p[1], list):
            if p[1][0] == 'bin_op':
                left = p[1][4]
            elif p[1][0] == 'un_op':
                left = p[1][3]
        elif isinstance(p[1], int):
            left = p[1]
        elif isinstance(p[1], str):
            if p[1] in assis:
                left = assis[p[1]]

        if isinstance(p[3], list):
            if p[3][0] == 'bin_op':
                right = p[3][4]
            elif p[3][0] == 'un_op':
                right = p[3][3]
        elif isinstance(p[3], int):
            right = p[3]
        elif isinstance(p[3], str):
            if p[3] in assis:
                right = assis[p[3]]

        if isinstance(left, int) and isinstance(right, int):
            val = left and right
        p[0] = ['bin_op', p[2], p[1], p[3], val] #'(' + str(p[1]) + str(p[2]) + str(p[3]) + ')'
    else:
        p[0] = p[1] #str(p[1])

def p_term2(p):
    '''term2 : NEG term2
            | term3'''
    if len(p) == 3:
        val = None
        if isinstance(p[2], list):
            if p[2][0] == 'bin_op':
                if p[2][4] != None:
                    val = not (p[2][4])
            elif p[2][0] == 'un_op':
                if p[2][3] != None:
                    val = not (p[2][3])
        elif isinstance(p[2], int):
            val = not p[2]
        elif isinstance(p[2], str):
            if p[2] in assis:
                val = assis[p[2]]

        if val != None:
            if val == True:
                val = 1
            else:
                val = 0
        p[0] = ['un_op', p[1], p[2], val] #'(' + str(p[1]) + str(p[2]) + ')'
    else:
        p[0] = p[1] #str(p[1])

def p_term3(p):
    '''term3 : term4 EQ term4
            | term4 NEQ term4
            | term4 LT term4
            | term4 BT term4
            | term4 LTE term4
            | term4 BTE term4
            | term4'''
    if len(p) == 4:
        val = None
        left = None
        right = None
        if isinstance(p[1], list):
            if p[1][0] == 'bin_op':
                left = p[1][4]
            elif p[1][0] == 'un_op':
                left = p[1][3]
        elif isinstance(p[1], int):
            left = p[1]
        elif isinstance(p[1], str):
            if p[1] in assis:
                left = assis[p[1]]

        if isinstance(p[3], list):
            if p[3][0] == 'bin_op':
                right = p[3][4]
            elif p[3][0] == 'un_op':
                right = p[3][3]
        elif isinstance(p[3], int):
            right = p[3]
        elif isinstance(p[3], str):
            if p[3] in assis:
                right = assis[p[3]]

        same = 0;
        if p[1] == p[3] and isinstance(p[1], str) and isinstance(p[3], str):
            same = 1;

        if p[2] == '==' and isinstance(left, int) and isinstance(right, int):
            val = left == right
            if same == 1:
                val = True
        elif p[2] == '/=' and isinstance(left, int) and isinstance(right, int):
            val = left != right
            if same == 1:
                val = False
        elif p[2] == '<' and isinstance(left, int) and isinstance(right, int):
            val = left < right
        elif p[2] == '<=' and isinstance(left, int) and isinstance(right, int):
            val = left <= right
            if same == 1:
                val = True
        elif p[2] == '>' and isinstance(left, int) and isinstance(right, int):
            val = left > right
        elif p[2] == '>=' and isinstance(left, int) and isinstance(right, int):
            val = left >= right
            if same == 1:
                val = True

        if val != None:
            if val == True:
                val = 1
            else:
                val = 0
        p[0] = ['bin_op', p[2], p[1], p[3], val] #'(' + str(p[1]) + str(p[2]) + str(p[3]) + ')'
    else:
        p[0] = p[1] #str(p[1])


def p_term4(p):
    '''term4 : term4 PLUS term5
            | term4 MINUS term5
            | term5'''
    if len(p) == 4:
        val = None
        left = None
        right = None
        if isinstance(p[1], list):
            if p[1][0] == 'bin_op':
                left = p[1][4]
            elif p[1][0] == 'un_op':
                left = p[1][3]
        elif isinstance(p[1], int):
            left = p[1]
        elif isinstance(p[1], str):
            if p[1] in assis:
                left = assis[p[1]]
        if isinstance(p[3], list):
            if p[3][0] == 'bin_op':
                right = p[3][4]
            elif p[3][0] == 'un_op':
                right = p[3][3]
        elif isinstance(p[3], int):
            right = p[3]
        elif isinstance(p[3], str):
            if p[3] in assis:
                right = assis[p[3]]

        if p[2] == '+' and isinstance(left, int) and isinstance(right, int):
            val = left + right
        elif p[2] == '-' and isinstance(left, int) and isinstance(right, int):
            val = left - right
        p[0] = ['bin_op', p[2], p[1], p[3], val] #'(' + str(p[1]) + str(p[2]) + str(p[3]) + ')'
        #print('p[1]: ', p[1], 'p[3]: ', p[3], 'val: ', val)
    else:
        p[0] = p[1] #str(p[1])
def p_term5(p):
    '''term5 : term5 MULTI term6
            | term5 DIVIDE term6
            | term6'''
    if len(p) == 4:
        val = None
        left = None
        right = None
        if isinstance(p[1], list):
            if p[1][0] == 'bin_op':
                left = p[1][4]
            elif p[1][0] == 'un_op':
                left = p[1][3]
        elif isinstance(p[1], int):
            left = p[1]
        elif isinstance(p[1], str):
            if p[1] in assis:
                left = assis[p[1]]
        if isinstance(p[3], list):
            if p[3][0] == 'bin_op':
                right = p[3][4]
            elif p[3][0] == 'un_op':
                right = p[3][3]
        elif isinstance(p[3], int):
            right = p[3]
        elif isinstance(p[3], str):
            if p[3] in assis:
                right = assis[p[3]]

        if p[2] == '/' and isinstance(left, int) and isinstance(right, int):
            val = left // right

        elif p[2] == '*' and isinstance(left, int) and isinstance(right, int):
            val = left * right
        p[0] = ['bin_op', p[2], p[1], p[3], val] #'(' + str(p[1]) + str(p[2]) + str(p[3]) + ')'
    else:
        p[0] = p[1] #str(p[1])

def p_term6(p):
    '''term6 : term8 POW term6
            | term8'''
    if len(p) == 4:
        val = None
        left = None
        right = None
        if isinstance(p[1], list):
            if p[1][0] == 'bin_op':
                left = p[1][4]
            elif p[1][0] == 'un_op':
                left = p[1][3]
        elif isinstance(p[1], int):
            left = p[1]
        elif isinstance(p[1], str):
            if p[1] in assis:
                left = assis[p[1]]

        if isinstance(p[3], list):
            if p[3][0] == 'bin_op':
                right = p[3][4]
            elif p[3][0] == 'un_op':
                right = p[3][3]
        elif isinstance(p[3], int):
            right = p[3]
        elif isinstance(p[3], str):
            if p[3] in assis:
                right = assis[p[3]]

        if isinstance(left, int) and isinstance(right, int):
            val = left ** right
        p[0] = ['bin_op', 'POW', p[1], p[3], val] #'(' + str(p[1]) + str(p[2]) + str(p[3]) + ')'
    else:
        p[0] = p[1] #str(p[1])

#def p_term7(p):
#    '''term7 : MINUS term7
#            | term8'''
#    if len(p) == 3:
#        val = None
#        if isinstance(p[2], list):
#            if p[2][0] == 'bin_op':
#                val = -(p[2][4])
#            elif p[2][0] == 'un_op':
#                val = -(p[2][3])
#        elif isinstance(p[2], int):
#            val = -p[2]
#        elif isinstance(p[2], str):
#            if p[2] in assis:
#                val = assis[p[2]]
#        p[0] = ['un_op', 'MINUS', p[2], val] #'(' + str(p[1]) + str(p[2]) + ')'
#    else:
#        p[0] = p[1] #str(p[1])

def p_term8_num(p):
    '''term8 : NUMBER
            | ID'''
    p[0] = p[1] #str(p[1])

def p_term8_expr(p):
    '''term8 : LPAREN expr RPAREN'''
    p[0] = p[2] #str(p[2])

def p_term8_func(p):
    '''term8 : ID LPAREN args RPAREN'''
    p[0] = ['call_func', p[1], p[3]] #str(p[1]) + '(' + str(p[3]) + ')'


def p_error(p):
    print("Syntax error at:", p)
    raise Exception("Syntax error!")



if __name__ == "__main__":
    start = 'prog'
    yacc.yacc()


    var = sys.argv[1]
    print('opening file ', var, '...')
    try:
      f = open(var, "r")
    except IOError:
      print('Error: File does not appear to exist.')
      exit()
    data = f.read()
    f.close()



    try:
        result = yacc.parse(data)
    except Exception:
        exit()


    if result != None:
        print('prog:')

        f = open(var + '.out', 'w')
        f.write('prog:\n')
        print_ast(result, f)
        f.close
