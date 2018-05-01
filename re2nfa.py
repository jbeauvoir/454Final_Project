import sys
from collections import OrderedDict

def main():



        #RE = 'C(Z) B 2 A 344'
        RE = input("Type a regular expression: ")
        

        # Regular Expression Parser Loop
        transitionDict = {}
        for x in RE:
            if x not in (' ', '(', ')', '*', '+'):
                    transitionDict[x] = 0    

        # Regular order was not supported so I imported a library
        # and casted it to a diciotnary type.
        transitionDict = dict(OrderedDict(sorted(transitionDict.items())))

        # In order to iterate through the dictionary and change values
        # a new copy must be made.
        transitionFinal = {}
        count = 0
        for key in transitionDict:
                transitionFinal[key] = count                
                print(key, count)
                count += 1

        print("Final table is: ")
        print(transitionFinal)

        

main()

