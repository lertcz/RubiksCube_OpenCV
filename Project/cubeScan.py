# Import essential libraries
import requests
import cv2
import numpy as np
import imutils

from rubik_solver import utils
from rubik_solver.CubieCube import DupedEdge, DupedCorner

# popup
import tkinter as tk
from tkinter import simpledialog

# visualize
import visualizeSolve as VS

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
    0: "w",
    1: "r",
    2: "b",
    3: "o",
    4: "g",
    5: "y"
}
notationKociemba = {
    0: "y",
    1: "g",
    2: "o",
    3: "b",
    4: "r",
    5: "w"
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
                                    prompt="What's your cam IP?\nhttp://_____:8080")
    return USER_INP

def getURL_image(url):
    try:
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

def createNotationAndSolve():
    cubeNotation = ""
    algNotation = ""
    #left, front, right, back, up, down
    #Kociemba 4, 0, 1, 2, 3, 5
    for num in [4, 0, 1, 2, 3, 5]:
        for i in range(3):
            for j in range(3):
                algNotation += notationKociemba[CUBE[num][i][j]] # notation for library
                cubeNotation += notationCFOP[CUBE[num][i][j]] # notation for visualizer
    
    try:
        return [cubeNotation, [str(move) for move in utils.solve(algNotation, 'Kociemba')]]
    except DupedEdge or DupedCorner:
        print("duplicate Edge or Corner!")

def previewCFOP(side = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]):
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


def scan():
    #get the url of the app server
    url = "http://" + getIP() + ":8080/shot.jpg"

    previewCFOP(None)          

    # While loop to continuously fetching data from the Url
    while True:
        img = getURL_image(url)
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) #convert to a HSV image
        imgHSV = cv2.medianBlur(imgHSV, 81, 1) #blur the image

        side = colorSelector(img, imgHSV)

        #draw the view + colors seen
        cv2.imshow("Android_cam", img)

        # Press Esc key to exit
        if cv2.waitKey(1) == 27:
            break

        if cv2.waitKey(33) == ord(" "):
            previewCFOP(side)
        
        if cv2.waitKey(33) == ord("s"):
            if False not in scanned:
                cv2.destroyAllWindows() #close all cv2 windows
                VS.visualize(*createNotationAndSolve()) # recieve colors and turns
            else:
                print("Need all sides scanned!")

if __name__ == '__main__':
    scan()