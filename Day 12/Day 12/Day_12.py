import math

def ClampVel(vel):
    if vel >= 1:
        vel = 1
    if vel <= -1:
        vel = -1
    return vel

def UpdatePositions():
        # each moon is influenced by the other moons
    for moonIndex in range(0, len(positions)):
        for otherMoonIndex in range(0, len(positions)):
            diffX = positions[otherMoonIndex][0] - positions[moonIndex][0]
            diffY = positions[otherMoonIndex][1] - positions[moonIndex][1]
            diffZ = positions[otherMoonIndex][2] - positions[moonIndex][2]

            velocities[moonIndex] = (velocities[moonIndex][0] + ClampVel(diffX), velocities[moonIndex][1] + ClampVel(diffY), velocities[moonIndex][2] + ClampVel(diffZ))

    for moonIndex in range(0, len(positions)):
        positions[moonIndex] = (positions[moonIndex][0] + velocities[moonIndex][0], positions[moonIndex][1] + velocities[moonIndex][1], positions[moonIndex][2] + velocities[moonIndex][2])

def GCD(a, b):
    if b == 0:
        return a
    return GCD(b, a % b)

def LCM(a, b):
    return (a * b) // GCD(a, b)

inputFile = open("input.txt", "r")

lines = [line for line in inputFile.readlines()]
positions = []
velocities = []
for line in lines:
    vals = line.split(" ");
    for i in range(0, len(vals)):
        vals[i] = vals[i].strip("<>=,xyz\n");
    pos = (int(vals[0]), int(vals[1]), int(vals[2]))
    positions.append(pos)
    velocities.append((0, 0, 0))

backupPositions = positions.copy()
backupVelocities = velocities.copy()

# simulate
for i in range(0, 1000):
    UpdatePositions()
    # calculate the energy
energy = 0
for i in range(0, len(positions)):
    posE = abs(positions[i][0]) + abs(positions[i][1]) + abs(positions[i][2])
    kinE = abs(velocities[i][0]) + abs(velocities[i][1]) + abs(velocities[i][2])
    energy = energy + (posE * kinE)

print (energy)

positions = backupPositions.copy()
velocities = backupVelocities.copy()

periods = (-1, -1, -1)
step = 1
while periods[0] == -1 or periods[1] == -1 or periods[2] == -1:
    step += 1
    UpdatePositions()
    gotPeriods = [True] * 3
    for index in range(0, len(positions)):
        
        if backupPositions[index][0] != positions[index][0]:
            gotPeriods[0] = False

        if backupPositions[index][1] != positions[index][1]:
            gotPeriods[1] = False
        
        if backupPositions[index][2] != positions[index][2]:
            gotPeriods[2] = False
    
    if gotPeriods[0] and periods[0] == -1:
        periods = (step, periods[1], periods[2])

    if gotPeriods[1] and periods[1] == -1:
        periods = (periods[0], step, periods[2])

    if gotPeriods[2] and periods[2] == -1:
        periods = (periods[0], periods[1], step)

print (LCM(periods[0], LCM(periods[1], periods[2])))

inputFile.close()