import sys
import time

# python3 Sudoku.py puzzles_1_standard_easy.txt

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
dictionary = {}
N = None
subblock_height = None
subblock_width = None
symbol_set = None

def displayPuzzle(puzzle):
    length = int(len(puzzle)**(1/2))
    for x in range(length):
        print(puzzle[x*length:(x+1)*length].replace("", " ").strip())
        
def findConstraintSets(width, height):
    setList = []
    squareDic = {}
    length = int(width*height)
    for x in range(length):
        cSet = []
        for y in range(length):
            cSet.append(x*length + y)
        setList.append(cSet)
    for x in range(length):
        cSet = set()
        for y in range(length):
            cSet.add(x + y*length)
        setList.append(cSet)
    for a in range(width):
        for b in range(height):
            cSet = set()
            for z in range(height):
                for y in range(width):
                    cSet.add(b*width + a*height*length + y + z*length)
            setList.append(cSet)
    for cSet in setList:
        for x in cSet:
            if(x not in squareDic):
                squareDic[x] = set()
            for y in cSet:
                if(x != y):
                    squareDic[x].add(y)
    print(squareDic)
    dictionary[length] = squareDic
                

def symbolNum(puzzle):
    symbolDic = {}
    for x in puzzle:
        if(x in symbolDic):
            symbolDic[x] += 1
        else:
            symbolDic[x] = 1
    for x in symbolDic:
        print(str(x) + ": " + str(symbolDic[x]) + " instances")

def get_next_unassigned_var(puzzle):
    return puzzle.index(".")

def get_sorted_values(puzzle, index, width, height):
    length = int(width*height)
    if(length not in dictionary):
        findConstraintSets(width, height)
    squareDic = dictionary[length]
    possible = symbol_set.copy()
    #print(possible)
    for x in squareDic[index]:
        if(puzzle[x] in possible):
            possible.remove(puzzle[x])
    return possible
    
    
    
def backtracking(puzzle, width, height):
    if("." not in puzzle):
        return puzzle
    index = get_next_unassigned_var(puzzle)
    a = get_sorted_values(puzzle, index, width, height).copy()
    #print(a)
    for x in a:
        newPuzzle = puzzle[:index] + x + puzzle[index+1:]
        result = backtracking(newPuzzle, width, height)
        if result is not None:
            return result
    return None
"""
puzzle = "..87A5169331.69A4872936217854A547A8632196A9531248778412359A68513796A24A629487351193452A76827..649135"
symbol_set = set()
for x in range(1, 11):
    if(x < 10):
        symbol_set.add(str(x))
    else:
        symbol_set.add(alphabet[(x-10)])


"""
file = sys.argv[1]
count = 0
with open(file) as f:
    for line in f:
        count+= 1
        N = int((len(line))**(1/2))
        sqrt = N**(1/2)
        subblock_height = 0
        subblock_width = 0
        if(sqrt%1 == 0):
            subblock_height = int(sqrt)
            subblock_width = int(sqrt)
        else:
            count1 = int(sqrt//1)
            count2 = int(sqrt//1) + 1
            while(N%count1 != 0):
                count1 -= 1
            while(N%count2 != 0):
                count2 += 1
            subblock_height = int(count1)
            subblock_width = int(count2)
        symbol_set = set()
        for x in range(1, N+1):
            if(x < 10):
                symbol_set.add(str(x))
            else:
                symbol_set.add(alphabet[(x-10)])
        print(backtracking(line, subblock_width, subblock_height))

