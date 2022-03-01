import time
import logging
logging.basicConfig(level=logging.DEBUG)
import numpy as np
import pathlib

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

filePath = str(pathlib.Path(__file__).parent.resolve())

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

colors = {
    "b": (0, 0, 1), #Blue
    "o": (1, 0.5, 0), #Orange
    "g": (0, 1, 0), #Green
    "r": (1, 0, 0), #Red
    "w": (1, 1, 1), #White
    "y": (1, 1, 0), #Yellow
    "B": (0, 0, 0)  #Black
}

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

rotation_table = {
    "U": [0, [1, 2, 3, 4]],
    "L": [1, [4, 5, 2, 0]],
    "F": [2, [1, 5, 3, 0]],
    "R": [3, [2, 5, 4, 0]],
    "B": [4, [3, 5, 1, 0]],
    "D": [5, [1, 2, 3, 4]],
}

color_lookup_table = { # >:D
    #color coordinates to find colors on surface of the cube
    #SIDES   B     L     F     R     U     D

    # layer 0
    "200": [None, 17, 24, None, None, 45], # c
    "201": [None, None, 25, None, None, 46], # e
    "202": [None, None, 26, 33, None, 47], # c
    "210": [None, 14, 21, None, None, None], # e
    "211": [None, None, 22, None, None, None], # center
    "212": [None, None, 23, 30, None, None], # e
    "220": [None, 11, 18, None, 6, None], # c
    "221": [None, None, 19, None, 7, None], # e
    "222": [None, None, 20, 27, 8, None], # c
    # layer 1
    "100": [None, 16, None, None, None, 48],      # e
    "101": [None, None, None, None, None, 49],    # center
    "102": [None, None, None, 34, None, 50],      # e
    "110": [None, 13, None, None, None, None],    # center
    "111": [None, None, None, None, None, None],  # core
    "112": [None, None, None, 31, None, None],    # center
    "120": [None, 10, None, None, 3, None],  # e
    "121": [None, None, None, None, 4, None],     # center
    "122": [None, None, None, 28, 5, None],  # e
    # layer 2
    "000": [44, 15, None, None, None, 53],     # c
    "001": [43, None, None, None, None, 50],     # e
    "002": [42, None, None, 35, None, 47],       # c
    "010": [41, 12, None, None, None, None], # e
    "011": [40, None, None, None, None, None],   #center
    "012": [39, None, None, 32, None, None],     # e
    "020": [38, 9, None, None, 0, None],         # c #
    "021": [37, None, None, None, 1, None],      # e
    "022": [36, None, None, 29, 2, None],        # c

}

def drawMove(x, y, text):
    textSurface = font.render(text, True, (255, 255, 255, 255)).convert_alpha()
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glWindowPos2d(x, y)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

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
def cubie(coords, cubeColors):
    #create verticies - points
    x, y, z = coords
    strCoords = str(z) + str(y) + str(x)

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
    c = 0
    
    for surface in surfaces:
        for vertex in surface:
            color = colors["B"]
            if color_lookup_table[strCoords][c] != None:
                colorCoord = color_lookup_table[strCoords][c]

                face = colorCoord // 9
                row = colorCoord // 3 % 3
                col = colorCoord % 3

                extractedColor = cubeColors[face][row][col]
                color = colors[extractedColor]
            

            glColor3fv(color)
            glVertex3fv(verticies[vertex])
        c += 1
    glEnd()

    #draw the outline
    glLineWidth(5)
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glColor3fv(colors["B"])
            glVertex3fv(verticies[vertex])
    
    glEnd()

