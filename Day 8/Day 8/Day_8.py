def LayerDetails(layer):

    startPixel = layer * pixelsPerLayer
    zeroCount = 0

    oneCount = 0
    twoCount = 0
    for i in range(startPixel, startPixel + pixelsPerLayer):

        if imgData[i] == 0:
            zeroCount += 1
        elif imgData[i] == 1:
            oneCount += 1
        elif imgData[i] == 2:
            twoCount += 1

    return (zeroCount, oneCount * twoCount)

def StoreData(layer):

    startPixel = layer * pixelsPerLayer
    imageIndex = 0
    for i in range(startPixel, startPixel + pixelsPerLayer):
        if imageIndex >= len(outputData):
            outputData.append(imgData[i])
        else:
            if outputData[imageIndex] == 2:
                outputData[imageIndex] = imgData[i]
        imageIndex += 1

inputFile = open("input.txt", "r")
data = inputFile.read()
inputFile.close()

imgData = [int(x) for x in data]

imgWidth = 25
imgHeight = 6

pixelsPerLayer = imgWidth * imgHeight
layersCount = len(imgData) // pixelsPerLayer

prevMinZero = len(imgData) + 1
result = 0

for layer in range(0, layersCount):
    layerDetails = LayerDetails(layer)

    if layerDetails[0] < prevMinZero:
        prevMinZero = layerDetails[0]
        result = layerDetails[1]

print (result)

outputFile = open("output.txt", "w")

outputData = []
for layer in range(0, layersCount):
    StoreData(layer)
    
renderIndex = 0
for i in range(0, imgHeight):
    row = ""
    for j in range(0, imgWidth):
        if outputData[renderIndex] == 1:
            row = row + str(outputData[renderIndex])
        else:
            row = row + " "
        renderIndex += 1
    outputFile.write(row + "\n")

outputFile.close()