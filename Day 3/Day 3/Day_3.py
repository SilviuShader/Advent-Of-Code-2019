import math
import pygame

windowWidth = int(960 * 1.1)
windowHeight = int(720 * 1.1)
drawScale = 0.04

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
            return (abs(x) + abs(y), (x, y))

    return (-1, (0, 0))

def ClosestIntersectionSteps(segment1, segment2):
    if segment1.y1 == segment1.y2 and segment2.x1 == segment2.x2:
        x = segment2.x1
        y = segment1.y1
        if x >= segment1.x1 and x <= segment1.x2 and y >= segment2.y1 and y <= segment2.y2:
            return (segment1.steps + segment2.steps + (abs(x - segment1.anchorx)) + (abs(y - segment2.anchory)), (x, y))

    return (-1, (0, 0))

def DrawSegment(segment, color):
    newSegment = segment

    center = (windowWidth / 2, windowHeight / 2)

    pygame.draw.line(screen, color, (newSegment.x1 * drawScale + center[0], -newSegment.y1 * drawScale + center[1]), (newSegment.x2 * drawScale + center[0], -newSegment.y2 * drawScale + center[1]), 3)

def DrawPoint(position, color):
    center = (windowWidth // 2, windowHeight // 2)
    pygame.draw.circle(screen, color, (int(center[0] + position[0] * drawScale), int(center[1] - position[1] * drawScale)), 7, 7)

inputFile = open("input.txt", "r")

firstInstructions = inputFile.readline().split(",")
secondInstructions = inputFile.readline().split(",")

segments1 = GetSegments(firstInstructions)
segments2 = GetSegments(secondInstructions)

minDistance = math.inf
resultPoint1 = (0, 0)

for segment1 in segments1:
    for segment2 in segments2:

        intersectionDistance, point1 = ClosestIntersection(segment1, segment2)
        intersectionDistance2, point2 = ClosestIntersection(segment2, segment1)

        if intersectionDistance > 0:
            if intersectionDistance < minDistance:
                minDistance = min(minDistance, intersectionDistance)
                resultPoint1 = point1
        
        if intersectionDistance2 > 0:
            if intersectionDistance2 < minDistance:
                minDistance = min(minDistance, intersectionDistance2)
                resultPoint1 = point2

print (minDistance)

minDistance = math.inf
resultPoint2 = (0, 0)

for segment1 in segments1:
    for segment2 in segments2:

        intersectionDistance, point1 = ClosestIntersectionSteps(segment1, segment2)
        intersectionDistance2, point2 = ClosestIntersectionSteps(segment2, segment1)

        if intersectionDistance > 0:
            if intersectionDistance < minDistance:
                minDistance = min(minDistance, intersectionDistance)
                resultPoint2 = point1

        if intersectionDistance2 > 0:
            if intersectionDistance2 < minDistance:
                minDistance = min(minDistance, intersectionDistance2)
                resultPoint2 = point2

print (minDistance)

pygame.init()

screen = pygame.display.set_mode((windowWidth, windowHeight))

crtSegment = 0.0
crtSegment2 = 0.0

running = True
canStart = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            canStart = True

    screen.fill((0, 0, 0))

    for index in range(0, int(crtSegment)):
        DrawSegment(segments1[index], (0, 255, 0))

    for index in range(0, int(crtSegment2)):
        DrawSegment(segments2[index], (255, 0, 0))
    
    if canStart:
        if crtSegment < len(segments1):
            crtSegment += 0.5
        else:
            if crtSegment2 < len(segments2):
                crtSegment2 += 0.5
            else:
                DrawPoint(resultPoint1, (255, 255, 0))
                DrawPoint(resultPoint2, (0, 0, 255))
    pygame.display.flip()

inputFile.close()