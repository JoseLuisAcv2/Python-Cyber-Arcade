# 2-D Tile Map Engine
#
# By Jose Acevedo

import pygame
import os

def init():
    global DISPLAYSURF, windowWidth, windowHeight
    pygame.init()
    DISPLAYSURF  = pygame.display.get_surface()
    windowWidth  = DISPLAYSURF.get_width()
    windowHeight = DISPLAYSURF.get_height()

def getGameMap():
    return gameMap

def loadImage(fileName: str):
    return pygame.image.load(fileName)

def loadGameMap(line: str , gameMap: []):
    line = line.strip("[\n")
    gameMap.append(line.split())

def loadMapDecoration(line: str, mapDecoration: []):
    line    = line.strip("-\n").split()    
    decoObj = {}
    decoObj["name"]    = line[0]
    decoObj["y"]       = int(line[1])
    decoObj["x"]       = int(line[2])
    decoObj["offsetx"] = int(line[3])    
    decoObj["offsety"] = int(line[4])

    mapDecoration.append(decoObj)

def loadMap(mapFilePath: str):
    global gameMap, mapDecoration
    gameMap = []
    mapDecoration = []
    # Read map tile design and decoration from file
    with open(mapFilePath, "r") as mapFile:
        for line in mapFile.readlines():
            if line[0] == "[": # Ignore comment lines
                loadGameMap(line, gameMap)
            elif line[0] == "-":
                loadMapDecoration(line, mapDecoration)

def loadTileSet(tileSetFolderPath: str):
    global tileSet, TILE_WIDTH, TILE_HEIGHT

    tileSet = {} # Contains all tile images

    for tileFileName in os.listdir(tileSetFolderPath):
        tileName = tileFileName.split(".")[0] # Remove file extension
        tileSet[tileName] = loadImage(tileSetFolderPath + "/" + tileFileName)

    # Get width and height of tiles. All tiles should have the same size
    TILE_WIDTH  = 128
    TILE_HEIGHT = 128

def loadDecorationSet(decorationSetFolderPath: str):
    global decorationSet

    decorationSet = {} # Contains all decoration images
    for decorationFileName in os.listdir(decorationSetFolderPath):
        decorationName = decorationFileName.split(".")[0] # Remove file extension
        decorationSet[decorationName] = {}
        decorationSet[decorationName]["image"]  = loadImage(decorationSetFolderPath + "/" + decorationFileName)
        decorationSet[decorationName]["width"]  = decorationSet[decorationName]["image"].get_rect().width
        decorationSet[decorationName]["height"] = decorationSet[decorationName]["image"].get_rect().height

def loadBackground(backgroundImageFilePath: str):
    global BACKGROUND_IMAGE, backgroundImageWidth, backgroundImageHeight
    BACKGROUND_IMAGE         = pygame.image.load(backgroundImageFilePath)
    backgroundImageWidth     = BACKGROUND_IMAGE.get_rect().width
    backgroundImageHeight    = BACKGROUND_IMAGE.get_rect().height

def drawMap(camerax: int, cameray: int):
    # Draw background
    drawBackground(camerax, cameray)

    # Draw tiles
    for i in range(len(gameMap)):
        for j in range(len(gameMap[i])):
            if gameMap[i][j] != "0":
                tilex = j*TILE_WIDTH  - camerax
                tiley = i*TILE_HEIGHT - cameray
                if isInsideCameraView(tilex, tiley, TILE_WIDTH, TILE_HEIGHT):
                    DISPLAYSURF.blit(tileSet[gameMap[i][j]], (tilex, tiley))

    # Draw decoration elements
    for decorationElement in mapDecoration:
        elementWidth  = decorationSet[decorationElement["name"]]["width"]
        elementHeight = decorationSet[decorationElement["name"]]["height"]
        elementy      = ((decorationElement["y"] + 1) * TILE_HEIGHT) - cameray - \
                          elementHeight + decorationElement["offsety"]
        elementx      = (decorationElement["x"] * TILE_WIDTH) - camerax + (TILE_WIDTH // 2) - \
                        (elementWidth // 2) + decorationElement["offsetx"]
                   
        if isInsideCameraView(elementx, elementy, elementWidth, elementHeight):
            DISPLAYSURF.blit(decorationSet[decorationElement["name"]]["image"], (elementx, elementy))

def drawBackground(camerax: int, cameray: int):
    repeatBackgroundImage = int(windowWidth / backgroundImageWidth) + 1
    for i in range(repeatBackgroundImage):
            DISPLAYSURF.blit(BACKGROUND_IMAGE, (i*backgroundImageWidth, 0))

def isInsideCameraView(objx: int, objy: int, objWidth: int, objHeight: int):
    if   0 > objx + objWidth:
        return False
    elif windowWidth < objx:
        return False
    elif 0 > objy + objHeight:
        return False
    elif windowHeight < objy:
        return False
    else:
        return True