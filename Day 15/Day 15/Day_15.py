import collections
import copy
from enum import IntEnum

# I know, I copy pasted this horrobly written class
# again...
# yeah.. I'll keep this shit computer
class IntCodeComputer:

    def __init__(self, code):
        self.defaultCode = code
        self.runningCode = self.defaultCode.copy()
        self.instructionPointer = 0
        self.inputQueue = collections.deque()
        self.outputQueue = collections.deque()
        self.relativeBase = 0

    def __deepcopy__(self, memodict={}):
        cpyobj = type(self)(self.defaultCode) # shallow copy of whole object 
        cpyobj.defaultCode = copy.deepcopy(self.defaultCode, memodict) # deepcopy required attr
        cpyobj.runningCode = copy.deepcopy(self.runningCode, memodict) # deepcopy required attr
        cpyobj.instructionPointer = copy.deepcopy(self.instructionPointer, memodict) # deepcopy required attr
        cpyobj.inputQueue = copy.deepcopy(self.inputQueue, memodict) # deepcopy required attr
        cpyobj.outputQueue = copy.deepcopy(self.outputQueue, memodict) # deepcopy required attr
        cpyobj.relativeBase = copy.deepcopy(self.relativeBase, memodict) # deepcopy required attr

        return cpyobj

    def AccessLocation(self, index):
        if index >= len(self.runningCode):
            self.runningCode.extend([0 for i in range(0, index - len(self.runningCode) + 1)])
        return self.runningCode[index]

    def StoreLocation(self, index, value):
        if index >= len(self.runningCode):
            self.runningCode.extend([0 for i in range(0, index - len(self.runningCode) + 1)])
        self.runningCode[index] = value

    def Run(self, inputArray, reset):

        if reset == True:
            self.runningCode = self.defaultCode.copy()
            self.instructionPointer = 0
            self.inputQueue = queue.Queue()
            self.outputQueue = queue.Queue()
            self.relativeBase = 0

        for inAr in inputArray:
            self.inputQueue.append(inAr)
        
        while self.instructionPointer < len(self.runningCode):
            instruction = self.runningCode[self.instructionPointer] % 100;

            aMode = (self.runningCode[self.instructionPointer] // 100) % 10
            bMode = (self.runningCode[self.instructionPointer] // 1000) % 10
            cMode = (self.runningCode[self.instructionPointer] // 10000) % 10

            a = b = c = 0

            if instruction == 1 or instruction == 2 or instruction == 7 or instruction == 8:
                a = self.AccessLocation(self.instructionPointer + 1)
                b = self.AccessLocation(self.instructionPointer + 2)
                c = self.AccessLocation(self.instructionPointer + 3)
                
                if aMode == 0:
                    a = self.AccessLocation(a)
                if aMode == 2:
                    a = self.AccessLocation(a + self.relativeBase)

                if bMode == 0:
                    b = self.AccessLocation(b)
                if bMode == 2:
                    b = self.AccessLocation(b + self.relativeBase)

                if cMode == 2:
                    c = c + self.relativeBase

            if instruction == 5 or instruction == 6:
                a = self.AccessLocation(self.instructionPointer + 1)
                b = self.AccessLocation(self.instructionPointer + 2)

                if aMode == 0:
                    a = self.AccessLocation(a)
                if aMode == 2:
                    a = self.AccessLocation(a + self.relativeBase)

                if bMode == 0:
                    b = self.AccessLocation(b)
                if bMode == 2:
                    b = self.AccessLocation(b + self.relativeBase)

            if instruction == 1:
                self.StoreLocation(c, a + b)
                self.instructionPointer += 4

            elif instruction == 2:
                self.StoreLocation(c, a * b)
                self.instructionPointer += 4

            elif instruction == 3:

                if not self.inputQueue:
                    return -1

                a = self.AccessLocation(self.instructionPointer + 1)

                if aMode == 2:
                    a = a + self.relativeBase

                self.StoreLocation(a, self.inputQueue.pop())
                self.instructionPointer += 2

            elif instruction == 4:
                a = self.AccessLocation(self.instructionPointer + 1)
                if aMode == 0:
                    a = self.AccessLocation(a)
                if aMode == 2:
                    a = self.AccessLocation(a + self.relativeBase)

                self.instructionPointer += 2
                return a

            elif instruction == 5:
                if a != 0:
                    self.instructionPointer = b
                else:
                    self.instructionPointer += 3

            elif instruction == 6:
                if a == 0:
                    self.instructionPointer = b
                else:
                    self.instructionPointer += 3

            elif instruction == 7:
                if a < b:
                    self.StoreLocation(c, 1)
                else:
                    self.StoreLocation(c, 0)
                self.instructionPointer += 4

            elif instruction == 8:
                if a == b:
                    self.StoreLocation(c, 1)
                else:
                    self.StoreLocation(c, 0)
                self.instructionPointer += 4

            elif instruction == 9:

                a = self.AccessLocation(self.instructionPointer + 1)
                if aMode == 0:
                    a = self.AccessLocation(a)
                if aMode == 2:
                    a = self.AccessLocation(a + self.relativeBase)

                self.relativeBase += a
                self.instructionPointer += 2

            elif instruction == 99:
                self.instructionPointer = len(self.runningCode) + 1
                return None
            else:
                print ("WTF")
                return None

        return None

def Lee(initialComputer):
    global visistedMap, resultPos
    computersQueue = collections.deque()
    computersQueue.append((initialComputer, 0, (0, 0)))
    result = 0

    while computersQueue:
        crtElem = computersQueue.pop()
        comp = crtElem[0]
        dist = crtElem[1]
        pos = crtElem[2]
        
        # now try the input directions
        for dir in range(1, 5):
            newComp = copy.deepcopy(comp)
            status = newComp.Run([dir], False)
            newPos = pos
            
            if dir == 1:
                newPos = (newPos[0] - 1, newPos[1])
            elif dir == 2:
                newPos = (newPos[0] + 1, newPos[1])
            elif dir == 3:
                newPos = (newPos[0], newPos[1] - 1)
            elif dir == 4:
                newPos = (newPos[0], newPos[1] + 1)

            if newPos not in visitedMap:

                if status == 1 or status == 2:
                    visitedMap[newPos] = True
                    computersQueue.append((newComp, dist + 1, newPos))
                else:
                    visitedMap[newPos] = False

                if status == 2:
                    result = dist + 1
                    resultPos = newPos

    return result

def Lee2():
    global visitedMap, resultPos
    
    positionsQueue = collections.deque()
    positionsQueue.append((resultPos[0], resultPos[1], 0))

    visited = set()
    visited.add((resultPos[0], resultPos[1]))

    result = 0

    while positionsQueue:

        firstPos = positionsQueue.pop()
        newPos = firstPos

        dy = [0, -1, 0, 1]
        dx = [-1, 0, 1, 0]

        for i in range(0, 4):
            
            newPos = (firstPos[0] + dy[i], firstPos[1] + dx[i], firstPos[2] + 1)
            if (newPos[0], newPos[1]) not in visited and visitedMap[(newPos[0], newPos[1])] == True:

                visited.add((newPos[0], newPos[1]))
                positionsQueue.append(newPos)
                result = max(result, newPos[2])

    return result

inputFile = open("input.txt", "r")
code = [int(x) for x in inputFile.read().split(",")]

visitedMap = {}
resultPos = (0, 0)

initialComputer = IntCodeComputer(code)
print (Lee(initialComputer), resultPos)
print (Lee2())


inputFile.close()