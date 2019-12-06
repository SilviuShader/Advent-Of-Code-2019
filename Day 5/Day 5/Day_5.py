
inputFile = open("input.txt", "r")

intcode = [int(x) for x in inputFile.read().split(",")]
i = 0

while i < len(intcode):
    instruction = intcode[i] % 100;

    aMode = (intcode[i] // 100) % 10
    bMode = (intcode[i] // 1000) % 10

    if instruction == 1:

        a = intcode[i + 1]
        b = intcode[i + 2]
        c = intcode[i + 3]

        if aMode == 0:
            a = intcode[a]
        if bMode == 0:
            b = intcode[b]

        intcode[c] = a + b
        i += 4

    elif instruction == 2:

        a = intcode[i + 1]
        b = intcode[i + 2]
        c = intcode[i + 3]

        if aMode == 0:
            a = intcode[a]
        if bMode == 0:
            b = intcode[b]

        intcode[c] = a * b
        i += 4

    elif instruction == 3:
        
        a = intcode[i + 1]
        intcode[a] = int(input())
        i += 2

    elif instruction == 4:
        
        a = intcode[i + 1]
        if aMode == 0:
            a = intcode[a]

        print (a)
        i += 2

    elif instruction == 5:

        a = intcode[i + 1]
        b = intcode[i + 2]

        if aMode == 0:
            a = intcode[a]

        if bMode == 0:
            b = intcode[b]

        if a != 0:
            i = b
        else:
            i += 3

    elif instruction == 6:

        a = intcode[i + 1]
        b = intcode[i + 2]

        if aMode == 0:
            a = intcode[a]

        if bMode == 0:
            b = intcode[b]

        if a == 0:
            i = b
        else:
            i += 3

    elif instruction == 7:

        a = intcode[i + 1]
        b = intcode[i + 2]
        c = intcode[i + 3]

        if aMode == 0:
            a = intcode[a]

        if bMode == 0:
            b = intcode[b]
        
        if a < b:
            intcode[c] = 1
        else:
            intcode[c] = 0

        i += 4
    elif instruction == 8:

        a = intcode[i + 1]
        b = intcode[i + 2]
        c = intcode[i + 3]

        if aMode == 0:
            a = intcode[a]

        if bMode == 0:
            b = intcode[b]
        
        if a == b:
            intcode[c] = 1
        else:
            intcode[c] = 0

        i += 4

    elif instruction == 99:

        i = len(intcode) + 1

inputFile.close();