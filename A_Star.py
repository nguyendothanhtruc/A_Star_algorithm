from PIL import Image
import numpy as np


class Node:
    x : int= None
    y : int= None
    gn : float = None
    fn : float = None
    hn : int = None
    parent = None

    def __init__(self,x,y):
        self.x = x
        self.y = y

        self.visited = 0
        
        self.fn = 0
        self.gn = 0
        self.hn = 0

    def isEqual(self,G):
        if self.x == G.x and self.y == G.y:
            return True
        return False



def convertToMatrix(filepath:str):
    #Open file bitmap => convert to array greyscale
    img = Image.open(filepath)
    bitmap = img.convert("L")
    map = np.asarray(bitmap,dtype='int')
    bitmap.close()
    return map

def colorBMP(fileInput:str,fileOutput:str, S:Node, G:Node):
    img = Image.open(fileInput)

    color = (255,0,0)
    
    while not G.isEqual(S):
        img.putpixel((G.x,G.y),color)
        G = G.parent
    img.putpixel((G.x,G.y),color)

    img.save(fileOutput)

def writePath(fileInput:str,fileOutput:str, S:Node, G:Node):
    output = open('out.txt','w')

    output.write(str(G.gn))

    output.close()

    colorBMP(fileInput,fileOutput,S,G)


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

def d(A:Node,B:Node,map):
    deltaA = map[A.y][A.x] - map[B.y][B.x]
    
    AB = np.sqrt(np.square(B.x-A.x) + np.square(B.y - A.y))
 
    return AB + abs(deltaA)*(0.5*np.sign(deltaA)+1)

def checkHeight(A:Node, B:Node, m: int):
    deltaA = map[A.y][A.x] - map[B.y][B.x]
    if abs(deltaA) <= m:
        return True
    return False

def H1_Manhattan(A:Node, B:Node, map):
    return abs(A.x-B.x)+abs(A.y-B.y) + abs(map[A.y][A.x] - map[B.y][B.x])#d(A,B,map)#

def H2_Euclid(A:Node, B:Node):
    return np.sqrt(np.square(A.x-B.x)+np.square(A.y-B.y))

def isIn(list, G:Node):
    for item in list:
        if item.x == G.x and item.y == G.y:
            return True,item

    return False,G
def isHere(list,G:Node):
    if list[G.y][G.x]>0:
        return True, G

def generateSuccessor(currentNode:Node):
    #Current_node coordinates
    x = currentNode.x
    y = currentNode.y

    row, column = map.shape 

    successor = []
    #Generates successors
    if y-1 > 0: #If not top border
        A = Node(x, y-1)
        if (checkHeight(currentNode,A,m)):
            successor.append(A)

        if x + 1 < column: #If not right border
            A = Node(x+1,y-1)
            if (checkHeight(currentNode,A,m)):
                successor.append(A)

            A = Node(x+1,y)
            if (checkHeight(currentNode,A,m)):
                successor.append(A)

        if x - 1 > 0: #If not left border
            A = Node(x-1,y-1)
            if (checkHeight(currentNode,A,m)):
                successor.append(A)

            A = Node(x-1,y)
            if (checkHeight(currentNode,A,m)):
                successor.append(A)   

    #If not bottom border
    if y + 1 < row: 
        A = Node(x,y+1)
        if (checkHeight(currentNode,A,m)):
            successor.append(A)

        if x + 1 < column:  #If not right border
            A = Node(x+1,y+1)
            if (checkHeight(currentNode,A,m)):
                successor.append(A)

        if x - 1 > 0:   #If not left border
            A = Node(x-1,y+1)
            if (checkHeight(currentNode,A,m)):
                successor.append(A)
        
    #If not right border
    if x + 1 < column: 
        A = Node(x+1,y)
        if (checkHeight(currentNode,A,m)):
                successor.append(A)

    #If not left border
        if x - 1 > 0: 
            A = Node(x-1,y)
            if (checkHeight(currentNode,A,m)):
                successor.append(A)  

    return successor   

def A_Star(map:np.array,S:Node,G:Node, m:int, heuristic,fileInput, fileOutput):
    queue:list = [] #open list
    row,col=map.shape
    closed_list=np.zeros((row,col))

    #Put S to open_list
    queue.append(S)
    S.fn = heuristic(S,G,map)


    currentNode:Node

    #While open_list is not empty
    dup=closed_list
    while (queue):
        currentNode = queue[0]

        #Reach goal -> draw path
        if currentNode.isEqual(G): 
            return writePath(fileInput, fileOutput, S,currentNode)

        successor = generateSuccessor(currentNode)

        #For each node in successros[]
        for node in successor:
            #Calculate successors.f(n)
            successor_cost = currentNode.gn + d(currentNode,node,map)

            check,node = isIn(queue,node)
            if check:
                if node.gn <= successor_cost: continue

            else: 
                #check,node = isIn(closed_list,node)
                check=isHere(closed_list,node)
                if check:
                    if node.gn <= successor_cost: 
                        continue

                    queue.append(node)

                   # closed_list.remove(node)
                    closed_list[node.y][node.x]=0
 

                else:
                	node.hn = heuristic(node,G,map) #heuristic 

                	queue.append(node)

            node.gn = successor_cost
            node.fn = node.gn + node.hn
            node.parent = currentNode
               
        #Add current_node to closed list
        #closed_list.append(currentNode)
        closed_list[currentNode.y][currentNode.x]=currentNode.gn

        #Remove current node from open_list
        queue.remove(currentNode)


        #Sort queue according to f(n) value
        queue.sort(key = lambda Node: Node.fn)
        #test
        dup=closed_list


    #If the last node is not goal -->No solution or error
    if currentNode != G: print ("Can not find solution")
    print(dup)

#MAIN:

map = convertToMatrix('map.bmp')
print(map)


S,G,m = readInput('input.txt')


A_Star(map,S,G,m,H1_Manhattan,'map.bmp', 'out.bmp')


#colorBMP('map.bmp','new.bmp')
