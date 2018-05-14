# Final Project CS 454
# Converting Regular Expressions to an NFA then running a string to test if it is
# a part of the language made by the RE
# Group: Michael Schmidt, Catherine Meyer, Jacques Beauvoir
import sys
sys.path
import ply.lex as lex
import ply.yacc as yacc

class NFA(object):
    def __init__(self):
        self.start = 0
        self.accept = 0
        self.deltaArray = []
        self.EArray = []

    def baseNFA(self, char, m):
        # builds a basic NFA with two states and one transition
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
                exit(3)
            temp2.append(None)
        self.deltaArray.append(temp)
        self.deltaArray.append(temp2)

    def union(self, otherNFA):
        # takes two NFAs and takes the union of them and replace the caller NFA
        tempNFA = NFA()
        temp = []
        for i in range(len(self.deltaArray[0])):
            temp.append(None)
        tempNFA.deltaArray.append(temp)

        # copy the first NFA into the temporary one, making sure to add one
        # to all state transitions to compensate for the new stating state
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
        # copy all epsilons
        B = len(self.EArray)
        for i in range(B - 1):
            epsilons = []
            for k in range(len(self.EArray[i])):
                epsilons.append(self.EArray[i][k] + 1)
            tempNFA.EArray.append(epsilons)

        # adds a transition for the NEW epsilon array from the last state added from the
        # first NFA to the last state of this new NFA
        C = len(otherNFA.deltaArray)
        tempNFA.EArray.append([A + C + 1])

        # copy the other NFA to the temp making sure to add to the old transitions
        # the number of states in NFA1, plus an addition one. (This will be the new state)
        for i in range(C):
            trans = []
            for k in range(len(otherNFA.deltaArray[i])):
                if otherNFA.deltaArray[i][k] is not None:
                    trans.append(otherNFA.deltaArray[i][k] + A + 1)
                else:
                    trans.append(None)
            tempNFA.deltaArray.append(trans)

        # copy epsilons
        D = len(otherNFA.EArray)
        for i in range(D - 1):
            epsilons = []
            for k in range(len(otherNFA.EArray[i])):
                epsilons.append(otherNFA.EArray[i][k] + A + 1)
            tempNFA.EArray.append(epsilons)

        # adds a transition for the NEW epsilon array from the last state added from the
        # second NFA to the last state of this new NFA
        tempNFA.EArray.append([A + C + 1])

        # set the last state to have no transitions on epsilon or delta
        tempNFA.EArray.append([])
        temp = []
        for i in range(len(self.deltaArray[0])):
            temp.append(None)
        tempNFA.deltaArray.append(temp)

        # overwrite the first NFA with the NEW NFA created by the Union
        self.deltaArray = tempNFA.deltaArray
        self.EArray = tempNFA.EArray
        self.accept = A + C + 1

        return

    def concatenate(self, otherNFA):
        newNFA = NFA()
        A = len(self.deltaArray)
        B = len(otherNFA.deltaArray)
        # copy over the first NFA into tempNFA(newNFA)
        for i in range(A):
            newNFA.deltaArray.append(self.deltaArray[i])
            if i < A - 1:
                newNFA.EArray.append(self.EArray[i])
            else:
                newNFA.EArray.append(self.EArray[i])
                # adds epsilon transition at old finish state of first NFA
                newNFA.EArray[i].append(A)

        # copy over the second NFA into tempNFA, adding the number of states in A to
        # the transitions in B to keep transitions the same
        for i in range(B):
            temp = []
            for k in range(len(otherNFA.deltaArray[i])):
                if otherNFA.deltaArray[i][k] is not None:
                    temp.append(otherNFA.deltaArray[i][k] + A)
                else:
                    temp.append(None)
            newNFA.deltaArray.append(temp)
        # copy epsilon transitions
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
        # copy the NFA into the temporary one, making sure to add one
        # to all state transitions to compensate for the new stating state
        A = len(self.deltaArray)
        # adds epsilon trans to state 1, and final state from the starting state
        tempNFA.EArray.append([1, A+1])
        for i in range(A):
            trans = []
            for k in range(len(self.deltaArray[i])):
                if self.deltaArray[i][k] is not None:
                    trans.append(self.deltaArray[i][k] + 1)
                else:
                    trans.append(None)
            tempNFA.deltaArray.append(trans)
        # copy over all epsilon trans
        B = len(self.EArray)
        for i in range(B-1):
            epsilons = []
            for k in range(len(self.EArray[i])):
                epsilons.append(self.EArray[i][k] + 1)
            tempNFA.EArray.append(epsilons)
        # add epsilon trans from old accepting state of the NFA to state 1 and new accepting state
        tempNFA.EArray.append([1, A+1])
        tempNFA.EArray.append([])
        temp2 = list(temp)
        tempNFA.deltaArray.append(temp2)

        self.deltaArray = tempNFA.deltaArray
        self.EArray = tempNFA.EArray
        self.accept = A + 1

        return

    def removeEpsilon(self):
        # removes all epsilon transitions from the NFA and replaces them with new
        # delta transitions. This uses the the rule of removing epsilons where
        # at state Q if there is a epsilon trans to a state U and there is a transition
        # from U to K, add that transition from Q to K and remove the epsilon.
        if len(self.deltaArray) == 2:  # just in case RE is length one
            self.EArray = []
            self.accept = [self.accept]
            return
        queue = []
        i = 0
        while len(queue) == 0:
            if not len(self.EArray[i]) == 0:
                for k in range(len(self.EArray[i])):
                    queue.append([i, self.EArray[i][k]])
            i = i + 1
        visitedBase = []
        for i in range(len(self.deltaArray)):
            visitedBase.append(False)

        acceptList = []
        addTrans = self.findTransitions(queue, visitedBase, acceptList)
        reachedStates = self.addTransitions(addTrans)

        # This is used to check if a state has already been visited and transitions have
        # already been added. Is basically a list of True and False, with the index
        # corresponding to the state in the NFA
        finalVisit = visitedBase[:]
        while len(reachedStates) > 0:
            if finalVisit[reachedStates[0]]:
                reachedStates.pop(0)
            elif reachedStates[0] == self.accept:
                reachedStates.pop(0)
            else:
                i = 0
                while len(queue) == 0:
                    s = reachedStates[i]
                    if not len(self.EArray[s]) == 0:
                        for k in range(len(self.EArray[s])):
                            queue.append([s, self.EArray[s][k]])
                    i = i + 1
                    reachedStates.pop(0)
                addTrans = self.findTransitions(queue, visitedBase, acceptList)
                reachedStates = reachedStates + self.addTransitions(addTrans)
                finalVisit[s] = True
        acceptList.append(self.accept)
        self.EArray = []
        self.accept = acceptList
        return

    def findTransitions(self, queue, visitedBase, acceptList):
        # finds all states (that don't have epsilon) that can be reach by purely epsilon
        # transitions from a give state.
        # this will then return a list of pairs that consist of
        # [given state, state that is reach by epsilon], this list is then passed to another
        # function (addTransitions)
        visited = visitedBase[:]
        addTrans = []
        state = queue[0][0]
        visited[state] = True
        while len(queue) > 0:
            eTran = queue[0][1]
            numE = len(self.EArray[eTran])
            if visited[eTran]:
                queue.pop(0)
            elif numE > 0:
                for i in range(len(self.EArray[eTran])):
                    epsilonTrans = [state, self.EArray[eTran][i]]
                    queue.append(epsilonTrans)
                queue.pop(0)
            elif eTran == self.accept:
                acceptList.append(state)
                queue.pop(0)
            else:
                addTrans.append(queue.pop(0))
            visited[eTran] = True
        return addTrans

    def addTransitions(self, addTrans):
        # copies all transitions from from the state reached by epsilon to the given state
        newDelta = self.deltaArray
        reachedStates = []
        while len(addTrans) > 0:
            state = addTrans[0][0]
            eTran = addTrans[0][1]
            for i in range(len(self.deltaArray[eTran])):
                if newDelta[state][i] is not None and self.deltaArray[eTran][i] is not None:
                    if isinstance(newDelta[state][i], int):
                        temp = [newDelta[state][i], self.deltaArray[eTran][i]]
                        newDelta[state][i] = temp
                    else:
                        newDelta[state][i].append(self.deltaArray[eTran][i])
                    reachedStates.append(self.deltaArray[eTran][i])
                elif self.deltaArray[eTran][i] is not None:
                    newDelta[state][i] = self.deltaArray[eTran][i]
                    reachedStates.append(self.deltaArray[eTran][i])

            addTrans.pop(0)
        return reachedStates


