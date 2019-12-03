
def ModuleMass(x):   
    result = 0
    
    while x > 0:
        x = x // 3
        x -= 2
        if x >= 0:
            result += x

    return result

def Solve1(messes):
    result = 0

    for mass in masses:
        crtMass = mass // 3
        crtMass -= 2
        result += crtMass

    return result

def Solve2(masses):
    result = 0

    for mass in masses:
        result += ModuleMass(mass)

    return result

inputFile = open("input.txt", "r")

fileData = []
fileData = inputFile.readlines()
masses = [int(x) for x in fileData]

print (Solve1(masses))
print (Solve2(masses))

inputFile.close()