import sys
sys.path.append("/home/student/jbeauvoir/classes/cs454/p3/454Final_Project/ply")
import ply.lex as lex
import ply.yacc as yacc
from collections import OrderedDict

class NFA(object):
    def __init__(self):
        self.start = 0
        self.accept = 0
        self.deltaArray = []
        self.EArray = []

    def baseNFA(self, char, m):
        self.accept = 1
        self.EArray = [[], []]
        temp = []
        temp2 = []

        for i in range(len(m)):
            if char in m:
                if m[char] == i:
                    temp.append(1)
                else:
                    temp.append(None)
            else:
                exit(2)
            temp2.append(None)

        self.deltaArray.append(temp)
        self.deltaArray.append(temp2)

    def union(self, otherNFA):
        tempNFA = NFA()
        temp = []
        for i in range(len(self.deltaArray[0])):
            temp.append(None)
        tempNFA.deltaArray.append(temp)

        A = len(self.deltaArray)
        tempNFA.EArray.append([1, A + 1])
        for i in range(A):
            trans = []
            for k in range(len(self.deltaArray[i])):
                if self.deltaArray[i][k] is not None:
                    trans.append(self.deltaArray[i][k] + 1)
                else:
                    trans.append(None)
            tempNFA.deltaArray.append(trans)
        B = len(self.EArray)
        for i in range(B - 1):
            epsilons = []
            for k in range(len(self.EArray[i])):
                epsilons.append(self.EArray[i][k] + 1)
            tempNFA.EArray.append(epsilons)

        C = len(otherNFA.deltaArray)
        tempNFA.EArray.append([A + C + 1])
        for i in range(C):
            trans = []
            for k in range(len(otherNFA.deltaArray[i])):
                if otherNFA.deltaArray[i][k] is not None:
                    trans.append(otherNFA.deltaArray[i][k] + A + 1)
                else:
                    trans.append(None)
            tempNFA.deltaArray.append(trans)
        D = len(otherNFA.EArray)
        for i in range(D - 1):
            epsilons = []
            for k in range(len(otherNFA.EArray[i])):
                epsilons.append(otherNFA.EArray[i][k] + A + 1)
            tempNFA.EArray.append(epsilons)

        tempNFA.EArray.append([A + C + 1])
        tempNFA.EArray.append([])
        temp = []
        for i in range(len(self.deltaArray[0])):
            temp.append(None)
        tempNFA.deltaArray.append(temp)

        self.deltaArray = tempNFA.deltaArray
        self.EArray = tempNFA.EArray
        self.accept = A + B + 1

        return

    def concatenate(self, otherNFA):
        newNFA = NFA()
        A = len(self.deltaArray)
        B = len(otherNFA.deltaArray)
        for i in range(A):
            newNFA.deltaArray.append(self.deltaArray[i])
            if i < A - 1:
                newNFA.EArray.append(self.EArray[i])
            else:
                newNFA.EArray.append(self.EArray[i])
                newNFA.EArray[i].append(A)
        for i in range(B):
            temp = []
            for k in range(len(otherNFA.deltaArray[i])):
                if otherNFA.deltaArray[i][k] is not None:
                    temp.append(otherNFA.deltaArray[i][k] + A)
                else:
                    temp.append(None)
            newNFA.deltaArray.append(temp)

        C = len(otherNFA.EArray)
        for i in range(C):
            epsilons = []
            for k in range(len(otherNFA.EArray[i])):
                epsilons.append(otherNFA.EArray[i][k] + A)
            newNFA.EArray.append(epsilons)

        self.deltaArray = newNFA.deltaArray
        self.EArray = newNFA.EArray
        self.accept = A+B - 1

    def star(self):
        tempNFA = NFA()
        temp = []
        for i in range(len(self.deltaArray[0])):
            temp.append(None)
        tempNFA.deltaArray.append(temp)
        A = len(self.deltaArray)
        tempNFA.EArray.append([1, A+1])
        for i in range(A):
            trans = []
            for k in range(len(self.deltaArray[i])):
                if self.deltaArray[i][k] is not None:
                    trans.append(self.deltaArray[i][k] + 1)
                else:
                    trans.append(None)
            tempNFA.deltaArray.append(trans)
        B = len(self.EArray)
        for i in range(B-1):
            epsilons = []
            for k in range(len(self.EArray[i])):
                epsilons.append(self.EArray[i][k] + 1)
            tempNFA.EArray.append(epsilons)
        tempNFA.EArray.append([1, A+1])
        tempNFA.EArray.append([])
        temp2 = list(temp)
        tempNFA.deltaArray.append(temp2)

        self.deltaArray = tempNFA.deltaArray
        self.EArray = tempNFA.EArray
        self.accept = A + 1

        return

