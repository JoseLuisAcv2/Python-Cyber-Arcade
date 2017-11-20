# Shooter
#
# By Jose Acevedo
#
# © Copyright 2015.

import pygame
import sys
import os
import tileMapEngine
import collisionEngine
from pygame.locals import *

### GAME SETTINGS ###
ACTION_TYPES            = ["moveRight", "moveLeft", "jump"]
CONTINUOUS_ACTION_TYPES = ["moveRight", "moveLeft"]

### DISPLAY SETTINGS ###
FPS                        = 30
WINDOW_WIDTH               = 1500
WINDOW_HEIGHT              = 700
WINDOW_WIDTH_HALF          = WINDOW_WIDTH  // 2
WINDOW_HEIGHT_HALF         = WINDOW_HEIGHT // 2

### TEXT SETTINGS ###
CAPTION_TEXT               = "Shooter"
            
def runGame():
    playerObjects, cameraCoords = initializeGame()
    moveDown, moveUp = False, False
    while True:

        # 1: Event handling loop
        for event in pygame.event.get():
    
            if event.type == QUIT:
                terminate()
    
            elif event.type == KEYDOWN:
                # Move player
                checkActionKeys(playerObjects, event.key, True, False)
                
            elif event.type == KEYUP:
                # Stop continuous movements
                checkActionKeys(playerObjects, event.key, False, True)

        # 2: Update game
        updatePlayersActions(playerObjects)

        # 3: Display game
        tileMapEngine.drawMap(cameraCoords["x"], cameraCoords["y"])
        drawPlayers(playerObjects, cameraCoords)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def main():
    gameSetup()
    while True:
        runGame()

def initializeGame():
    playerObjects = {}
    for i in range(1, gameSettings["NUMBER_OF_PLAYERS"]+ 1):
        playerObjects["player%s" % i] = makePlayer(i)
    cameraCoords = {"x": gameSettings["CAMERA_START_POSITION_X"],
                    "y": gameSettings["CAMERA_START_POSITION_Y"]}

    return playerObjects, cameraCoords

def makePlayer(playerNumber: int):
    playerObj = {}
    playerObj["character"]    = gameSettings["PLAYER" + str(playerNumber) + "_CHARACTER"]
    playerObj["health"]       = gameSettings["PLAYER_MAX_HEALTH"]
    playerObj["x"]            = gameSettings["PLAYER" + str(playerNumber) + "_START_POSITION_X"]
    playerObj["y"]            = gameSettings["PLAYER" + str(playerNumber) + "_START_POSITION_Y"]

    # Add actions
    for action in ACTION_TYPES:
        playerObj[action]         = False
        playerObj[action + "Key"] = gameSettings["PLAYER" + str(playerNumber) + "_" + action.upper()]

    return playerObj

def updatePlayersActions(playerObjects: {}):
    for i in range(1, gameSettings["NUMBER_OF_PLAYERS"] + 1):
        updatePlayerActions(playerObjects["player%s" % i])

def updatePlayerActions(player: {}):

    if player["moveRight"]:
        player["x"] += gameSettings["PLAYER_MOVERATE"]

    elif player["moveLeft"]:
        player["x"] -= gameSettings["PLAYER_MOVERATE"]

def checkActionKeys(playerObjects: {}, keyPressed: int, keyDown: bool, keyUp: bool):
    if keyDown:
        for i in range(1, gameSettings["NUMBER_OF_PLAYERS"] + 1):
            for action in ACTION_TYPES:
                # Evaluation occurs at ascii value level
                if keyPressed == eval(playerObjects["player%s" % i][action + "Key"]):
                    playerObjects["player%s" % i][action] = True

    elif keyUp:
        for i in range(1, gameSettings["NUMBER_OF_PLAYERS"] + 1):
            for action in CONTINUOUS_ACTION_TYPES:
                # Evaluation occurs at ascii value level
                if keyPressed == eval(playerObjects["player%s" % i][action + "Key"]):
                    playerObjects["player%s" % i][action] = False

"""def moveCamera(camerax: int, cameray: int, playerx: int, playery: int):

    if playerx - (camerax + WINDOW_WIDTH_HALF) > CAMERASLACK_X:
        # Player moved to the right
        camerax = playerx - WINDOW_WIDTH_HALF - CAMERASLACK_X
    elif (camerax + WINDOW_WIDTH_HALF) - playerx > CAMERASLACK_X:
        # Player moved to the left
        camerax = playerx - WINDOW_WIDTH_HALF + CAMERASLACK_X
    if playery - (cameray + WINDOW_HEIGHT_HALF) > CAMERASLACK_Y:
        # Player moved down
        cameray = playery - WINDOW_HEIGHT_HALF - CAMERASLACK_Y
    elif (cameray + WINDOW_HEIGHT_HALF) - playery > CAMERASLACK_Y:
        # Player moved up
        cameray = playery - WINDOW_HEIGHT_HALF + CAMERASLACK_Y

    return camerax, cameray"""

def drawPlayers(playerObjects: {}, cameraCoords: {}):
    for i in range(1, gameSettings["NUMBER_OF_PLAYERS"] + 1):
        drawPlayer(playerObjects["player%s" % i]["x"], playerObjects["player%s" % i]["y"],
                   playerObjects["player%s" % i]["character"], cameraCoords["x"], cameraCoords["y"])

def drawPlayer(playerx: int, playery: int, playerCharacter: str, camerax: int, cameray: int):
    DISPLAYSURF.blit(CHARACTER_IMAGES[playerCharacter], (playerx - camerax, playery - cameray))

def loadImage(imageFilePath: str):
    image = pygame.image.load(imageFilePath)
    return pygame.transform.scale(image, (gameSettings["CHARACTERS_SIZE"], gameSettings["CHARACTERS_SIZE"]))

def windowSetUp():
    global DISPLAYSURF
    DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(CAPTION_TEXT)

def mapSetUp():
    # load and set game map
    tileMapEngine.init()
    tileMapEngine.loadMap(gameSettings["MAPDESIGNFILE"])
    tileMapEngine.loadBackground(gameSettings["BACKGROUNDFILE"])
    tileMapEngine.loadTileSet(gameSettings["TILESETFOLDER"])
    tileMapEngine.loadDecorationSet(gameSettings["DECORATIONSETFOLDER"])

def loadCharacterImages():
    global CHARACTER_IMAGES
    CHARACTER_IMAGES = {}

    for characterFileName in os.listdir(gameSettings["CHARACTERSETFOLDER"]):
        characterName = characterFileName.split(".")[0] # Remove file extension
        CHARACTER_IMAGES[characterName] = loadImage(gameSettings["CHARACTERSETFOLDER"] + "/" + characterFileName)

def loadGameSettings():
    global gameSettings

    gameSettings = {}
    with open("ShooterGameSettings.txt", "r") as gameSettingsFile:
        gameSettingsLines = gameSettingsFile.readlines()
        for line in gameSettingsLines:
            if line[0] == "#" or line == "\n":
                # Line begins with "#" which means it's a comment or
                # it's a blank line
                continue
            else:
                line = line.split()
                gameSetting = line[0]
                gameValue   = line[2]
                # Convert numbers with str type to int type
                try:
                    gameValue = int(gameValue)
                except:
                    # Game value is str value
                    pass

                gameSettings[gameSetting] = gameValue  

def gameSetup():
    global FPSCLOCK
    windowSetUp()
    loadGameSettings()
    mapSetUp()
    loadCharacterImages()
    FPSCLOCK = pygame.time.Clock()

def terminate():
    pygame.quit()
    sys.exit()    

if __name__ == "__main__":
    main()