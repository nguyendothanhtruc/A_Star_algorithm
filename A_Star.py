from PIL import Image
import numpy as np


class Node:
    x : int= None
    y : int= None
    visited : bool = None
    gn : float = None
    fn : float = None
    hn : float = None
    parent = None

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.visited = 0
        self.fn = 0
        self.gn = 0
        self.hn = 0



def convertToMatrix(filepath:str):
    #Open file bitmap => convert to array greyscale
    img = Image.open(filepath)
    bitmap = img.convert("L")
    map = np.asarray(bitmap,dtype='int')
    bitmap.close()
    return map

    """"
    #[layer][row][column] <=> x,y,z
    bitmap = np.array(img)
    width,height = img.size
    
    map = np.empty((height,width), dtype='int')
    
    #Convert into 2D array 
    for i in range(height):
        for j in range(width):
            map[i][j] = bitmap[i][j][0]
    return map
    """

def colorBMP(fileInput:str,fileOutput:str):
    img = Image.open(fileInput)

    width,height = img.size

    color = (255,0,0)

    for x in range(height):
        for y in range(width):
            if x == y:
                img.putpixel((x,y), color)
    
    img.save(fileOutput)

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

def A_Star(map:np.array,S:Node,G:Node, m:int):
    queue:list = []
    closed_list : list = []

    queue.append(S)
    S.fn = d(S,G,map) #hẻuistic
    
    currentNode:Node
    row, column = map.shape

    while (queue):
        currentNode = queue[0]
        
        currentNode.fn = currentNode.gn + currentNode.hn

        if currentNode == G: return 'ok'

        x = currentNode.x
        y = currentNode.y

        successor = []
    
        if y-1 > 0:
            A = Node(x,y-1)
            if (checkHeight(currentNode,A,m)):
                successor.append(A)

            if x + 1 < column: 
                A = Node(x+1,y-1)
                if (checkHeight(currentNode,A,m)):
                    successor.append(A)

                A = Node(x+1,y)
                if (checkHeight(currentNode,A,m)):
                    successor.append(A)

            if x - 1 > 0: 
                A = Node(x-1,y-1)
                if (checkHeight(currentNode,A,m)):
                    successor.append(A)

                A = Node(x-1,y)
                if (checkHeight(currentNode,A,m)):
                    successor.append(A)   

        if y + 1 < row:
            A = Node(x,y+1)
            if (checkHeight(currentNode,A,m)):
                successor.append(A)

            if x + 1 < column: 
                A = Node(x+1,y+1)
                if (checkHeight(currentNode,A,m)):
                    successor.append(A)

            if x - 1 > 0:
                A = Node(x-1,y+1)
                if (checkHeight(currentNode,A,m)):
                    successor.append(A)
        
        for node in successor:
            successor_cost = currentNode.gn + d(currentNode,node,map)
            if node in queue:
                if node.gn <= successor_cost: break
            elif node in closed_list:
                if node.gn <= successor_cost: break

                node.gn = successor_cost
                node.parent = currentNode

                queue.append(node)
            else:
                node.gn = successor_cost
                node.hn = d(node,G,map) #heuristic 
                node.parent = currentNode

                queue.append(node)
               

        closed_list.append(currentNode)

        queue.remove(currentNode)

        queue.sort(key = lambda Node: Node.gn)


    if currentNode != G: return "Error"
                
                

        
        



#MAIN:

map = convertToMatrix('t.bmp')
print(map)
#S,G,m = readInput('in.txt')
A = Node(0,0)
B = Node(2,3)
m = 200
A_Star(map,A,B,m)


#colorBMP('map.bmp','new.bmp')
