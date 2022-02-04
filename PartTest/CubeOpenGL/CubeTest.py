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

def cubie(coords):
    #create verticies - points
    x, y, z = coords
    verticies = [
        (x, -y, -z),
        (x, y, -z),
        (-x, y, -z),
        (-x, -y, -z),
        (x, -y, z),
        (x, y, z),
        (-x, -y, z),
        (-x, y, z)
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
    glLineWidth(10)
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glColor3fv(BLACK)
            glVertex3fv(verticies[vertex])
    
    glEnd()
    

def Cube():
    points = [0, 0.33, 0.66]
    for z in points:
        for y in points:
            for x in points:
                cubie([x, y, z])


def main():
    #pygame
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL) # set pygame to be ready for 3 axis
    pygame.display.set_caption('Cube visualizer')

    #openGL
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glEnable(GL_DEPTH_TEST);
    glTranslatef(0.0, 0.0, -5)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # get keys
        keypress = pygame.key.get_pressed()#Move using WASD

        # apply the movment
        if keypress[pygame.K_w]:
            glTranslatef(0, -0.1, 0)
        if keypress[pygame.K_s]:
            glTranslatef(0, 0.1, 0)
        if keypress[pygame.K_d]:
            glTranslatef(-0.1, 0, 0)
        if keypress[pygame.K_a]:
            glTranslatef(0.1, 0, 0)

        #glRotate(1, 3, 1, 1)

        #clear the canvas
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        #draw the cube
        Cube()

        pygame.display.flip()
        pygame.time.wait(10)

main()