def testString(nonE_NFA, inputStr, map):
    states = [0]
    for i in inputStr:
        if i in map:
            transition = map[i]
        else:
            return False
        numStates = len(states)
        for j in range(numStates):
            if states[j] != -1:
                if isinstance(nonE_NFA.deltaArray[states[j]][transition], int):
                    states[j] = nonE_NFA.deltaArray[states[j]][transition]
                elif nonE_NFA.deltaArray[states[j]][transition] is not None:
                    numTrans = len(nonE_NFA.deltaArray[states[j]][transition])
                    temp = nonE_NFA.deltaArray[states[j]][transition]
                    states[j] = temp[0]
                    for k in range(1, numTrans):
                        state = temp[k]
                        states.append(state)
                else:
                    states[j] = -1
    for i in states:
        for j in nonE_NFA.accept:
            if i == j:
                return True


def readInput(str, i, m):
    if str[i] == '(' and i != 0:
        return readInput(str, i+1, m)
    elif str[i] == '+' or str[i] == ')':
        exit(2)
    elif str[i] != '(':
        startNFA = NFA()
        startNFA.baseNFA(str[i], m)
        i = i + 1
        if i < len(str):
            if str[i] == '*':
                startNFA.star()
                i = i + 1
    else:
        startNFA, i = readInput(str, i+1, m)
        if i < len(str):
            if str[i] == '*':
                startNFA.star()
                i = i + 1
    while i < len(str):
        if str[i] == '(':
            tempNFA, i = readInput(str, i+1, m)
            if i < len(str):
                if str[i] == '*':
                    tempNFA.star()
            startNFA.concatenate(tempNFA)
        elif str[i] == '+':
            tempNFA, i = readInput(str, i+1, m)
            startNFA.union(tempNFA)
            if str[i - 1] == ')':
                return startNFA, i
        elif str[i] == ')':
            return startNFA, (i+1)
        else:
            tempNFA = NFA()
            tempNFA.baseNFA(str[i], m)
            if i+1 < len(str):
                if str[i+1] == '*':
                    tempNFA.star()
                    i = i + 1
            startNFA.concatenate(tempNFA)
        i = i + 1
    return startNFA, i


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
    answerNFA.removeEpsilon()
    while True:
        try: 
            testStr = input('\nEnter a string to test or hit \'command-D\' to enter a new RE\n ')
            if testString(answerNFA, testStr, m):
                print("This string is accepted")
            else:
                print("This string is rejected")
        except EOFError:
            break

    
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
    m = {}
    for letter in str(RE):
        if letter not in (' ', '(', ')', '*', '+', '\'', ','):
            m[letter] = 0
            count = 0
            for key in m:
                m[key] = count                
                count += 1
    print(m)
    return m


# Call parser (not in a function))
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
    print("Please type in a regular expression for processing. The alphabet is [a-zA-Z0-9]. \nUse 'control-D' to exit the program.")
    while True:
        try: 
            RE = input('\n>> ')
            parser.parse(RE)
        except EOFError:
            break

main()
