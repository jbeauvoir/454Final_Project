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
                    trans.append(otherNFA.deltaArray[i][k] + A)
                else:
                    trans.append(None)
            tempNFA.deltaArray.append(trans)
        D = len(otherNFA.EArray)
        for i in range(D - 1):
            epsilons = []
            for k in range(len(otherNFA.EArray[i])):
                epsilons.append(otherNFA.EArray[i][k] + A)
            tempNFA.EArray.append(epsilons)

        tempNFA.EArray.append([A + B + 1])
        tempNFA.EArray.append([])
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
                    temp.append(otherNFA.deltaArray[i][k]+A)
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
        tempNFA.deltaArray.append(temp)

        self.deltaArray = tempNFA.deltaArray
        self.EArray = tempNFA.EArray
        self.accept = A + 1
        
        return

    def removeEpsilon(self):
        # work in progress, overwrite whole transition []
        queue = []
        A = len(self.EArray)
        for i in range(A):
            if not len(self.EArray[i]) == 0:
                for k in range(len(self.EArray[i])):
                    queue.append([i, self.EArray[i][k]])
        newDelta = list(self.deltaArray)  # copy
        while len(queue) > 0:
            state = queue[0][0]
            eTran = queue[0][1]
            numE = len(self.EArray[eTran])
            if numE > 0:
                for i in range(len(self.EArray[eTran])):
                    queue.append([state, self.EArray[eTran][i]])
            elif not eTran == self.accept:
                newDelta[state] = self.deltaArray[eTran]
            queue.pop(0)

        return



def main():

    m = {'0': 0, '1': 1}
    nfa1 = NFA()
    nfa1.baseNFA('1', m)

    nfa2 = NFA()
    nfa2.baseNFA('0', m)

    nfa1.union(nfa2)

    #nfa1.concatenate(nfa2)

    #nfa1.star()
    #nfa1.concatenate(nfa2)

   # nfa1.removeEpsilon()

    return 0








main()
