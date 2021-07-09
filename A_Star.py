from PIL import Image
import numpy as np
import math as m

def convertToMatrix(filepath:str):
    #Open file bitmap -> store in bitmap 3D array
    img = Image.open(filepath)
    #[layer][row][column] <=> x,y,z
    bitmap = np.array(img)

    width,height = img.size
    
    map = np.empty((height,width), dtype='int')
    
    #Convert into 2D array 
    for i in range(height):
        for j in range(width):
            map[i][j] = bitmap[i][j][0]
    return map

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
    S = int(a), int(b)
    print(S)

    Line = input.readline()
    Line = Line.replace('(','')
    Line = Line.replace(')','')
    a,b = Line.split(';')
    G = int(a), int(b)
    print(G)

    Line = input.readline()
    m = int(Line)
    print(m)

    return S,G,m

def d(A,B,map):
    deltaA = map[A[0]][A[1]] - map[B[0]][B[1]]
    
    AB = np.sqrt(np.square(B[0]-A[0]) + np.square(B[1] - A[1]))
 
    return AB + abs(deltaA)*(0.5*np.sign(deltaA)+1)


#MAIN:

map = convertToMatrix('map.bmp')
#print(map)


S,G,m = readInput('input.txt')

distance = d(S,G,map)
print(distance)

#colorBMP('map.bmp','new.bmp')
