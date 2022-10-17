#python3 Sudoku1Red.py puzzles_1_standard_easy.txt
#python3 Sudoku1Red.py puzzles_2_variety_easy.txt

import sys

with open(sys.argv[1]) as f:
    puzzles = [line.strip() for line in f]

def setupPuzzle(p):
    global N, subblock_height, subblock_width, symbol_set
    symbols = "123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    N = int(len(p)**0.5)
    if(N==(int(N**0.5))**2):
        subblock_height = int(N**0.5) 
        subblock_width = int(N**0.5)
    else:
        f = int(N**0.5)
        while(N%f!=0):
            f-=1
        subblock_height = f
        f = int(N**0.5+1)
        while(N%f!=0):
            f+=1
        subblock_width = f
    symbol_set = list(symbols[:N])
    #print(N, subblock_height, subblock_width)

def printPuzzle(p):
    for i in range(0,len(p),N):
        print(" ".join(p[i:i+N]))


def makeC(p):
    global cSet, cDict
    l = [p[x:x+N] for x in range(0,len(p),N)]
    cSet = []
    # for i in range(0,N): #rows
    #     cSet.append(set([(N*i + l[i].index(x)) for x in l[i]])) # if x!='.'
    # for i in range(0,N): #col
    #     temp = [x[i] for x in l]
    #     #cSet.append(set([x for x in temp if x!='.'])) 
    #     cSet.append(set([i + N*j for j in range(0,len(temp))])) #if temp[j]!='.'

    for i in range(0,N): #rows
        temp = []
        for j in range (0,N):
            temp.append(N*i + j)
        cSet.append(set(temp))
    for i in range(0,N): #col
        temp = []
        for j in range(0,N):
            temp.append(i + N*j)
        cSet.append(set(temp))

    # l2 = [[] for i in range(len(l))] #holds the subblocks
    # count=0
    # for i in range(0,subblock_height):
    #     for i1 in range(i,len(l),subblock_height):
    #         for i2 in range(0,len(l),subblock_width):
    #             l2[count]+=l[i1][i2:i2+subblock_width]
    #             count+=1
    #     count=0
    l3 = [[] for i in range(len(l))] #holds the subblocks
    count=0
    for i in range(0,subblock_height):
        for i1 in range(i,len(l),subblock_height):
            for i2 in range(0,len(l),subblock_width):
                l3[count]+= [N*i1 + x for x in range(i2,i2+subblock_width)]
                count+=1
        count=0
    # for i in range (0,len(l2)):
    #     temp = []
    #     for j in range (0,len(l2[0])):
    #         if(l2[i][j]!='.'):
    #             temp.append(l3[i][j])
    #     cSet.append(set(temp))
    for i in l3:
        cSet.append(i)
    #print(cSet)
    #----------------------------#
    cDict = {x:set() for x in range(0,N**2)} #neighbors
    for i in cDict.keys():
        for j in cSet:
            if i in j:
                temp = {x for x in j}
                temp.remove(i)
                cDict[i] |= temp
    #print(cDict)

def symbInstances(p):
    for i in symbol_set:
        print(str(i) + ": " + str(p.count(i)))

def get_sorted_values(p,ind):
    temp = []
    for i in cDict[ind]:
        temp.append(p[i])
    return [x for x in symbol_set if x not in temp]


def sud_backtrack(p):
    if '.' not in p: return p
    var = p.index('.')
    for val in get_sorted_values(p,var):
        new_state = p[0:var] + val + p[var+1:]
        result = sud_backtrack(new_state)
        if result is not None:
            return result
    return None

def solve(p):
    setupPuzzle(p)
    makeC(p)
    ans = sud_backtrack(p)
    print(ans)

# print(puzzles[0])
# solve(puzzles[0])
# setupPuzzle(puzzles[0])
# printPuzzle(puzzles[0])
# makeC(puzzles[0])

for i in puzzles:
    #setupPuzzle(i)
    solve(i)


