import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

#setup verticies - points
verticies = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)
#setup edges
edges = (
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
)

def Cube():
    glBegin(GL_LINES)
    #create the cube
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    
    glEnd()

def move(mouseMove, up_down_angle):
    # get keys
    keypress = pygame.key.get_pressed()#Move using WASD

    """ # init model view matrix
    glLoadIdentity() """

    # apply the look up and down ////
    up_down_angle += mouseMove[1]*0.1
    glRotatef(up_down_angle, 1.0, 0.0, 0.0)

    """ # init the view matrix /////
    glPushMatrix()
    glLoadIdentity() """

    # apply the movment
    if keypress[pygame.K_w]:
        glTranslatef(0, 0, 0.1)
    if keypress[pygame.K_s]:
        glTranslatef(0, 0, -0.1)
    if keypress[pygame.K_d]:
        glTranslatef(-0.1, 0, 0)
    if keypress[pygame.K_a]:
        glTranslatef(0.1, 0, 0)
    
    # apply the left and right rotation
    glRotatef(mouseMove[0]*0.1, 0.0, 1.0, 0.0)

    """ # multiply the current matrix by the get the new view matrix and store the final vie matrix 
    glMultMatrixf(viewMatrix)
    viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

    # apply view matrix /////
    glPopMatrix()
    glMultMatrixf(viewMatrix) """

    

def main():
    #pygame
    pygame.init()
    display = (800, 600)
    scree = pygame.display.set_mode(display, DOUBLEBUF|OPENGL) # set pygame to be ready for 3 axis
    pygame.display.set_caption('Cube visualizer')
    pygame.mouse.set_visible(False) # hide the mouse

    #openGL
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)
    glRotate(0, 0, 0, 0)

    #movement
    # init mouse movement and center mouse on screen
    displayCenter = [scree.get_size()[i] // 2 for i in range(2)]
    pygame.mouse.set_pos(displayCenter)

    """ glMatrixMode(GL_MODELVIEW)
    gluLookAt(0, -8, 0, 0, 0, 0, 0, 0, 1)
    viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
    glLoadIdentity() """

    # loop variables
    mouseMove = [0, 0]
    up_down_angle = 0.0
    paused = False
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            #rotation and movement
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    run = False
                if event.key == pygame.K_PAUSE or event.key == pygame.K_p:
                    paused = not paused
                    pygame.mouse.set_visible(paused)
                    pygame.mouse.set_pos(displayCenter)  
            if event.type == pygame.MOUSEMOTION:
                mouseMove = [event.pos[i] - displayCenter[i] for i in range(2)]
                if not paused:
                    pygame.mouse.set_pos(displayCenter)  
            
        
        if not paused:
            move(mouseMove, up_down_angle)#, viewMatrix)

            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

            Cube()

            pygame.display.flip()
            pygame.time.wait(10)

main()