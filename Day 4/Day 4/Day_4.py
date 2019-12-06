def CheckNumber(number):
    gotTwice = False
    prevC = 10

    while number != 0:
        
        c = number % 10
        number //= 10
        
        if c > prevC:
            return False
        if c == prevC:
            gotTwice = True

        prevC = c

    return gotTwice

def CheckNumber2(number):

    gotTwice = False
    prevC = 10
    occurences = 0

    while number != 0:
        
        c = number % 10
        number //= 10
        
        if c > prevC:
            return False

        if c == prevC:
            occurences += 1
        else:
            if occurences == 1:
                gotTwice = True

            occurences = 0

        prevC = c


    if occurences == 1:
        gotTwice = True

    return gotTwice

left, right = input().split("-")

left = int(left)
right = int(right)

count = 0

for i in range(left, right + 1):
    if CheckNumber(i):
        count += 1

print (count)

count = 0

for i in range(left, right + 1):
    if CheckNumber2(i):
        count += 1

print (count)