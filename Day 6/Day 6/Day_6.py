import queue

def DFS(node, counter):
    if tree.get(node) != None:
        for otherNode in tree.get(node):
            counter[0] += 1
            DFS(otherNode, counter)

def BFS(start, end):

    distance = {}
    distance[start] = 0
    remainingNodes = queue.Queue()
    remainingNodes.put(start)

    while not remainingNodes.empty():
        crtNode = remainingNodes.get()
        newDist = distance[crtNode] + 1
        
        if graph.get(crtNode) != None:
            for neighbour in graph.get(crtNode):
                
                if distance.get(neighbour) == None:
                    distance[neighbour] = newDist
                    remainingNodes.put(neighbour)

                elif distance[neighbour] > newDist:
                    distance[neighbour] = newDist
                    remainingNodes.put(neighbour)

    return distance[end] - 2


inputFile = open("input.txt", "r")

lines = inputFile.readlines()
tree = {}
for line in lines:

    key = line.split(")")[0]
    value = line.split(")")[1].replace("\n", "")

    if tree.get(key) == None:
        tree[key] = [value]
    else:
        tree[key].append(value)

counter = [0]
for key in tree:
    DFS(key, counter)

print (counter[0])

graph = {}

# make the tree into a graph
for key in tree:
    if graph.get(key) == None:
        graph[key] = tree[key]
    else:
        graph[key].extend(tree[key])

    for node in tree[key]:
        if graph.get(node) == None:
            graph[node] = [key]
        else:
            graph[node].append(key)

print (BFS("YOU", "SAN"))

inputFile.close()