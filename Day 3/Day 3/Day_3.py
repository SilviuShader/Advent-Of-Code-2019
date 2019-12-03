import math

class Segment:

    def __init__(self, x1, y1, x2, y2, steps):
        
        if x1 == x2:
           self.x1 = x1;
           self.x2 = x2;
           self.y1 = min(y1, y2)
           self.y2 = max(y1, y2)
        else:
            self.y1 = y1
            self.y2 = y2
            self.x1 = min(x1, x2)
            self.x2 = max(x1, x2)

        self.steps = steps

        self.anchorx = x1
        self.anchory = y1

def GetSegments(instructions):
    
    x     = 0
    y     = 0
    steps = 0

    result = []

    for instruction in instructions:
        add = int(instruction.replace(instruction[0], ''))
        if instruction[0] == 'U':
            result.append(Segment(x, y, x, y + add, steps))
            y += add
        elif instruction[0] == 'D':
            result.append(Segment(x, y, x, y - add, steps))
            y -= add
        elif instruction[0] == 'L':
            result.append(Segment(x, y, x - add, y, steps))
            x -= add
        elif instruction[0] == 'R':
            result.append(Segment(x, y, x + add, y, steps))
            x += add
        else:
            print ("WTF")
        steps += add

    return result

def ClosestIntersection(segment1, segment2):
    
    if segment1.y1 == segment1.y2 and segment2.x1 == segment2.x2:
        x = segment2.x1
        y = segment1.y1
        if x >= segment1.x1 and x <= segment1.x2 and y >= segment2.y1 and y <= segment2.y2:
            return abs(x) + abs(y)

    return -1

def ClosestIntersectionSteps(segment1, segment2):
    if segment1.y1 == segment1.y2 and segment2.x1 == segment2.x2:
        x = segment2.x1
        y = segment1.y1
        if x >= segment1.x1 and x <= segment1.x2 and y >= segment2.y1 and y <= segment2.y2:
            return segment1.steps + segment2.steps + (abs(x - segment1.anchorx)) + (abs(y - segment2.anchory))

    return -1

inputFile = open("input.txt", "r")

firstInstructions = inputFile.readline().split(",")
secondInstructions = inputFile.readline().split(",")

segments1 = GetSegments(firstInstructions)
segments2 = GetSegments(secondInstructions)

minDistance = math.inf

for segment1 in segments1:
    for segment2 in segments2:

        intersectionDistance = ClosestIntersection(segment1, segment2)
        intersectionDistance2 = ClosestIntersection(segment2, segment1)

        if intersectionDistance > 0:
                minDistance = min(minDistance, intersectionDistance)
        
        if intersectionDistance2 > 0:
                minDistance = min(minDistance, intersectionDistance2)

print (minDistance)

minDistance = math.inf

for segment1 in segments1:
    for segment2 in segments2:

        intersectionDistance = ClosestIntersectionSteps(segment1, segment2)
        intersectionDistance2 = ClosestIntersectionSteps(segment2, segment1)

        if intersectionDistance > 0:
                minDistance = min(minDistance, intersectionDistance)

        if intersectionDistance2 > 0:
                minDistance = min(minDistance, intersectionDistance2)

print (minDistance)