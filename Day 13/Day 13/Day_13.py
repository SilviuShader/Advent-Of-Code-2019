import queue
from enum import IntEnum
from time import sleep
import keyboard

# I know, I copy pasted this horrobly written class
# again...
# and again.. I should really write a proper intcode computer
class IntCodeComputer:

    def __init__(self, code):
        self.defaultCode = code
        self.runningCode = self.defaultCode.copy()
        self.instructionPointer = 0
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
            self.outputQueue = queue.Queue()
            self.relativeBase = 0

        inputIndex = 0
        
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

                a = self.AccessLocation(self.instructionPointer + 1)

                if aMode == 2:
                    a = a + self.relativeBase

                self.StoreLocation(a, inputArray[inputIndex])
                inputIndex += 1
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

def Render(screenMatrix):
    finalString = ""
    for row in range(0, len(screenMatrix)):
        for column in range(0, len(screenMatrix[i])):
            finalString += str(screenMatrix[row][column])
        finalString += "\n"
    print (finalString, end = "\r")

def GetBallX(screenMatrix):
    for row in range(0, len(screenMatrix)):
        for column in range(0, len(screenMatrix[i])):
            if screenMatrix[row][column] == 4:
                return column
    return 0

def GetPadX(screenMatrix):
    for row in range(0, len(screenMatrix)):
        for column in range(0, len(screenMatrix[i])):
            if screenMatrix[row][column] == 3:
                return column
    return 0

inputFile = open("input.txt", "r")

code = [int(x) for x in inputFile.read().split(",")]
computer = IntCodeComputer(code)

screenMatrix = [0] * 24
for i in range(0, len(screenMatrix)):
    screenMatrix[i] = [0] * 42

cond = True
while cond:

    result1 = computer.Run([], False)
    if result1 != None:
        result2 = computer.Run([], False)
        result3 = computer.Run([], False)

        screenMatrix[result2][result1] = result3

    else:
        cond = False

counter = 0;

for i in range(0, len(screenMatrix)):
    for j in range(0, len(screenMatrix[i])):
        if screenMatrix[i][j] == 2:
            counter += 1

print (counter)

code[0] = 2

computer = IntCodeComputer(code)

screenMatrix = [0] * 24
for i in range(0, len(screenMatrix)):
    screenMatrix[i] = [0] * 42

cond = True
iter = 0
score = 0
while cond:

    cond2 = True
    exec = 0

    if iter >= len(screenMatrix) * len(screenMatrix[0]):
       sleep(0.001)

    while cond2 or iter < len(screenMatrix) * len(screenMatrix[0]):
        cond2 = True
        exec += 1

        inp = 0
        ballX = GetBallX(screenMatrix)
        padX = GetPadX(screenMatrix)
        if padX == ballX:
            inp = 0
        elif padX > ballX:
            inp = -1
        else:
            inp = 1

        result1 = computer.Run([inp], False)
        if result1 != None:
            result2 = computer.Run([inp], False)
            result3 = computer.Run([inp], False)

            if result1 == -1 and result2 == 0:
                score = result3
            else:
                screenMatrix[result2][result1] = result3
            
            if result3 == 4 or exec >= 10:
                cond2 = False

        else:
            cond = False
            break

        Render(screenMatrix)

        iter += 1

print(score)
inputFile.close()