class ProduceDetails:

    def __init__(self, prodQuantity, requirements):
        self.prodQuantity = prodQuantity
        self.requirements = requirements
        self.produced = 0
        self.needToProduce = 0

def Produce(material):
    details = recipes[material]
    remainToProduce = details.needToProduce - details.produced

    if remainToProduce > 0:
        timesToProduce = remainToProduce // details.prodQuantity
        if timesToProduce * details.prodQuantity < remainToProduce:
            timesToProduce += 1

        for requirement in details.requirements:
            recipes[requirement[1]].needToProduce += requirement[0] * timesToProduce
            Produce(requirement[1])

        recipes[material].produced += timesToProduce * details.prodQuantity
               

inputFile = open("input.txt", "r")

pairs = [(line.split("=")[0], line.split("=")[1].replace(">", "").replace("\n", "")) for line in inputFile.readlines()]

recipes = {}

for (a, b) in pairs:
    rawRequirements = [ore for ore in a.split(",")]
    requirements = []
    for req in rawRequirements:
        reqs = req.split(" ")
        reqIndex = 0
        if reqs[0] == "":
            reqIndex = 1
        requirements.append((int(reqs[reqIndex]), reqs[reqIndex+1]))

    secondArg = b.split(" ")
    prodQuantity = int(secondArg[1])
    name = secondArg[2]
    
    recipes[name] = ProduceDetails(prodQuantity, requirements)

recipes["FUEL"].needToProduce = 1
recipes["ORE"] = ProduceDetails(1, [])
Produce("FUEL")
result1 = recipes["ORE"].produced
print (recipes["ORE"].produced)
trillion = 1000000000000


result2 = recipes["FUEL"].produced
# we brute force like TARANII
while recipes["ORE"].produced <= trillion:
    result2 = recipes["FUEL"].produced
    recipes["FUEL"].needToProduce += 1
    Produce("FUEL")

print (result2)

inputFile.close()