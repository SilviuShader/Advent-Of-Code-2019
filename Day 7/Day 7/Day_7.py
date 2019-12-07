import queue

class IntCodeComputer:

    def __init__(self, code):
        self.defaultCode = code
        self.runningCode = self.defaultCode.copy()
        self.instructionPointer = 0
        self.inputQueue = queue.Queue()
        self.outputQueue = queue.Queue()

    def Run(self, inputArray, reset):

        if reset == True:
            self.runningCode = self.defaultCode.copy()
            self.instructionPointer = 0
            self.inputQueue = queue.Queue()
            self.outputQueue = queue.Queue()

        for inAr in inputArray:
            self.inputQueue.put(inAr)
        
        while self.instructionPointer < len(self.runningCode):
            instruction = self.runningCode[self.instructionPointer] % 100;

            aMode = (self.runningCode[self.instructionPointer] // 100) % 10
            bMode = (self.runningCode[self.instructionPointer] // 1000) % 10
            a = b = c = 0

            if instruction == 1 or instruction == 2 or instruction == 7 or instruction == 8:
                a = self.runningCode[self.instructionPointer + 1]
                b = self.runningCode[self.instructionPointer + 2]
                c = self.runningCode[self.instructionPointer + 3]
                if aMode == 0:
                    a = self.runningCode[a]
                if bMode == 0:
                    b = self.runningCode[b]
            if instruction == 5 or instruction == 6:
                a = self.runningCode[self.instructionPointer + 1]
                b = self.runningCode[self.instructionPointer + 2]

                if aMode == 0:
                    a = self.runningCode[a]

                if bMode == 0:
                    b = self.runningCode[b]

            if instruction == 1:
                self.runningCode[c] = a + b
                self.instructionPointer += 4

            elif instruction == 2:
                self.runningCode[c] = a * b
                self.instructionPointer += 4

            elif instruction == 3:

                if self.inputQueue.empty():
                    return None

                a = self.runningCode[self.instructionPointer + 1]
                self.runningCode[a] = self.inputQueue.get()
                self.instructionPointer += 2

            elif instruction == 4:
                a = self.runningCode[self.instructionPointer + 1]
                if aMode == 0:
                    a = self.runningCode[a]

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
                    self.runningCode[c] = 1
                else:
                    self.runningCode[c] = 0
                self.instructionPointer += 4

            elif instruction == 8:
                if a == b:
                    self.runningCode[c] = 1
                else:
                    self.runningCode[c] = 0
                self.instructionPointer += 4

            elif instruction == 99:
                self.instructionPointer = len(self.runningCode) + 1
                self.outputQueue.put(None)

        return self.outputQueue.get()

def Backtr(n, k, index, solution, maxValue, been):
    if index >= n:
        
        lastOutput = 0
        for sol in solution:
            lastOutput = computer.Run([sol, lastOutput], True)

        if lastOutput > maxValue[0]:
            maxValue[0] = lastOutput

    else:

       for i in range(0, k):
           if been[i] == False:

               been[i] = True
               solution[index] = i
               Backtr(n, k, index + 1, solution, maxValue, been)
               been[i] = False

def Backtr2(n, k, index, solution, maxValue, been):
    if index >= n:
        
        computers = [IntCodeComputer(intcode) for x in range(0, n)]
        cond = True
        lastOutput = 0
        iter = 0
        lastE = None

        while cond:
            comIndex = 0
            for com in computers:
                # F-in hell, it took me quite a while to understand
                # that I have to do this
                if iter == 0:
                    output = com.Run([solution[comIndex], lastOutput], False)
                else:
                    output = com.Run([lastOutput], False)

                if output == None:
                    cond = False
                    lastOutput = lastE
                    break

                lastOutput = output
                comIndex += 1
                if lastOutput != None and comIndex == n:
                    lastE = lastOutput

            if cond == False:
                if lastOutput > maxValue[0]:
                    maxValue[0] = lastOutput
            iter += 1
                
    else:

        for i in range(5, k+5):
            if been[i] == False:

                been[i] = True
                solution[index] = i
                Backtr2(n, k, index+1, solution, maxValue, been)
                been[i] = False

inputFile = open("input.txt", "r")

intcode = [int(x) for x in inputFile.read().split(",")]
computer = IntCodeComputer(intcode)

solution = [0 for x in range(0, 5)]
been = [False for x in range(0, 5)]
maxValue = [0]

Backtr(5, 5, 0, solution, maxValue, been)

print (maxValue[0])

solution = [0 for x in range(0, 5)]
been = [False for x in range(0, 10)]
maxValue = [0]

Backtr2(5, 5, 0, solution, maxValue, been)

print (maxValue[0])

inputFile.close()
