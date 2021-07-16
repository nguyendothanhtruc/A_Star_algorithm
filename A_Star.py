from PIL import Image
import numpy as np


class Node:
    x : int= None
    y : int= None
    gn : float = None
    fn : float = None
    hn : float = None
    parent = None

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.fn = 0
        self.gn = 0
        self.hn = 0

    def isEqual(self,G):
        if self.x == G.x and self.y == G.y:
            return True
        return False


#Handle input 
def convertToMatrix(filepath:str):
    #Open file bitmap => convert to array greyscale
    img = Image.open(filepath)
    bitmap = img.convert("L")
    map = np.asarray(bitmap,dtype='int')
    bitmap.close()
    return map

def readInput(filepath:str):
    input = open(filepath,'r',encoding = 'utf-8')

    Line = input.readline()
    Line = Line.replace('(','')
    Line = Line.replace(')','')
    a,b = Line.split(';')
    S = Node(int(a), int(b))

    Line = input.readline()
    Line = Line.replace('(','')
    Line = Line.replace(')','')
    a,b = Line.split(';')
    G = Node(int(a), int(b))

    Line = input.readline()
    m = int(Line)

    input.close()

    return S,G,m

#Output to file
def colorBMP(G:Node):
    img = Image.open(imageInput)

    color = (255,0,0)
    
    while not G.isEqual(Start):
        img.putpixel((G.x,G.y),color)
        G = G.parent
      
    img.putpixel((G.x,G.y),color)

    img.save(imageOutput)

def writePath(G:Node, closed_list):
    output = open(fileOutput,'w')

    if G != None:
        distance = str(G.gn) + '\n'
        count = str(np.count_nonzero(closed_list)) + '\n'
        s = [distance, count]
        
        output.writelines(s)

        output.close()

        colorBMP(G)
    else:
        output.write("No solution / Error")

        output.close()


#Calculate distance from A->B:
def distance(A:Node,B:Node):
    deltaA = map[A.y][A.x] - map[B.y][B.x]
    
    AB = np.sqrt(np.square(B.x-A.x) + np.square(B.y - A.y))
 
    return AB + abs(deltaA)*(0.5*np.sign(deltaA)+1)

#Check if can climb from A->B:
def checkHeight(A:Node, B:Node):
    deltaA = map[A.y][A.x] - map[B.y][B.x]
    if abs(deltaA) <= m:
        return True
    return False

#Check if node in queue:
def isIn(list, G:Node):
    for item in list:
        if item.x == G.x and item.y == G.y:
            return True,item

    return False,G

#Heuristic functions:
def H1_Manhattan(A:Node, B:Node):
    return abs(A.x-B.x)+abs(A.y-B.y) + abs(map[A.y][A.x] - map[B.y][B.x])

def H2_Euclid(A:Node, B:Node):
    return np.sqrt(np.square(A.x-B.x)+np.square(A.y-B.y))

def H3_Complex(A:Node, B:Node):
    dx1 = A.x - B.x
    dy1 = A.y - B.y
    dx2 = Start.x - B.x
    dy2 = Start.y - B.y
    cross = abs(dx1*dy2 - dx2*dy1)
    return cross*0.001

def generateSuccessor(currentNode:Node):
    #Current_node coordinates
    x = currentNode.x
    y = currentNode.y

    row, column = map.shape 

    successor = []
    #Generates successors
    if y-1 > 0: #If not top border
        A = Node(x, y-1)
        if (checkHeight(currentNode,A)):
            successor.append(A)

        if x + 1 < column: #If not right border
            A = Node(x+1,y-1)
            if (checkHeight(currentNode,A)):
                successor.append(A)

            A = Node(x+1,y)
            if (checkHeight(currentNode,A)):
                successor.append(A)

        if x - 1 > 0: #If not left border
            A = Node(x-1,y-1)
            if (checkHeight(currentNode,A)):
                successor.append(A)

            A = Node(x-1,y)
            if (checkHeight(currentNode,A)):
                successor.append(A)   

    #If not bottom border
    if y + 1 < row: 
        A = Node(x,y+1)
        if (checkHeight(currentNode,A)):
            successor.append(A)

        if x + 1 < column:  #If not right border
            A = Node(x+1,y+1)
            if (checkHeight(currentNode,A)):
                successor.append(A)

        if x - 1 > 0:   #If not left border
            A = Node(x-1,y+1)
            if (checkHeight(currentNode,A)):
                successor.append(A)
        
    #If not right border
    if x + 1 < column: 
        A = Node(x+1,y)
        if (checkHeight(currentNode,A)):
                successor.append(A)

    #If not left border
        if x - 1 > 0: 
            A = Node(x-1,y)
            if (checkHeight(currentNode,A)):
                successor.append(A)  

    return successor   

def A_Star(heuristic):
    #Open list to store node have not been explored
    queue:list = [] 

    #initialize matrix store g(n) value of each node
    row,col=map.shape
    closed_list=np.zeros((row,col))

    #Put Start node to open_list
    queue.append(Start)
    Start.fn = heuristic(Start,Goal)


    currentNode:Node

    #While open_list is not empty

    dup=closed_list
    while (queue):
        currentNode = queue[0]

        #Reach goal -> draw path
        if currentNode.isEqual(Goal): 
            return writePath(currentNode,closed_list)

        #Generate all successors of this node
        successor = generateSuccessor(currentNode)

        #For each node in successros[]
        for node in successor:
            #Calculate cost from current node to this successor
            successor_cost = currentNode.gn + distance(currentNode,node)

            #If node is in queue and has g(n) <= successor_cost => Skip this node
            #Otherwise, update node's value
            check,node = isIn(queue,node)
            if check:
                if node.gn <= successor_cost: 
                    continue

            else: 
               
                #If node is in closed_list has g(n) <= successor_cost => Skip this node
                #Otherwise, add this node back to queue
                if closed_list[node.y][node.x] > 0:
                    if closed_list[node.y][node.x] <= successor_cost: 
                        continue

                    queue.append(node)

                    closed_list[node.y][node.x]=0
 

                #Update h(n) and add this node to queue
                else:
                	node.hn = heuristic(node,Goal) 

                	queue.append(node)

            #Update node's value
            node.gn = successor_cost
            node.fn = node.gn + node.hn
            node.parent = currentNode
               
        #Add current_node to closed list
        closed_list[currentNode.y][currentNode.x]=currentNode.gn

        #Remove current node from queue
        queue.remove(currentNode)

        #Sort queue according to f(n) value
        queue.sort(key = lambda Node: Node.fn)

        #test
        dup=closed_list


    #If the last node is not goal -->No solution or error
    if currentNode != Goal: writePath(None,closed_list)
    print(dup)


#---------MAIN--------:

#Global variable
imageInput = 'map.bmp'
fileInput = 'input.txt'

map = convertToMatrix(imageInput)

Start,Goal,m = readInput('input.txt')

#function:

imageOutput = 'map1.bmp'
fileOutput = 'output1.txt'
A_Star(H1_Manhattan)

imageOutput = 'map2.bmp'
fileOutput = 'output2.txt'
A_Star(H2_Euclid)

imageOutput = 'map3.bmp'
fileOutput = 'output3.txt'
A_Star(H3_Complex)

