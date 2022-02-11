from ctypes import pointer
from multiprocessing.dummy import current_process
from pickle import NONE

import time
import logging
logging.basicConfig(level=logging.DEBUG)
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


class Big_Cube_model:
    def __init__(self) -> None:
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
        self.turn_degree = 90

        # all_points is list containing Cartesian product -- (0, 1, 2) x (0, 1, 2) x (0, 1, 2)
        self.all_points = [None]*27
        points = (0, 1, 2)
        for z in points:
            for y in points:
                for x in points:
                    self.all_points[9*z + 3*y + x] = [x,y,z]

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
            cubie(point)
        
        glPopMatrix()

        #update screen
        pygame.display.flip()

    def __rotation_animation_update(self,tick):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glPushMatrix()

        ORIENTATION, MAX, AXIS, TRANSLATE, SIDE_CONDITION = self.parsed_rot_dat
        SIDE, VALUE = SIDE_CONDITION
        
        ONE_STEP = 1

        for x,y,z in self.all_points:
            if SIDE == "X":
                if x != VALUE:
                    cubie([x, y, z])
            elif SIDE == "Y":
                if y != VALUE:
                    cubie([x, y, z])
            elif SIDE == "Z":
                if z != VALUE:
                    cubie([x, y, z])

        #unpack value
        glTranslate(*TRANSLATE)
        glRotate(self.turn_degree, *AXIS)
        glTranslate(*[-axis for axis in TRANSLATE])

        #increment the turn degree
        self.turn_degree += ONE_STEP * ORIENTATION

        for x,y,z in self.all_points:
            if SIDE == "X":
                if x == VALUE:
                    cubie([x, y, z])
            elif SIDE == "Y":
                if y == VALUE:
                    cubie([x, y, z])
            elif SIDE == "Z":
                if z == VALUE:
                    cubie([x, y, z])

        #update screen
        pygame.display.flip()

        if self.turn_degree <= MAX + (ONE_STEP * ORIENTATION):
            logging.info('Animation complete')
            self.turn_degree = MAX
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
    
    Cube = Big_Cube_model()
    TURNS = ["U", "U'", "U2", "L", "L'", "L2", "F", "F'", "F2", "R", "R'", "R2", "B", "B'", "B2", "D", "D'", "D2"]
    Cube.add_rotation("R2")

    tick = 0
    tps = 30
    tick_rate = 1/tps
    test_sample = 100
    loop_timer_begin = time.time()
    running_perf_average = 0

    #Cube.basic_state()

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

if __name__ == "__main__":
    main()