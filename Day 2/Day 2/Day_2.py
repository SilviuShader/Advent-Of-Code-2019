def execute(numbers, noun, verb):

    numbers[1] = noun
    numbers[2] = verb

    for index in range(0, len(numbers), 4):
        crtCommand = numbers[index]
    
        index1 = numbers[index + 1]
        index2 = numbers[index + 2]
        index3 = numbers[index + 3]

        if crtCommand == 99:
            return numbers[0]
        elif crtCommand == 1:
            numbers[index3] = numbers[index1] + numbers[index2]
        elif crtCommand == 2:
            numbers[index3] = numbers[index1] * numbers[index2]
        else:
            print ("Well, that was unexpected")
            return -1

    return -1

inputFile    = open("input.txt", "r")
wantedValue = 19690720

numbers = [int(x) for x in inputFile.readline().split(",")]

print (execute([x for x in numbers],12, 1))

found = False

for i in range (0, 100):
    for j in range (0, 100):
        val = execute([x for x in numbers], i, j)
        if val == wantedValue:
            
            print (100 * i + j)
            found = True
            break

    if found:
        break

inputFile.close();