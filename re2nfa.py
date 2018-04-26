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
            if m[i][0] == char:
                temp.append(1)
            else:
                temp.append(None)
            temp2.append(None)
        self.deltaArray.append(temp)
        self.deltaArray.append(temp2)

    def union(self, otherNFA):
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
            newNFA.EArray.append(otherNFA.EArray[i])
        self.deltaArray = newNFA.deltaArray
        self.EArray = newNFA.EArray
        self.accept = A+B

    def star(self):
        return


def main():

    m = [['0', 0], ['1', 1]]
    nfa1 = NFA()
    nfa1.baseNFA('1', m)

    nfa2 = NFA()
    nfa2.baseNFA('0', m)
    nfa1.concatenate(nfa2)

    return 0








main()