'************************* END NFA CODE *****************************'

# List of tokens to be used
tokens = [
    
    'SYMBOL',
    'L_PAREN',
    'R_PAREN',
    'UNION',
    'KLEENE'

]


# t_ tells lexer what the token actually looks like
# ordered in precedence 

t_L_PAREN = r'\('
t_R_PAREN = r'\)'
t_KLEENE = r'\*'
t_UNION = r'\+'

t_ignore = r' '

# Dictates what a valid symbol can be,
# which is any up/lower letter and digits
# 0 to 9
def t_SYMBOL(t):
    
    r'[a-zA-Z0-9]'
    t.type = 'SYMBOL'
    return t

def t_error(t):
    print("Illegal character")
    t.lexer.skip(1)
    


# Create the Lexer
lexer = lex.lex()

'********************* PARSER **************************'

# Sets up precedence 
precedence = (

    ('left', 'UNION'),
    ('left', 'KLEENE')
)


def p_regex(p): 

    '''
    regex : expression 
          | empty
    '''
    m = dictCreator(p[1])
    mainNFA = NFA()
    answer = run(p[1],mainNFA, m)
    answerNFA = answer[1]
    print(str(answerNFA.deltaArray))

def p_expression_kleene(p):
    '''
    expression : expression KLEENE
    '''
    p[0] = (p[2], p[1])
    
def p_expression_expression(p):
    '''
    expression : expression expression
    '''
    p[0] = (p[1], p[2])

def p_LRparen(p):
    '''
    expression : L_PAREN expression R_PAREN       
    '''
    p[0] = p[2] 

def p_expression_union_concat(p):
    '''
    expression : expression UNION expression
               
    '''
    p[0] = (p[2], p[1], p[3])

def p_expression_symbol(p):
    '''
    expression : SYMBOL
    '''
    p[0] = p[1]

def p_error(p):
    print("Syntax error found!")
    
def p_empty(p):
    '''
    empty :
    '''
    p[0] = None 

'******************************************************'

def dictCreator(RE):
    # Regular Expression Parser Loop
    transitionDict = {}
    for letter in str(RE):
        if letter not in (' ', '(', ')', '*', '+', '\'', ','):
            transitionDict[letter] = 0
            # Regular order was not supported so I imported a library
            # and casted it to a diciotnary type.
            
            #transitionDict = dict(OrderedDict(sorted(transitionDict.items())))

            # In order to iterate through the dictionary and change values
            # a new copy must be made.
            transitionFinal = {}
            count = 0
            for key in transitionDict:
                transitionFinal[key] = count                
                #print(key, count)
                count += 1
            m = transitionFinal
    print(m)
    return m  


# Call parser
parser = yacc.yacc()


# nfa creation will occur in the base case
def run(p, nfa, m):
    
    if type(p) == tuple:
        # Union Check 
        if p[0] == '+':
            lhs = run(p[1],nfa,m)
            rhs = run(p[2],nfa,m)
            lhsNFA = lhs[1]
            rhsNFA = rhs[1]
            lhsNFA.union(rhsNFA)
            return (p, lhsNFA)
        # Kleene Star Check
        if p[0] == '*':
            inString = run(p[1],nfa,m)
            stringNFA = inString[1] 
            stringNFA.star()
            return (p, stringNFA, m)
        # Concatenation
        else:
            lhs = run(p[0],nfa,m)
            rhs = run(p[1],nfa,m)
            lhsNFA = lhs[1]
            rhsNFA = rhs[1]
            lhsNFA.concatenate(rhsNFA)
            return (p, lhsNFA, m)   
    else:
        tempNFA = NFA()
        tempNFA.baseNFA(p,m)
        return(p, tempNFA, m)

    return (p,nfa,m)


def main():

    print("Welcome!")
    print("Please type in a regular expression for processing. The alphabet is [a-zA-Z0-9].")
    while True:
        try: 
            RE = input('\n>> ')
            parser.parse(RE)
        except EOFError:
            break

main()
