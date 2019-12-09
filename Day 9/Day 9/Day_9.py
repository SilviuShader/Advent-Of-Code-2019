import queue

# I know, I copy pasted this horrobly written class
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

inputFile = open("input.txt", "r")

intcode = [int(x) for x in inputFile.read().split(",")]

computer = IntCodeComputer(intcode)
result = computer.Run([2], False)

while result != None:
    print(result)
    result = computer.Run([], False)

inputFile.close()