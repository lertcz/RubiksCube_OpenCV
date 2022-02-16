"""            ----------------
               | 0  | 1  | 2  |
               ----------------
               | 3  | 4  | 5  |
               ----------------
               | 6  | 7  | 8  |
               ----------------
-------------------------------------------------------------
| 9  | 10 | 11 | 18 | 19 | 20 | 27 | 28 | 29 | 36 | 37 | 38 |
---------------|--------------|--------------|---------------
| 12 | 13 | 14 | 21 | 22 | 23 | 30 | 31 | 32 | 39 | 40 | 41 |
---------------|--------------|--------------|---------------
| 15 | 16 | 17 | 24 | 25 | 26 | 33 | 34 | 35 | 42 | 43 | 44 |
-------------------------------------------------------------
               ----------------
               | 45 | 46 | 47 |
               ----------------
               | 48 | 49 | 50 |
               ----------------
               | 51 | 52 | 53 |
               ----------------                               """

""" total = [0, 4, 14, 21, 27, 39, 40, 51]

for pos in total:
    print()
    print(pos)
    col = pos % 9
    row = pos % 9 // 3 - 1
    face = (pos // 9 % 3)
    print(col, row, face) """

import numpy as np

# rotation test
""" cube = np.array([[['g', 'o', 'w'], ['g', 'y', 'y'], ['b', 'r', 'o']], 
                [['o', 'g', 'r'], ['b', 'b', 'g'], ['b', 'w', 'r']], 
                [['r', 'b', 'w'], ['o', 'r', 'w'], ['b', 'r', 'y']], 
                [['y', 'r', 'b'], ['g', 'g', 'w'], ['y', 'y', 'o']], 
                [['w', 'y', 'o'], ['o', 'o', 'w'], ['w', 'y', 'r']], 
                [['g', 'r', 'g'], ['b', 'w', 'o'], ['g', 'b', 'y']]]) """

cube = np.array([[['y', 'y', 'y'], ['y', 'y', 'y'], ['y', 'y', 'y']], 
                [['b', 'b', 'b'], ['b', 'b', 'b'], ['b', 'b', 'b']], 
                [['r', 'r', 'r'], ['r', 'r', 'r'], ['r', 'r', 'r']], 
                [['g', 'g', 'g'], ['g', 'g', 'g'], ['g', 'g', 'g']], 
                [['o', 'o', 'o'], ['o', 'o', 'o'], ['o', 'o', 'o']], 
                [['w', 'w', 'w'], ['w', 'w', 'w'], ['w', 'w', 'w']]])

""" cube = np.array([[[0, 0, 0], [0, 0, 0], [0, 0, 0]], 
                [[0, 0, 0], [0, 0, 0], [0, 0, 0]], 
                [[0, 0, 0], [0, 0, 0], [0, 0, 0]], 
                [[0, 0, 0], [0, 0, 0], [0, 0, 0]], 
                [[0, 0, 0], [0, 0, 0], [0, 0, 0]], 
                [[0, 0, 0], [0, 0, 0], [0, 0, 0]]]) """

#nummpy rot90
#-1  90
#1  -90
#2  180

rotation_table = {
    "U": [0, [1, 2, 3, 4]],
    "L": [1, [4, 5, 2, 0]],
    "F": [2, [1, 5, 3, 0]],
    "R": [3, [2, 5, 4, 0]],
    "B": [4, [3, 5, 1, 0]],
    "D": [5, [1, 2, 3, 4]],
}   

def rotateSide(turn):
    ROTATE = -1

    if len(turn) == 2:
        if turn[1] == "'":
            ROTATE = -3

        elif turn[1] == "2":
            ROTATE = -2

    #find and rotate the current face
    currentFace = rotation_table[turn[0]][0]
    cube[currentFace] = np.rot90(cube[currentFace], ROTATE)

    #create variables with each neighbouring face
    face1, face2, face3, face4 = rotation_table[turn[0]][1]

    for x in range(3):
        for _ in range(-ROTATE):
            if turn[0] == "U":
                temp = cube[face1][0][x]
                cube[face1][0][x] = cube[face2][0][x]
                cube[face2][0][x] = cube[face3][0][x]
                cube[face3][0][x] = cube[face4][0][x]
                cube[face4][0][x] = temp

            elif turn[0] == "L":
                temp = cube[face1][2-x][2]
                cube[face1][2-x][2] = cube[face2][x][0]
                cube[face2][x][0] = cube[face3][x][0]
                cube[face3][x][0] = cube[face4][x][0]
                cube[face4][x][0] = temp 

            elif turn[0] == "F":
                temp = cube[face1][x][2]
                cube[face1][x][2] = cube[face2][0][x]
                cube[face2][0][x] = cube[face3][2-x][0]
                cube[face3][2-x][0] = cube[face4][2][2-x]
                cube[face4][2][2-x] = temp

            elif turn[0] == "R":
                temp = cube[face1][x][2]
                cube[face1][x][2] = cube[face2][x][2]
                cube[face2][x][2] = cube[face3][2-x][0]
                cube[face3][2-x][0] = cube[face4][x][2]
                cube[face4][x][2] = temp 

            elif turn[0] == "B":
                temp = cube[face1][x][2]
                cube[face1][x][2] = cube[face2][2][2-x]
                cube[face2][2][2-x] = cube[face3][2-x][0]
                cube[face3][2-x][0] = cube[face4][0][x]
                cube[face4][0][x] = temp 

            elif turn[0] == "D":
                temp = cube[face4][2][x]
                cube[face4][2][x] = cube[face3][2][x]
                cube[face3][2][x] = cube[face2][2][x]
                cube[face2][2][x] = cube[face1][2][x]
                cube[face1][2][x] = temp
            

    
space = np.array([[""], [""], [""]])
def printCube():
    for x in range(3):
        print("\t       ", cube[0][x])
    print(np.concatenate((cube[1], space,  cube[2], space, cube[3], space, cube[4]), axis=1 ))
    for x in range(3):
        print("\t       ", cube[5][x])
    print()

printCube()
rotateSide("R")
rotateSide("U")
rotateSide("R'")
rotateSide("U'")
printCube()