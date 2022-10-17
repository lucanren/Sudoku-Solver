

#python3 Sudoku2Red.py puzzles_1_standard_easy.txt
#python3 Sudoku2Red.py puzzles_2_variety_easy.txt
#python3 Sudoku2Red.py puzzles_3_standard_medium.txt
#python3 Sudoku2Red.py puzzles_4_variety_medium.txt
#python3 Sudoku2Red.py puzzles_5_standard_hard.txt
#python3 Sudoku2Red.py puzzles_6_variety_hard.txt
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

def printPuzzle(p):
    for i in range(0,len(p),N):
        print(" ".join(p[i:i+N]))

def makeC(p):
    global cSet, cDict
    l = [p[x:x+N] for x in range(0,len(p),N)]
    cSet = []
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
    l3 = [[] for i in range(len(l))] #holds the subblocks
    count=0
    for i in range(0,subblock_height):
        for i1 in range(i,len(l),subblock_height):
            for i2 in range(0,len(l),subblock_width):
                l3[count]+= [N*i1 + x for x in range(i2,i2+subblock_width)]
                count+=1
        count=0
    for i in l3:
        cSet.append(i)
    cDict = {x:set() for x in range(0,N**2)} #neighbors
    for i in cDict.keys():
        for j in cSet:
            if i in j:
                temp = {x for x in j}
                temp.remove(i)
                cDict[i] |= temp

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

################

def setupPuzzle2(p):
    p2 = {x:"" for x in range(0,N**2)}
    for i in range (0,len(p)):
        if p[i] == ".":
            p2[i]+= "".join(symbol_set)
        else:
            p2[i]+=p[i]
    return p2

def forward_looking(p): 
    solved_ind = [x for x in p.keys() if len(p[x])==1]
    while len(solved_ind)!=0:
        i = solved_ind.pop()
        val = p[i]
        neighbors = cDict[i]
        for j in neighbors:
            if val in p[j]:
                p[j] = p[j].replace(val,"")
                if(len(p[j])==1):
                    solved_ind.append(j)
                if len(p[j])==0:
                    return None
    return p
            
def most_constrained(p):
    lst = [(x,len(p[x])) for x in p.keys()]
    lst.sort(key=lambda y:y[1])
    for i in lst:
        if i[1]!=1:
            return i[0]
    return None


def sud_back_fl(p):
    var = most_constrained(p)
    if var is None: return p
    for val in get_sorted_values(p,var):
        new_p = {a:p[a] for a in p.keys()}
        new_p[var] = val
        checked_p = forward_looking(new_p)
        if checked_p is not None:
            result = sud_back_fl(checked_p)
            if result is not None:
                return result
    return None

def c_prop(p):
    bool = False
    for grp in cSet:
        for val in symbol_set:
            count = 0
            temp = []
            for i in grp:
                if val in p[i]:
                    temp.append(i)
                    count+=1
            if count == 1:
                bool = True
                p[temp[0]]=val
    if bool: return p
    return None

def sud_back_fl_cp(p):
    var = most_constrained(p)
    if var is None: return p
    for val in get_sorted_values(p,var):
        new_p = {a:p[a] for a in p.keys()}
        new_p[var] = val
        checked_p = forward_looking(new_p)
        if checked_p is not None:
            checked_p2 = c_prop(checked_p)
            if checked_p2 is not None:
                result = sud_back_fl_cp(checked_p2)
                if result is not None:
                        return result
            else:
                if checked_p is not None:
                    result = sud_back_fl_cp(checked_p)
                    if result is not None:
                        return result
    return None


def solve(p):
    setupPuzzle(p)
    makeC(p)
    x = setupPuzzle2(p)
    x = forward_looking(x)
    ans = sud_back_fl_cp(x)
    temp = "".join([ans[i] for i in ans.keys()])
    print(temp)

for i in puzzles:
    solve(i)

# print(puzzles[0])
# setupPuzzle(puzzles[0])
# printPuzzle(puzzles[0])
# makeC(puzzles[0])
# x = setupPuzzle2(puzzles[0])
# x = forward_looking(x)
# print(c_prop(x))



