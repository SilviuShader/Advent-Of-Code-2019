import copy

def GenerateNewDigits():
    global digits, newDigits, pattern
    patternStep = 1
        
    for i in range(0, len(newDigits)):

        crtSum = 0

        patternIndex = 0
        patternAccum = 1
        for j in range(0, len(digits)):

            if patternAccum >= patternStep:
                patternAccum = 0
                patternIndex += 1

            if patternIndex >= len(pattern):
                patternIndex = 0

            crtSum += digits[j] * pattern[patternIndex]
            patternAccum += 1

        newDigits[i] = abs(crtSum) % 10

        patternStep += 1

digits = [int(x) for x in input().replace("\n", "")]
initialDigits = copy.deepcopy(digits)

digCount = len(digits)
newDigits = [0] * digCount

pattern = [0, 1, 0, -1]
steps = 100

for i in range(0, steps):

    GenerateNewDigits()
    digits = copy.deepcopy(newDigits)

result1 = ""
for i in range(0, 8):
    result1 = result1 + str(digits[i])

print (result1)

toSkip = 0
for i in range(0, 7):
    toSkip = toSkip * 10 + initialDigits[i]

digits = (initialDigits * 10000)
digits = digits[toSkip:]

for i in range(0, steps):

    for j in range(len(digits) - 2, -1, -1):
        digits[j] += digits[j + 1]
        digits[j] %= 10

result1 = ""
for i in range(0, 8):
    result1 = result1 + str(digits[i])

print (result1)