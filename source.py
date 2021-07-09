from PIL import Image
import numpy as np

def convertToMatrix(filepath):
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



#MAIN:
map = convertToMatrix('t.bmp')
print(map)
print(map.shape)


