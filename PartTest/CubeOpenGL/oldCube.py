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

BLACK = (0, 0, 0)

def rotate(turn):
    ORIENTATION = 1
    MAX = 90
    TRANSLATE = [0, 0, 0]
    AXIS = [0, 0, 0]
    SIDE_CONDITION = NONE

    if "'" in turn:
        ORIENTATION *= -1
        MAX *= -1
    elif "2" in turn:
        MAX = 180
    
    if "R" in turn:
        TRANSLATE = [0, 1.5, 1.5]
        AXIS = [1, 0, 0]
        SIDE_CONDITION = ["X", 2]

    elif "L" in turn:
        TRANSLATE = [0, 1.5, 1.5]
        AXIS = [1, 0, 0]
        SIDE_CONDITION = ["X", 0]

    elif "U" in turn:
        TRANSLATE = [1.5, 0, 1.5]
        AXIS = [0, 1, 0]
        SIDE_CONDITION = ["Y", 2]

    elif "D" in turn:
        TRANSLATE = [1.5, 0, 1.5]
        AXIS = [0, 1, 0]  
        SIDE_CONDITION = ["Y", 0]

    elif "F" in turn:
        TRANSLATE = [1.5, 1.5, 0]
        AXIS = [0, 0, 1]
        SIDE_CONDITION = ["Z", 2]

    elif "B" in turn:
        TRANSLATE = [1.5, 1.5, 0]
        AXIS = [0, 0, 1]
        SIDE_CONDITION = ["Z", 0]

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
    glLineWidth(5)
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
def DrawCube(rotation=None):
    points = [0, 1, 2] #set points of cube
    TURN_DEGREE = 0 #
    
    while True:
        #clear the canvas
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        glPushMatrix()
        if rotation:
            ORIENTATION, MAX, AXIS, TRANSLATE, SIDE_CONDITION = rotate(rotation)
            SIDE, VALUE = SIDE_CONDITION
        
        for z in points:
            for y in points:
                for x in points:
                    if SIDE == "X":
                        if x != VALUE:
                            cubie([x, y, z])
                    elif SIDE == "Y":
                        if y != VALUE:
                            cubie([x, y, z])
                    elif SIDE == "Z":
                        if z != VALUE:
                            cubie([x, y, z])
                    


        if rotation:    
            #unpack value
            glTranslate(*TRANSLATE)
            glRotate(TURN_DEGREE, *AXIS)
            glTranslate(*[-axis for axis in TRANSLATE])

            #increment the turn degree
            TURN_DEGREE += ONE_STEP * ORIENTATION

        for z in points:
            for y in points:
                for x in points:
                    if SIDE == "X":
                        if x == VALUE:
                            cubie([x, y, z])
                    elif SIDE == "Y":
                        if y == VALUE:
                            cubie([x, y, z])
                    elif SIDE == "Z":
                        if z == VALUE:
                            cubie([x, y, z])
        glPopMatrix()

        #update screen
        pygame.display.flip()
        #delay
        pygame.time.wait(10)

        if TURN_DEGREE == MAX + (ONE_STEP * ORIENTATION):
            break

def wait_for_input():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            if event.type == pygame.K_SPACE:
                pass

def twist():
    pass

def main():
    #pygame
    pygame.init()
    display = (800, 600) # display size
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL) # set pygame to be ready for 3 axis (3D)
    pygame.display.set_caption('Cube visualizer')

    #openGL
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glEnable(GL_DEPTH_TEST)
    #glEnable(GL_CULL_FACE)
    
    #setup the view of the cube
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

            #draw the cube and animate current turn
            DrawCube(turn)

            #delay between turns
            pygame.time.wait(250)
        
        while True:
            LEAVE = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                
                if event.type == pygame.K_SPACE:
                    LEAVE = False
            
            if LEAVE:
                break

main()