class Big_Cube_model:
    def __init__(self, CubeColors: str, TurnSet: list) -> None:
        self.display = 0

        self.curr_update = self.__basic_state_update

        # pause duration in ticks
        self.pause_duration = 60
        self.pause_start = 0

        # curr_rotation is string representing value to be parsed by rotation_string_parser
        # parsed_rot_dat is list containing parsed value by rotation_string_parser
        # turn degree ...
        self.curr_rotation = None
        self.parsed_rot_dat = []
        self.turn_degree = 0

        # all_points is list containing Cartesian product -- (0, 1, 2) x (0, 1, 2) x (0, 1, 2)
        self.all_points = [None]*27
        points = (0, 1, 2)
        for z in points:
            for y in points:
                for x in points:
                    self.all_points[9*z + 3*y + x] = [x,y,z]

        # load the tile colors
        self.CubeColors = self.__loadColors(CubeColors)

        # load the sequence
        self.TurnSet = TurnSet
        self.nextTurn = 1

        # play the first animation
        self.add_rotation(self.TurnSet[0])
    
    def __loadColors(self, colors: str) -> list:
        """
        CDS: wwwwwwwwwooooooooogggggggggrrrrrrrrrbbbbbbbbbyyyyyyyyy,
        unpack the cube definition string into faces, rows and columns
        """
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

        return np.array([[[colors[face*9 + row*3 + col] for col in range(3)] for row in range(3)] for face in range(6)])

    def update(self,tick):
        """
        calls function saved in curr_update
        """
        self.curr_update(tick)

    def __basic_state_update(self):
        """
        draws base model
        """
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glPushMatrix()

        for point in self.all_points:
            cubie(point, self.CubeColors)
        
        glPopMatrix()

        #update screen
        pygame.display.flip()

    def __rotation_animation_update(self,tick):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glPushMatrix()

        ORIENTATION, MAX, AXIS, TRANSLATE, SIDE_CONDITION = self.parsed_rot_dat
        SIDE, VALUE = SIDE_CONDITION

        #draw text
        drawMove(100, 100, self.TurnSet[self.nextTurn-1])
        
        # 1 2 3 6 | 90 must be divided by the number without reminder
        # amout of degrees moved per update
        ONE_STEP = 3

        for x,y,z in self.all_points:
            if SIDE == "X":
                if x != VALUE:
                    cubie([x, y, z], self.CubeColors)
            elif SIDE == "Y":
                if y != VALUE:
                    cubie([x, y, z], self.CubeColors)
            elif SIDE == "Z":
                if z != VALUE:
                    cubie([x, y, z], self.CubeColors)

        #unpack value
        glTranslate(*TRANSLATE)
        glRotate(self.turn_degree, *AXIS)
        glTranslate(*[-axis for axis in TRANSLATE])

        #increment the turn degree
        self.turn_degree += ONE_STEP * ORIENTATION

        for x,y,z in self.all_points:
            if SIDE == "X":
                if x == VALUE:
                    cubie([x, y, z], self.CubeColors)
            elif SIDE == "Y":
                if y == VALUE:
                    cubie([x, y, z], self.CubeColors)
            elif SIDE == "Z":
                if z == VALUE:
                    cubie([x, y, z], self.CubeColors)

        #update screen
        pygame.display.flip()

        if self.turn_degree == MAX + (ONE_STEP * ORIENTATION):
            logging.info('Animation complete')
            # reset rotation
            self.turn_degree = 0

            # load next animation
            if self.nextTurn < len(self.TurnSet):
                # rotate colors after rotation
                self.__rotateFace_Color(self.TurnSet[self.nextTurn-1])
                # rotate
                self.add_rotation(self.TurnSet[self.nextTurn])
                # increment nextTurn
                self.nextTurn += 1
            
            # if all animations have been played STOP
            else:
                self.__rotateFace_Color(self.TurnSet[self.nextTurn-1])
                self.curr_update = self.__do_nothing_update

        glPopMatrix()

    def __do_nothing_update(self,tick):
        """
        does nothing, is saved to curr_update if there is no change happening
        """
        pass

    def basic_state(self):
        """
        Draws basic state of model, updates curr_update
        """
        self.__basic_state_update()
        self.curr_update = self.__do_nothing_update

    def add_rotation(self,rotation: str):
        """
        calls rotation_string_parser on str rotation, then saves data and starts animation
        """
        logging.info(f"Rotation added {rotation}")
        self.parsed_rot_dat = rotation_string_parser(rotation)
        self.curr_update = self.__rotation_animation_update

    def __rotateFace_Color(self, turn):
        cube = self.CubeColors
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

def visualize(COLORS, TURNS):
    print(COLORS, TURNS)
    global font

    #pygame
    pygame.init()
    display = (800, 600)
    gameScreen = pygame.display.set_mode(display, DOUBLEBUF|OPENGL) # set pygame to be ready for 3 axis
    pygame.display.set_caption('Cube visualizer')
    font = pygame.font.SysFont('arial', 64)

    #openGL
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glEnable(GL_DEPTH_TEST)

    #enable blending for text (transparent BG)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glTranslatef(0, -.5, -10)
    # front
    glRotate(20, 1, 0, 0)
    glRotate(-45, 0, 1, 0) 

    #debug
    #glTranslatef(0, -.5, -10)
    # back
    #glRotate(-20, 1, 0, 0)
    #glRotate(135, 0, 1, 0) 
    
    
    Cube = Big_Cube_model(CubeColors=COLORS, TurnSet=TURNS)

    #Cube.basic_state()

    tick = 0
    tps = 30
    tick_rate = 1/tps
    test_sample = 100
    loop_timer_begin = time.time()
    running_perf_average = 0

    #Cube.add_rotation(TURNS[0])

    is_running = True
    while is_running:
        loop_timer_begin = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

        #draw the cube
        Cube.update(tick=tick)

        tick+=1
        loop_timer_end = time.time()
        delta = (loop_timer_end - loop_timer_begin)
        running_perf_average += delta

        # if set tick rate (1/tps) is greater than loop time
        delta = tick_rate - delta
        if delta > 0:
            time.sleep(delta)

        # measures time per test_sample
        if not (tick % test_sample):
            # convert from s to ms
            running_perf_average = (running_perf_average) * 1000 / test_sample
            logging.debug(f"Tick: {tick}, avg time {running_perf_average:.5f} ms")
            running_perf_average = 0
    
    pygame.quit()
    quit()