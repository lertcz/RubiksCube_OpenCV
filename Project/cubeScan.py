# Import essential libraries
from cv2 import bitwise_and
import requests
import cv2
import numpy as np
import imutils

from rubik_solver import utils
from rubik_solver.CubieCube import DupedEdge, DupedCorner

# popup
import tkinter as tk
from tkinter import simpledialog

#left, front, right, back, up, down
# CFOP
CUBE = [[[0, 0, 0], [0, 3, 0], [0, 0, 0]],
        [[0, 0, 0], [0, 4, 0], [0, 0, 0]],
        [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
        [[0, 0, 0], [0, 2, 0], [0, 0, 0]],
        [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        [[0, 0, 0], [0, 5, 0], [0, 0, 0]]]

scanned = [False for _ in range(6)]
notationCFOP = {
    0: "w", # white  >
    1: "r", # red    >
    2: "b", # blue   >
    3: "o", # orange >
    4: "g", # green  >
    5: "y"  # yellow >
}
notationKociemba = {
    0: "y", # white  >
    1: "g", # red    >
    2: "o", # blue   >
    3: "b", # orange >
    4: "r", # green  >
    5: "w"  # yellow >
}

WHITE = (255, 255, 255)
RED = (0, 0, 255)
BLUE = (255, 0, 0)
ORANGE = (0, 128, 255)
GREEN = (0, 255, 0)
YELLOW = (0, 255, 255)

SIDES = [WHITE, RED, BLUE, ORANGE, GREEN, YELLOW]

#white = [[180, 255, 255], [0, 0, 50]]
#red1 = [[180, 255, 255], [159, 50, 70]]
red2 = [[9, 255, 255], [0, 50, 70]] #cube red is in range 2
blue = [[128, 255, 255], [90, 50, 70]]
orange = [[24, 255, 255], [10, 50, 70]]
green = [[89, 255, 255], [36, 50, 70]]
yellow = [[35, 255, 255], [25, 50, 70]]

colors = [red2, blue, orange, green, yellow]

# image
def getIP():
    #IP popup ---------------------------
    root = tk.Tk()

    #hide the root
    root.withdraw()

    # the input dialog
    USER_INP = simpledialog.askstring(title="IP",
                                    prompt="What's your cam IP?")

    return USER_INP

def getURL_image():
    try:
        #url = "http://" + getIP() + "/shot.jpg"
        url = "http://192.168.1.109:8080/shot.jpg"
        img_resp = requests.get(url) #get image from url
        img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
        img = cv2.imdecode(img_arr, -1)
        img = imutils.resize(img, width=750, height=1800) #resize img
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE) #rotate 90deg

        return img

    except requests.exceptions.ConnectionError:
        print("Invalid IP, terminating session")
        print(url)
        quit(1)

def colorSelector(img, HSV):
    x = 80
    y = 200
    w = h = 16
    space = 100
    side = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    
    #loop trough 9 squares
    for i in range(3):
        offsetX = (w + space) * i
        for j in range(3):
            offsetY = (h + space) * j
            colorChoice = WHITE

            #loop trough masks
            for id, values in enumerate(colors):
                lower = np.array(values[1])
                upper = np.array(values[0])

                mask = cv2.inRange(HSV, lower, upper)
                
                #if mask corespond to color return it (white is base)
                if mask[y + offsetY + 8][x + offsetX + 8]:
                    side[j][i] = id+1
                    colorChoice = SIDES[id+1]
                    break
            
            cv2.rectangle(img, (x + offsetX, y + offsetY), (x + w + offsetX, y + h + offsetY), colorChoice, 2)
            
    
    return side

def createNotationAndSolve(visualization: bool):
    cubeNotation = ""
    #left, front, right, back, up, down
    #CFOP 5, 3, 2, 1, 0, 4
    #Kociemba 4, 0, 1, 2, 3, 5
    for num in [4, 0, 1, 2, 3, 5]:
        for i in range(3):
            for j in range(3):
                if visualization:
                    cubeNotation += notationCFOP[CUBE[num][i][j]]
                else:
                    cubeNotation += notationKociemba[CUBE[num][i][j]]
    
    if visualization:
        return cubeNotation
    else:
        print(cubeNotation)
        try:
            return [str(move) for move in utils.solve(cubeNotation, 'Kociemba')]
        except DupedEdge or DupedCorner:
            print("duplicate Edge!")

def previewCFOP(side = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]):  #redundant
    w = 30
    h = 30
    space = 10
    bigSpace = 30

    cubeSize = (w + space)*3 - space

    x = bigSpace
    y = bigSpace*2 + cubeSize


    previewWindow = np.zeros((470, 590, 3), np.uint8)

    #change scanned side
    #cube order: left, front, right, back, up, down
    if side:
        center = side[1][1]

        if center == 3:   # left      ORANGE
            CUBE[0] = side
            scanned[0] = True
        elif center == 4: # front     GREEN
            CUBE[1] = side
            scanned[1] = True
        elif center == 1: # right     RED
            CUBE[2] = side
            scanned[2] = True
        elif center == 2: # back      BLUE
            CUBE[3] = side
            scanned[3] = True
        elif center == 0: # up        WHITE
            CUBE[4] = side
            scanned[4] = True
        elif center == 5: # bottom    YELLOW
            CUBE[5] = side
            scanned[5] = True

    #left front right back
    for face in range(4):
        for i in range(3):
            offsetX = (w + space) * i + ((3* (w + space) - space + bigSpace) * face)
            for j in range(3):
                offsetY = (h + space) * j
                cv2.rectangle(previewWindow, (x + offsetX, y + offsetY), (x + w + offsetX, y + h + offsetY), SIDES[CUBE[face][j][i]], -1)
    
    #up
    x = bigSpace*2 + cubeSize
    for i in range(3):
        y = bigSpace
        offsetX = (w + space) * i
        for j in range(3):
            offsetY = (h + space) * j
            cv2.rectangle(previewWindow, (x + offsetX, y + offsetY), (x + w + offsetX, y + h + offsetY), SIDES[CUBE[4][j][i]], -1)
    #down
    for i in range(3):
        y = bigSpace*3 + cubeSize*2
        offsetX = (w + space) * i
        for j in range(3):
            offsetY = (h + space) * j
            cv2.rectangle(previewWindow, (x + offsetX, y + offsetY), (x + w + offsetX, y + h + offsetY), SIDES[CUBE[5][j][i]], -1)

    cv2.imshow("preview", previewWindow)

