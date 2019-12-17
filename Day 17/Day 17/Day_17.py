import queue
import re

# I won't bother anymore
class IntCodeComputer:

    def __init__(self, code):
        self.defaultCode = code
        self.runningCode = self.defaultCode.copy()
        self.instructionPointer = 0
        self.inputQueue = queue.Queue()
        self.outputQueue = queue.Queue()
        self.relativeBase = 0

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
            self.inputQueue.put(inAr)
        
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

                if self.inputQueue.empty():
                    return None

                a = self.AccessLocation(self.instructionPointer + 1)

                if aMode == 2:
                    a = a + self.relativeBase

                self.StoreLocation(a, self.inputQueue.get())
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

        return self.outputQueue.get()

class MoveInstruction:

    def __init__(self, dir, length):
        self.dir = dir
        self.length = length

def ValidPos(row, col):
    global mat
    
    if row >= 0 and row < len(mat) and col >= 0 and col < len(mat[0]):
        return True

    return False

def GetLeftVector(vector):
    if vector[0] == -1:
        return (0, -1)
    elif vector[1] == -1:
        return (1, 0)
    elif vector[0] == 1:
        return (0, 1)
    elif vector[1] == 1:
        return (-1, 0)

def GetRightVector(vector):
    return GetLeftVector(GetLeftVector(GetLeftVector(vector)))

def GetMoveSequence():
    global mat
    
    playerPos = (0, 0)
    result = []

    for row in range(len(mat)):
        for col in range(len(mat[0])):
            if mat[row][col] == "^":
                playerPos = (row, col)

    moveDir = (-1, 0)

    fin = False
    crtMove = MoveInstruction("", 0)
    moved = 0
    while not fin:

        crtMove.length = moved
        newPos = (playerPos[0] + moveDir[0], playerPos[1] + moveDir[1])

        if (not ValidPos(newPos[0], newPos[1])) or mat[newPos[0]][newPos[1]] != "#":
            result.append(crtMove)
            moved = 0
            leftVec = GetLeftVector(moveDir)
            rightVec = GetRightVector(moveDir)

            changedDir = False

            testPos = (playerPos[0] + leftVec[0], playerPos[1] + leftVec[1])

            if ValidPos(testPos[0], testPos[1]):
                if mat[testPos[0]][testPos[1]] == "#":
                    moveDir = leftVec
                    changedDir = True
                    crtMove = MoveInstruction("L", 0)
                    newPos = testPos

            testPos = (playerPos[0] + rightVec[0], playerPos[1] + rightVec[1])

            if ValidPos(testPos[0], testPos[1]):
                if mat[testPos[0]][testPos[1]] == "#":
                    moveDir = rightVec
                    changedDir = True
                    crtMove = MoveInstruction("R", 0)
                    newPos = testPos

            if not changedDir:
                fin = True
                       
        playerPos = newPos
        moved += 1

    return result


inputFile = open("input.txt", "r")

intcode = [int(x) for x in inputFile.read().split(",")]

computer = IntCodeComputer(intcode)

result = computer.Run([], False)

mat = [""]

while result != None:

    crtStr = mat[len(mat) - 1]
    if result == 35:
        crtStr += "#"
        mat[len(mat) - 1] = crtStr

    elif result == 46:
        crtStr += "."
        mat[len(mat) - 1] = crtStr
    
    elif result == 10:
        mat.append("")

    else:
        crtStr += chr(result)
        mat[len(mat) - 1] = crtStr
           
    result = computer.Run([], False)

mat.pop()
mat.pop()

result = 0

for row in range(len(mat)):
    printString = ""
    for col in range(len(mat[row])):
        if mat[row][col] == "#":
            dirX = [0, -1, 0, 1]
            dirY = [-1, 0, 1, 0]

            valid = True

            for k in range(0, 4):
                newRow = dirY[k] + row
                newCol = dirX[k] + col

                if ValidPos(newRow, newCol) == True:
                    if mat[newRow][newCol] != "#":
                        valid = False

            if valid:
                add = row * col
                result += add
                printString += "O"
            else:
                printString += "#"
        else:
            printString += mat[row][col]
    #print(printString)

print(result)

moveSequence = GetMoveSequence()
for seq in moveSequence:
    pass

seqString = ""
for i in range(1, len(moveSequence)):
    seqString += moveSequence[i].dir
    seqString += str(moveSequence[i].length)

# print (seqString)

# my results, good enough to manually send data to the robot
'''
R4L12L8R4 L8R10R10R6 R4L12L8R4 R4R10L12 R4L12L8R4 L8R10R10R6 R4L12L8R4 R4R10L12 L8R10R10R6 R4R10L12
'''

A = "R,4,L,12,L,8,R,4\n"
B = "L,8,R,10,R,10,R,6\n"
C = "R,4,R,10,L,12\n"

order = "A,B,A,C,A,B,A,C,B,C\n"

inputs = [ord(x) for x in order]
inputs.extend([ord(x) for x in A])
inputs.extend([ord(x) for x in B])
inputs.extend([ord(x) for x in C])
inputs.extend([ord("n"), 10])

intcode[0] = 2

#reset the computer
newComputer = IntCodeComputer(intcode)
result = newComputer.Run(inputs, False)
prevRes = result
while result != None:
    prevRes = result
    result = newComputer.Run(inputs, False)

print (prevRes)

# this was an attempt, I won't bother making this work
'''
index = 0
stop = False
while index < len(seqString) and not stop:
    
    prevSubstrings = []
    for j in range(index + 1, len(seqString)):
        rng = (index, j)
        substr = seqString[index : j + 1]
        substrings = re.findall(substr, seqString)
        accumDiff = 1

        if len(substrings) == 1 or len(substrings[0]) > 20:
            index = j - accumDiff - 1
            #if len(prevSubstrings) == 0:
                #stop = True
                
            print (prevSubstrings)
            break

        if substrings[0][len(substrings[0])-1].isdigit():
            prevSubstrings = substrings
            accumDiff += 1
        else:
            accumDiff = 1
    index += 1
'''

inputFile.close()