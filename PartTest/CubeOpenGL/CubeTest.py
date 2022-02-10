from pickle import NONE
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

#initialize edges
edges = [
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 7),
    (6, 3),
    (6, 4),
    (6, 7),
    (5, 1),
    (5, 4),
    (5, 7)
]
#initialize surfaces
surfaces = [
    (0, 1, 2, 3),
    (3, 2, 7, 6),
    (6, 7, 5, 4),
    (4, 5, 1, 0),
    (1, 5, 7, 2),
    (4, 0, 3, 6)
]

colors = [
    (0, 0, 1), #Blue
    (1, 0.5, 0), #Orange
    (0, 1, 0), #Green
    (1, 0, 0), #Red
    (1, 1, 1), #White
    (1, 1, 0), #Yellow
]

translation_table = {
    "R" : (0, 1.5, 1.5),
    "L" : (0, 1.5, 1.5),
    "U" : (1.5, 0, 1.5),
    "D" : (1.5, 0, 1.5),
    "F" : (1.5, 1.5, 0),
    "B" : (1.5, 1.5, 0)
}

rotation_axis_table = {
    "R" : (1, 0, 0),
    "L" : (1, 0, 0),
    "U" : (0, 1, 0),
    "D" : (0, 1, 0),
    "F" : (0, 0, 1),
    "B" : (0, 0, 1)
}

side_condition_table = {
    "R" : ["X", 2],
    "L" : ["X", 0],
    "U" : ["Y", 2],
    "D" : ["Y", 0],
    "F" : ["Z", 2],
    "B" : ["Z", 0]
}

BLACK = (0, 0, 0)

def rotation_string_parser(input_str: str):
    ORIENTATION = 1
    MAX = 90

    if len(input_str) == 2:
        side, x = input_str

        if x == "'":
            ORIENTATION *= -1
            MAX *= -1

        elif x == "2":
            MAX = 180

    else:
        side = input_str

    TRANSLATE = translation_table[side]
    AXIS = rotation_axis_table[side]
    SIDE_CONDITION = side_condition_table[side]

    if SIDE_CONDITION[1] == 2:
        #fix the rotation like real cube
        ORIENTATION *= -1
        MAX *= -1
        #--------

    return [ORIENTATION, MAX, AXIS, TRANSLATE, SIDE_CONDITION]

SIZE = 1
def cubie(coords):
    #create verticies - points
    x, y, z = coords
    verticies = [
        (x+SIZE, y, z),
        (x+SIZE, y+SIZE, z),
        (x, y+SIZE, z),
        (x, y, z),
        (x+SIZE, y, z+SIZE),
        (x+SIZE, y+SIZE, z+SIZE),
        (x, y, z+SIZE),
        (x, y+SIZE, z+SIZE)
    ]

    #draw the plain
    glBegin(GL_QUADS)
    x = 0
    for surface in surfaces:
        for vertex in surface:
            glColor3fv(colors[x])
            glVertex3fv(verticies[vertex])
        x += 1

    glEnd()

    #draw the outline
    glLineWidth(5)
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glColor3fv(BLACK)
            glVertex3fv(verticies[vertex])
    
    glEnd()

ONE_STEP = 6
def Cube(rotation=None):
    points = [0, 1, 2]
    TURN_DEGREE = 0
    
    while True:
        #clear the canvas
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        glPushMatrix()
        ORIENTATION, MAX, AXIS, TRANSLATE, SIDE_CONDITION = rotation_string_parser(rotation)
        SIDE, VALUE = SIDE_CONDITION

        if SIDE == "X":
            for x in points:
                if x != VALUE:
                    for y in points:
                        for z in points:
                            cubie([x, y, z])
        
        elif SIDE == "Y":
            for y in points:
                if y != VALUE:
                    for x in points:
                        for z in points:
                            cubie([x, y, z])
        
        elif SIDE == "Z":
            for z in points:
                if z != VALUE:
                    for x in points:
                        for y in points:
                            cubie([x, y, z])
        
        if rotation:    
            #unpack value
            glTranslate(*TRANSLATE)
            glRotate(TURN_DEGREE, *AXIS)
            glTranslate(*[-axis for axis in TRANSLATE])

            #increment the turn degree
            TURN_DEGREE += ONE_STEP * ORIENTATION

        if SIDE == "X":
            for x in points:
                if x == VALUE:
                    for y in points:
                        for z in points:
                            cubie([x, y, z])
        
        elif SIDE == "Y":
            for y in points:
                if y == VALUE:
                    for x in points:
                        for z in points:
                            cubie([x, y, z])
        
        elif SIDE == "Z":
            for z in points:
                if z == VALUE:
                    for x in points:
                        for y in points:
                            cubie([x, y, z])

        glPopMatrix()

        #update screen
        pygame.display.flip()
        #delay
        pygame.time.wait(10)

        if TURN_DEGREE == MAX + (ONE_STEP * ORIENTATION):
            break

def main():
    #pygame
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL) # set pygame to be ready for 3 axis
    pygame.display.set_caption('Cube visualizer')

    #openGL
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glEnable(GL_DEPTH_TEST)
    glTranslatef(0, -0.5, -10)
    glRotate(20, 1, 0, 0)
    glRotate(-45, 0, 1, 0)
    
    TURNS = ["U", "U'", "U2", "L", "L'", "L2", "F", "F'", "F2", "R", "R'", "R2", "B", "B'", "B2", "D", "D'", "D2"]

    while True:
        for turn in TURNS:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            #draw the cube
            Cube(turn)
            pygame.time.wait(250)

        quit("turned em all muhahahaha")

if __name__ == "__main__":
    main()