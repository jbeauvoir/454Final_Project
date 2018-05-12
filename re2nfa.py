# Final Project CS 454
# Converting Regular Expressions to an NFA then running a string to test if it is
# a part of the language made by the RE

# Group: Michael Schmidt, Catherine Meyer, Jacques Beauvoir


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
        self.accept = A + B + 1

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


def testString(nonE_NFA, str, map):
    states = [0]
    for i in str:
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


def createNFAmulitpleOf3():
    m = {'0': 0, '1': 1}
    bNFA = NFA()
    bNFA.baseNFA('0', m)

    temp = NFA()
    temp.baseNFA('0', m)

    bNFA.union(temp)
    bNFA.star()

    temp = NFA()
    temp.baseNFA('0',m)
    temp2 = NFA()
    temp2.baseNFA('1',m)
    temp2.star()
    temp.concatenate(temp2)
    temp.concatenate(bNFA)
    bNFA = NFA()
    bNFA.baseNFA('0', m)
    temp.concatenate(bNFA)
    temp.star()

    bNFA = NFA()
    bNFA.baseNFA('1', m)
    bNFA.concatenate(temp)
    temp = NFA()
    temp.baseNFA('1', m)
    bNFA.concatenate(temp)
    bNFA.star()

    finalNFA = NFA()
    finalNFA.baseNFA('0', m)
    finalNFA.union(bNFA)
    finalNFA.star()

    return finalNFA


def readInput(str, i):
    m = {'0': 0, '1': 1}
    if str[i] == '(' and i != 0:
        return readInput(str, i+1)
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
        startNFA, i = readInput(str, i+1)
        if i < len(str):
            if str[i] == '*':
                startNFA.star()
                i = i + 1
    while i < len(str):
        if str[i] == '(':
            tempNFA, i = readInput(str, i+1)
            if i < len(str):
                if str[i] == '*':
                    tempNFA.star()
            startNFA.concatenate(tempNFA)
        elif str[i] == '+':
            tempNFA, i = readInput(str, i+1)
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


def main():
    m = {'0': 0, '1': 1}
    multi3NFA = createNFAmulitpleOf3()
    multi3NFA.removeEpsilon()

    regEx = input("Enter a regular expression: ")
    myNFA, i = readInput(regEx, 0)
    myNFA.removeEpsilon()

    testStr = input("Enter string to test:")

    if testString(myNFA, testStr, m):
        print("This string is accepted")
    else:
        print("This string is rejected")

    return 0

main()