def previewKociemba(side = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]):
    w = 30
    h = 30
    space = 10
    bigSpace = 30

    cubeSize = (w + space)*3 - space

    x = bigSpace
    y = bigSpace*2 + cubeSize


    previewWindow = np.zeros((470, 590, 3), np.uint8)

    #change scanned side
    #cube order: left, front, right, back, up, down
    if side:
        center = side[1][1]

        if center == 2:   # left      BLUE
            CUBE[0] = side
            scanned[0] = True
        elif center == 1: # front     RED
            CUBE[1] = side
            scanned[1] = True
        elif center == 4: # right     GREEN
            CUBE[2] = side
            scanned[2] = True
        elif center == 3: # back      ORANGE
            CUBE[3] = side
            scanned[3] = True
        elif center == 5: # up        YELLOW
            CUBE[4] = side
            scanned[4] = True
        elif center == 0: # bottom    WHITE
            CUBE[5] = side
            scanned[5] = True

    #left front right back
    for face in range(4):
        for i in range(3):
            offsetX = (w + space) * i + ((3* (w + space) - space + bigSpace) * face)
            for j in range(3):
                offsetY = (h + space) * j
                cv2.rectangle(previewWindow, (x + offsetX, y + offsetY), (x + w + offsetX, y + h + offsetY), SIDES[CUBE[face][j][i]], -1)
    
    #up
    x = bigSpace*2 + cubeSize
    for i in range(3):
        y = bigSpace
        offsetX = (w + space) * i
        for j in range(3):
            offsetY = (h + space) * j
            cv2.rectangle(previewWindow, (x + offsetX, y + offsetY), (x + w + offsetX, y + h + offsetY), SIDES[CUBE[4][j][i]], -1)
    #down
    for i in range(3):
        y = bigSpace*3 + cubeSize*2
        offsetX = (w + space) * i
        for j in range(3):
            offsetY = (h + space) * j
            cv2.rectangle(previewWindow, (x + offsetX, y + offsetY), (x + w + offsetX, y + h + offsetY), SIDES[CUBE[5][j][i]], -1)

    cv2.imshow("preview", previewWindow)


def scan():
    previewCFOP(None)          

    # While loop to continuously fetching data from the Url
    while True:
        img = getURL_image()
        #img = testIMG() #base image
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) #HSV image
        imgHSV = cv2.medianBlur(imgHSV, 81, 1) #blur the image

        side = colorSelector(img, imgHSV)

        #draw images and masks
        cv2.imshow("Android_cam", img)

        # Press Esc key to exit
        if cv2.waitKey(1) == 27:
            break

        if cv2.waitKey(33) == ord(" "):
            previewCFOP(side)
        
        if cv2.waitKey(33) == ord("s"):
            if False not in scanned:
                cv2.destroyAllWindows()
                moves = createNotationAndSolve(False)
                return [createNotationAndSolve(True), moves]
            else:
                print("Need all sides scanned!")

cv2.destroyAllWindows()