class NFA:
    start = 0
    accept = 0
    deltaArray = []
    EArray = []

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
        return

    def star(self):
        return


def main():

    m = [['0', 0], ['1', 1]]
    nfa1 = NFA()
    nfa1.baseNFA('1', m)

    return 0








main()
