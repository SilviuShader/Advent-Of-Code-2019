import math

def GCD(a, b):
    if b == 0:
        return a
    return GCD(b, a % b)

def IsPosInMap(pos, coordsMap):
    if pos[0] >= 0 and pos[1] >= 0 and pos[0] < len(coordsMap) and pos[1] < len(coordsMap[0]):
        return True
    return False

def Distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def RegularLength(vector):
    return math.sqrt((vector[0]**2) + (vector[1]**2))

def Dot(vector1, vector2):
    return (vector1[0] * vector2[0]) + (vector1[1] * vector2[1])

def RegularNormalize(vector):
    return (vector[0] / RegularLength(vector), vector[1] / RegularLength(vector), vector[2])

def Intersects(asteroid, other, coordsMap):
    vector = (other[0] - asteroid[0], other[1] - asteroid[1])

    # "normalize" the vector
    gcd = GCD(abs(vector[0]), abs(vector[1]))
    vector = (vector[0] // gcd, vector[1] // gcd)

    crtPos = asteroid

    dist = Distance(crtPos, other)
    prevDist = dist

    while IsPosInMap(crtPos, coordsMap):

        if crtPos[0] == other[0] and crtPos[1] == other[1]:
            return True

        if crtPos[0] != asteroid[0] or crtPos[1] != asteroid[1]:
            if coordsMap[crtPos[0]][crtPos[1]] == "#":
                return False

        crtPos = (crtPos[0] + vector[0], crtPos[1] + vector[1])

        prevDist = dist
        dist = Distance(crtPos, other)

        if dist > prevDist:
            return False

    return False

def Detect(coords, asteroid, coordsMap):

    result = 0
    intersections = []

    for coord in coords:
        if coord[0] != asteroid[0] or coord[1] != asteroid[1]:
            if Intersects(asteroid, coord, coordsMap):
                result += 1
                intersections.append(coord)

    return (result, intersections)

inputFile = open("input.txt", "r")

asteroidsMap = [list(line.replace("\n", "")) for line in inputFile.readlines()]

asteroidCoords = []

row = 0
for line in asteroidsMap:
    for column in range(0, len(line)):
        if line[column] == '#':
            asteroidCoords.append((row, column))
    row += 1

bestCount = 0
bestCoords = (0, 0)
for asteroid in asteroidCoords:
    detectedCount = Detect(asteroidCoords, asteroid, asteroidsMap)[0]
    if detectedCount > bestCount:
        bestCoords = asteroid
        bestCount = detectedCount

print ((bestCoords[1], bestCoords[0]), bestCount)
print ("\n")

foundVal = False
destroyedCount = 0
while foundVal == False:

    foundCoords = Detect(asteroidCoords, bestCoords, asteroidsMap)[1]
    # sort the coords clockwise
    # first we get the vectors from the asteroids to the base
    vectors = [RegularNormalize((a - bestCoords[0], b - bestCoords[1], (a, b))) for (a, b) in foundCoords]
    up = (-1, 0)
    # now we'll find the closest vector to the up vector

    bestDot = -10

    index = 0
    foundIndex = 0

    for vector in vectors:
        
        if up[1] * vector[0] >= up[0] * vector[1]:
            if bestDot < Dot(up, vector):
                bestDot = Dot(up, vector)
                # we found the closest to the up vector
                foundIndex = index

        index += 1

    # now that we have the first asteroid, we can use selection sort for the other of other asteroids
    aux = vectors[foundIndex]
    vectors[foundIndex] = vectors[0]
    vectors[0] = aux
    
    for i in range(0, len(vectors) - 1):
        prevVector = vectors[i]
        crtDot = -10
        foundVector = i + 1
        for j in range(i + 1, len(vectors)):
            if prevVector[1] * vectors[j][0] > prevVector[0] * vectors[j][1]:
                if crtDot < Dot(prevVector, vectors[j]):
                    crtDot = Dot(prevVector, vectors[j])
                    foundVector = j

        aux = vectors[foundVector]
        vectors[foundVector] = vectors[i + 1]
        vectors[i + 1] = aux

    # now that we have the list of vectors, we can remove them
    for i in range(0, len(vectors)):
        destroyedCount += 1

        vec = vectors[i][2]
        asteroidsMap[vec[0]][vec[1]] = "."
        asteroidCoords.remove(vec)
        printVal = vectors[i][2]
        print (100 *printVal[1] + printVal[0], destroyedCount)

        if destroyedCount >= 200:
            foundVal = True
            break

inputFile.close()