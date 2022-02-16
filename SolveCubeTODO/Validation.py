from numpy import number
from CubeExceptions import *
from collections import Counter

sides = {"w", "o", "g", "r", "b", "y"}

# 0     Cube is solvable
# -1    Not all centers exist once
# -2    Not all 12 edges exist once
# -3    One edge is flipped
# -4    Not all 8 corners exist once
# -5    One corner is twisted
# -6    Parity error two corners or two edges have to be exchanged
# -7    Cube string should be 54 characters long

def validateString(cubeString):
    if len(cubeString) != 54:
        raise InappropriateCubeString("Lenght of the string should be 54 characters long")
    
    if set(cubeString) != sides:
        raise InappropriateCubeString("wrong")
    
    numberOfColors = Counter(cubeString).values()
    if len(set(numberOfColors)) != 1:
        raise InappropriateCubeString("Each color should apear 9 times")

def checkCenters(cubeString):
    
    centers = [cubeString[4+center*9] for center in range(6)]
    uniqueCenters = set(centers)
    
    if uniqueCenters != sides:
        raise DuplicateCenters("Not all centers exist once")

    if "".join(centers) != "wogrby":
        raise InappropriateCubeString("Make sure you scan the cube with green side in front and white on top") 
    
def checkCorners(cubeString):
    raise DuplicatedEdge("Not all 8 corners exist once")

def checkEdges(cubeString):
    raise DuplicatedEdge("Not all 12 edges exist once")

def flippedEdge(cubeString):
    raise FlipError("One edge is flipped")

def checkCornerTwist(cubeString):
    raise CornerTwist("One corner is twisted")

def checkParity(cubeString):
    raise Parity("Parity = two corners or two edges have to be exchanged")



    

def checkCube(cube):
    validateString(cube)
    checkCenters(cube)