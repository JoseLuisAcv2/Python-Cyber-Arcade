# Snake Game
#
# By Jose Acevedo
#
# © Copyright 2015.

import pygame
import random
import sys
import time
import os
from   pygame.locals import *

# COLORS            R    G    B
WHITE           = (255, 255, 255)
BLACK           = (0  , 0  , 0  )
RED             = (255, 0  , 0  )
DARKRED         = (155, 0  , 0  )
GREEN           = (0  , 255, 0  )
DARKGREEN       = (0  , 155, 0  )
SKYBLUE         = (135, 206, 234)
LIGHTESTGRAY    = (140, 140, 140)
LIGHTGRAY       = (50 , 80 , 80 )
YELLOW          = (155, 155, 0  )

# CONSTANTS
HEAD                           = 0
UP                             = "up"
DOWN                           = "down"
LEFT                           = "left"
RIGHT                          = "right"
EASY                           = "easy"
MEDIUM                         = "medium"
HARD                           = "hard"
ON                             = "on"
OFF                            = "off"

### GAME SETTINGS ###

# DISPLAY SETTINGS
WINDOW_WIDTH                   = 750
WINDOW_HEIGHT                  = 750
CELL_SIZE                      = 30
FPS                            = 15
INITIAL_SNAKE_LENGHT           = 3
SNAKELOGO_WIDTH                = 400
SNAKELOGO_HEIGHT               = 400
PLAYBUTTON_WIDTH               = 100
PLAYBUTTON_HEIGHT              = 100
LEVELBUTTON_WIDTH              = 220
LEVELBUTTON_HEIGHT             = 29
GAME_SPEED_EASY                = 9
GAME_SPEED_MEDIUM              = 13
GAME_SPEED_HARD                = 17
COUNTDOWN_LENGHT               = 0.5
INITIAL_SNAKE_DIRECTON         = RIGHT
SNAKE_COLOR                    = GREEN
SNAKE_BORDER_COLOR             = DARKGREEN
APPLE_COLOR                    = RED
APPLE_BORDER_COLOR             = DARKRED
GAME_BACKGROUND_COLOR          = BLACK
MAIN_MENU_BACKGROUND_COLOR     = SKYBLUE
BOARD_COLOR                    = RED
HIGHLIGHT_COLOR                = YELLOW
HIGHLIGHT_MARGIN_WIDTH         = 10
HIGHLIGHT_BORDER_SQUARE_SIZE   = 10
COUNTDOWN_NUMBER_SIZE          = 150
CELL_BORDER_WIDTH              = CELL_SIZE // 5
WINDOW_WIDTH_CENTER            = WINDOW_WIDTH  // 2
WINDOW_HEIGHT_CENTER           = WINDOW_HEIGHT // 2
GRID_WIDTH                     = WINDOW_WIDTH  / CELL_SIZE
GRID_HEIGHT                    = WINDOW_HEIGHT / CELL_SIZE
SNAKELOGO_TOPLEFT_X            = WINDOW_WIDTH_CENTER  - (SNAKELOGO_WIDTH // 2)
SNAKELOGO_TOPLEFT_Y            = WINDOW_HEIGHT_CENTER // 10 + CELL_SIZE
PLAYBUTTON_TOPLEFT_X           = WINDOW_WIDTH_CENTER  - (PLAYBUTTON_WIDTH // 2)
PLAYBUTTON_TOPLEFT_Y           = WINDOW_HEIGHT_CENTER + (CELL_SIZE * 2) + (CELL_SIZE // 2)
EASYLEVELBUTTON_TOPLEFT_X      = WINDOW_WIDTH_CENTER  - (LEVELBUTTON_WIDTH // 2)
EASYLEVELBUTTON_TOPLEFT_Y      = WINDOW_HEIGHT_CENTER + (CELL_SIZE * 2)
MEDIUMLEVELBUTTON_TOPLEFT_X    = WINDOW_WIDTH_CENTER  - (LEVELBUTTON_WIDTH // 2)
MEDIUMLEVELBUTTON_TOPLEFT_Y    = WINDOW_HEIGHT_CENTER + (CELL_SIZE * 3) + (CELL_SIZE // 2)
HARDLEVELBUTTON_TOPLEFT_X      = WINDOW_WIDTH_CENTER  - (LEVELBUTTON_WIDTH // 2)
HARDLEVELBUTTON_TOPLEFT_Y      = WINDOW_HEIGHT_CENTER + (CELL_SIZE * 5)
COUNTDOWN_NUMBER_CENTER_X      = WINDOW_WIDTH_CENTER
COUNTDOWN_NUMBER_CENTER_Y      = WINDOW_HEIGHT_CENTER
COUNTDOWN_GO_WIDTH             = 200
COUNTDOWN_GO_HEIGHT            = 150
BOARD_WIDTH                    = 300
BOARD_HEIGHT                   = 300
BOARD_TOPLEFT_X                = WINDOW_WIDTH_CENTER  - (BOARD_WIDTH // 2)
BOARD_TOPLEFT_Y                = WINDOW_HEIGHT_CENTER - (BOARD_HEIGHT // 2)
BOARD_CORNER_SQUARE_SIZE       = 20
BACKGROUND_IMAGE_WIDTH         = 300
BACKGROUND_IMAGE_HEIGHT        = 300
AUDIOBUTTON_SIZE               = 50
AUDIOBUTTON_TOPLEFT_X          = WINDOW_WIDTH - (AUDIOBUTTON_SIZE) - (AUDIOBUTTON_SIZE // 2)
AUDIOBUTTON_TOPLEFT_Y          = AUDIOBUTTON_SIZE // 2 - 7
GAMEOVER_WIDTH                 = 400
GAMEOVER_HEIGHT                = 200
GAMEOVERIMAGE_TOPLEFT_X        = WINDOW_WIDTH_CENTER - (GAMEOVER_WIDTH // 2)
GAMEOVERIMAGE_TOPLEFT_Y        = WINDOW_HEIGHT_CENTER - GAMEOVER_HEIGHT
PAUSEBUTTON_SIZE               = 114
PAUSEIMAGE_WIDTH               = 400
PAUSEIMAGE_HEIGHT              = 50
HIGHLIGHTRING_SIZE             = 70
MENUBARBUTTON_SIZE             = 42
SURETOQUITIMAGE_WDITH          = 600
SURETOQUITIMAGE_HEIGHT         = 20

assert(WINDOW_WIDTH % CELL_SIZE == 0 and WINDOW_HEIGHT % CELL_SIZE == 0)

# TEXT SETTINGS
GAME_TITLE                     = "SNAKE"
SCORE_TEXT                     = "SCORE"
RECORD_TEXT                    = "RECORD"
CREDITS_TEXT                   = "© Jose Acevedo"
TEXT_FONT                      = "freesansbold.ttf"
NEWRECORD_MESSAGE              = "NEW RECORD"
TEXT_SIZE                      = 25
GAME_TITLE_SIZE                = 150
CREDITS_TEXT_SIZE              = 13
TEXT_COLOR                     = LIGHTESTGRAY
GAME_TITLE_TEXT_COLOR          = LIGHTGRAY
CREDITS_TEXT_COLOR             = LIGHTGRAY
GAME_WINDOW_CAPTION            = GAME_TITLE
GAME_TITLE_CENTER_X            = WINDOW_WIDTH_CENTER
GAME_TITLE_CENTER_Y            = WINDOW_HEIGHT_CENTER - (WINDOW_HEIGHT // 8)
CREDITS_CENTER_X               = GAME_TITLE_CENTER_X  + (CELL_SIZE * 4)
CREDITS_CENTER_Y               = GAME_TITLE_CENTER_Y  + (CELL_SIZE * 4)
SCORE_TEXT_TOPLEFT_X           = CELL_SIZE
SCORE_TEXT_TOPLEFT_Y           = CELL_SIZE
RECORD_TEXT_TOPLEFT_X          = CELL_SIZE
RECORD_TEXT_TOPLEFT_Y          = CELL_SIZE * 2

def imageGenerator(imagePath: "image", width: int, height: int) -> ("surj"):

    image         = pygame.image.load(imagePath)
    resizedImage  = pygame.transform.scale(image, (width, height))

    return resizedImage

# GAME SETUP
pygame.init()
DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
BASINFONT   = pygame.font.Font(TEXT_FONT, TEXT_SIZE)
FPSCLOCK    = pygame.time.Clock()
pygame.display.set_caption(GAME_WINDOW_CAPTION)

# IMAGES SETUP
BACKGROUND_IMAGE     = imageGenerator("SnakeImages/BackgroundImage.png", BACKGROUND_IMAGE_WIDTH, BACKGROUND_IMAGE_HEIGHT)
PLAYBUTTON           = imageGenerator("SnakeImages/PlayButton.png" , PLAYBUTTON_WIDTH, PLAYBUTTON_HEIGHT)
AUDIOBUTTON          = imageGenerator("SnakeImages/AudioButton.png", AUDIOBUTTON_SIZE, AUDIOBUTTON_SIZE)
MUTEBUTTON           = imageGenerator("SnakeImages/MuteButton.png" , AUDIOBUTTON_SIZE, AUDIOBUTTON_SIZE)
SNAKELOGO            = imageGenerator("SnakeImages/SnakeLogo.png"  , SNAKELOGO_WIDTH , SNAKELOGO_HEIGHT)
EASYLEVELBUTTON      = imageGenerator("SnakeImages/EasyLevelButton.png"  , LEVELBUTTON_WIDTH, LEVELBUTTON_HEIGHT)
MEDIUMLEVELBUTTON    = imageGenerator("SnakeImages/MediumLevelButton.png", LEVELBUTTON_WIDTH, LEVELBUTTON_HEIGHT)
HARDLEVELBUTTON      = imageGenerator("SnakeImages/HardLevelButton.png"  , LEVELBUTTON_WIDTH, LEVELBUTTON_HEIGHT)
NUMBER1IMAGE         = imageGenerator("SnakeImages/Number1.png" , COUNTDOWN_NUMBER_SIZE, COUNTDOWN_NUMBER_SIZE)
NUMBER2IMAGE         = imageGenerator("SnakeImages/Number2.png" , COUNTDOWN_NUMBER_SIZE, COUNTDOWN_NUMBER_SIZE)
NUMBER3IMAGE         = imageGenerator("SnakeImages/Number3.png" , COUNTDOWN_NUMBER_SIZE, COUNTDOWN_NUMBER_SIZE)
GOIMAGE              = imageGenerator("SnakeImages/GoImage.png" , COUNTDOWN_GO_WIDTH   , COUNTDOWN_GO_HEIGHT)
GAMEOVERIMAGE        = imageGenerator("SnakeImages/GameOver.png", GAMEOVER_WIDTH       , GAMEOVER_HEIGHT)
RESUMEGAMEBUTTON     = imageGenerator("SnakeImages/ResumeGameButton.png", MENUBARBUTTON_SIZE, MENUBARBUTTON_SIZE)
RESTARTBUTTON        = imageGenerator("SnakeImages/RestartButton.png"   , MENUBARBUTTON_SIZE, MENUBARBUTTON_SIZE)
EXITBUTTON           = imageGenerator("SnakeImages/ExitButton.png"      , MENUBARBUTTON_SIZE, MENUBARBUTTON_SIZE)
MENUBUTTON           = imageGenerator("SnakeImages/MenuButton.png"      , MENUBARBUTTON_SIZE, MENUBARBUTTON_SIZE)
CHECKBUTTON          = imageGenerator("SnakeImages/CheckButton.png"     , MENUBARBUTTON_SIZE, MENUBARBUTTON_SIZE)
CLOSEBUTTON          = imageGenerator("SnakeImages/CloseButton.png"     , MENUBARBUTTON_SIZE, MENUBARBUTTON_SIZE)
PAUSEBUTTON          = imageGenerator("SnakeImages/PauseButton.png"     , PAUSEBUTTON_SIZE      , PAUSEBUTTON_SIZE)
PAUSEIMAGE           = imageGenerator("SnakeImages/PauseImage.png"      , PAUSEIMAGE_WIDTH      , PAUSEIMAGE_HEIGHT)
HIGHLIGHTRING        = imageGenerator("SnakeImages/HighlightRing.png"   , HIGHLIGHTRING_SIZE    , HIGHLIGHTRING_SIZE)
SURETOQUITIMAGE      = imageGenerator("SnakeImages/SureToQuit.png"      , SURETOQUITIMAGE_WDITH , SURETOQUITIMAGE_HEIGHT)
BACKGROUND_MINIIMAGE = imageGenerator("SnakeImages/BackgroundImage.png" , 10, 10)

# SOUND SETUP
pygame.mixer.music.load("/home/jose/Documents/juegos/Snake/SnakeSounds/BackgroundMusic.mp3")
BUTTONCLICKSOUND = pygame.mixer.Sound("/home/jose/Documents/juegos/Snake/SnakeSounds/ButtonClickSound.wav")
EATAPPLESOUND    = pygame.mixer.Sound("/home/jose/Documents/juegos/Snake/SnakeSounds/EatAppleSound.wav")

def getRandomLocation() -> (int, int):

    x = random.randint(0, GRID_WIDTH  - 1)
    y = random.randint(0, GRID_HEIGHT - 1)

    return x, y

def getSnakeStartingPosition() -> ([{int}]):

    startX = 6
    startY = GRID_HEIGHT // 2

    snakeCoords = [ {"x": startX    , "y": startY},
                    {"x": startX - 1, "y": startY},
                    {"x": startX - 1, "y": startY} ]

    assert(len(snakeCoords) == INITIAL_SNAKE_LENGHT)

    return snakeCoords

def getApplePosition(snakeCoords: [{int}], snakeLenght: int) -> ({int}):

    validPosition = False
    while not validPosition:
        appleX, appleY = getRandomLocation()
        # Check apple doesn't appear on a cell occupied by snake
        for i in range(snakeLenght):
            if appleX == snakeCoords[i]["x"] and appleY == snakeCoords[i]["y"]:
                validPosition = False
                break
        else:
            validPosition = True

    appleCoords = {"x": appleX, "y": appleY}

    return appleCoords

def initializeGame() -> ([{int}], int, {int}, str, int, int, bool, bool):

    global score

    snakeCoords   = getSnakeStartingPosition()
    snakeLenght   = INITIAL_SNAKE_LENGHT
    appleCoords   = getApplePosition(snakeCoords, snakeLenght)
    direction     = INITIAL_SNAKE_DIRECTON
    score         = 0
    gameOver      = False

    # Get game record
    if RecordFileExists():
        with open("recordSnake.txt", "r") as recordFile:
            record = int(recordFile.read())
        newRecord = False
    
    else:
        record    = score
        newRecord = True

    return snakeCoords, snakeLenght, appleCoords, direction, \
           score      , record     , newRecord  , gameOver

def snakeCollision(snakeCoords: [{int}], snakeLenght: int) -> (bool):

    collision = False
    # Check if snake hits borders
    if snakeCoords[HEAD]["x"] <= -1             or \
       snakeCoords[HEAD]["y"] <= -1             or \
       snakeCoords[HEAD]["x"] >= GRID_WIDTH     or \
       snakeCoords[HEAD]["y"] >= GRID_HEIGHT:
       collision = True

    # Check if snake hits itself
    for i in range(snakeLenght)[2:]:
        if snakeCoords[HEAD]["x"] == snakeCoords[i]["x"] and \
           snakeCoords[HEAD]["y"] == snakeCoords[i]["y"]:
           collision = True
           break

    return collision

def snakeEatsApple(snakeCoords: [{int}], appleCoords: {int}) -> (bool):

    if snakeCoords[HEAD]["x"] == appleCoords["x"] and \
       snakeCoords[HEAD]["y"] == appleCoords["y"]:
        return True
    else:
        return False

def checkAppleEaten(snakeCoords: [{int}], snakeLenght: int, appleCoords: {int}, score: int) -> ([{int}], int, {int}, int):

    if snakeEatsApple(snakeCoords, appleCoords):
        EATAPPLESOUND.play()
        score = addPoints(score)
        appleCoords = getApplePosition(snakeCoords, snakeLenght)
        # Snake grows
        snakeLenght += 1

    elif not snakeEatsApple(snakeCoords, appleCoords):
        # Remove snake tail
        snakeCoords.pop()

    return snakeLenght, appleCoords, score

def validDirection(snakeCoords: [{int}], selectedDirecton: str) -> (bool):

    if   selectedDirecton == UP    and \
       snakeCoords[HEAD]["x"] == snakeCoords[1]["x"]:
       valid = False

    elif selectedDirecton == DOWN  and \
       snakeCoords[HEAD]["x"] == snakeCoords[1]["x"]:
       valid = False

    elif selectedDirecton == RIGHT and \
       snakeCoords[HEAD]["y"] == snakeCoords[1]["y"]:
       valid = False

    elif selectedDirecton == LEFT  and \
       snakeCoords[HEAD]["y"] == snakeCoords[1]["y"]:
       valid = False

    else:
        valid = True

    return valid

def moveSnake(snakeCoords: [{int}], snakeLenght: int, appleCoords: {int}, direction: str) -> ("void"):

    snakeheadX = snakeCoords[HEAD]["x"]
    snakeheadY = snakeCoords[HEAD]["y"]

    # Move snake head
    if   direction == UP:
        newSnakeHead = {"x": snakeheadX, "y": snakeheadY - 1}

    elif direction == DOWN:
        newSnakeHead = {"x": snakeheadX, "y": snakeheadY + 1}

    elif direction == RIGHT:
        newSnakeHead = {"x": snakeheadX + 1, "y": snakeheadY}

    elif direction == LEFT:
        newSnakeHead = {"x": snakeheadX - 1, "y": snakeheadY}

    snakeCoords.insert(HEAD, newSnakeHead)

def addPoints(score: int) -> (int):
    score += 1

    return score

def updateDirection(previousDirection: str, newDirection: str) -> (str):
    previousDirection = newDirection

    return previousDirection

def convertToPixelCoordinates(gridCoord: int) -> (int):
    pixelCoord = gridCoord * CELL_SIZE

    return pixelCoord

def RecordFileExists() -> (bool):
    return os.path.exists("recordSnake.txt")

def CompareScoreAndRecord(score: int, record: int, newRecord: bool) -> (int, bool):

    if score > record or newRecord:
        record      = score
        newRecord   = True

    else:
        newRecord = False

    return record, newRecord

def CheckGameRecord(snakeCoords: [{int}], snakeLenght: int, appleCoords: {int},
                    score: int, record: int, newRecord: bool) -> ("void"):

    if newRecord:
        with open("recordSnake.txt", "w") as recordFile:
            recordFile.write(str(score))

    restart ,quitGame, goToMenu = displayGameOver(snakeCoords, snakeLenght, appleCoords, score, record, newRecord)

    return restart, quitGame, goToMenu

def endOfGame(snakeCoords: [{int}], snakeLenght: int) -> (bool):

    if snakeCollision(snakeCoords, snakeLenght):
        gameOver = True
    else:
        gameOver = False

    return gameOver

def terminate() -> ("void"):
    pygame.quit()
    sys.exit()

def changeHighlightedLevelButton(highlightedButton: "surf", highlightedButtonRect: "rect", direction: str) -> ("surf", "rect"):

    if direction == DOWN:
        if highlightedButton == EASYLEVELBUTTON:
            BUTTONCLICKSOUND.play()
            highlightedButton     = MEDIUMLEVELBUTTON
            highlightedButtonRect = MEDIUMLEVELBUTTONRECT

        elif highlightedButton == MEDIUMLEVELBUTTON:
            BUTTONCLICKSOUND.play()
            highlightedButton     = HARDLEVELBUTTON
            highlightedButtonRect = HARDLEVELBUTTONRECT
    
    elif direction == UP:
        if highlightedButton == MEDIUMLEVELBUTTON:
            BUTTONCLICKSOUND.play()
            highlightedButton     = EASYLEVELBUTTON
            highlightedButtonRect = EASYLEVELBUTTONRECT

        elif highlightedButton == HARDLEVELBUTTON:
            BUTTONCLICKSOUND.play()
            highlightedButton     = MEDIUMLEVELBUTTON
            highlightedButtonRect = MEDIUMLEVELBUTTONRECT

    return highlightedButton, highlightedButtonRect

def changeHighlightedMenuButtonByKeyboard(highlightedButton: "surf", highlightedButtonRect: "rect", direction: str) -> ("surf", "rect"):

    if direction == RIGHT:
        if highlightedButton == RESUMEGAMEBUTTON:
            BUTTONCLICKSOUND.play()
            highlightedButton     = RESTARTBUTTON
            highlightedButtonRect = RESTARTBUTTONRECT

        elif highlightedButton == RESTARTBUTTON:
            BUTTONCLICKSOUND.play()
            highlightedButton     = MENUBUTTON
            highlightedButtonRect = MENUBUTTONRECT

        elif highlightedButton == MENUBUTTON:
            BUTTONCLICKSOUND.play()
            highlightedButton     = EXITBUTTON
            highlightedButtonRect = EXITBUTTONRECT

    elif direction == LEFT:
        if highlightedButton == RESTARTBUTTON:
            BUTTONCLICKSOUND.play()
            highlightedButton     = RESUMEGAMEBUTTON
            highlightedButtonRect = RESUMEGAMEBUTTONRECT

        elif highlightedButton == MENUBUTTON:
            BUTTONCLICKSOUND.play()
            highlightedButton     = RESTARTBUTTON
            highlightedButtonRect = RESTARTBUTTONRECT

        elif highlightedButton == EXITBUTTON:
            BUTTONCLICKSOUND.play()
            highlightedButton     = MENUBUTTON
            highlightedButtonRect = MENUBUTTONRECT

    return highlightedButton, highlightedButtonRect

def changeHighlightedMenuButtonByMouse(highlightedButton: "surf", highlightedButtonRect: "rect",
                                       mousex: int, mousey: int) -> ("surf", "rect"):

    if RESUMEGAMEBUTTONRECT.collidepoint(mousex, mousey):
        highlightedButton     = RESUMEGAMEBUTTON
        highlightedButtonRect = RESUMEGAMEBUTTONRECT

    elif RESTARTBUTTONRECT.collidepoint(mousex, mousey):
        highlightedButton     = RESTARTBUTTON
        highlightedButtonRect = RESTARTBUTTONRECT

    elif MENUBUTTONRECT.collidepoint(mousex, mousey):
        highlightedButton     = MENUBUTTON
        highlightedButtonRect = MENUBUTTONRECT

    elif EXITBUTTONRECT.collidepoint(mousex, mousey):
        highlightedButton     = EXITBUTTON
        highlightedButtonRect = EXITBUTTONRECT        

    return highlightedButton, highlightedButtonRect

def checkPauseMenuBar(highlightedButton: "rect") -> (bool, bool, bool, bool):
    BUTTONCLICKSOUND.play()
    if highlightedButton == RESUMEGAMEBUTTON:
        play     = True
        restart  = False
        quitGame = False
        goToMenu = False

    elif highlightedButton == RESTARTBUTTON:
        play     = True
        restart  = True
        quitGame = False
        goToMenu = False

    elif highlightedButton == MENUBUTTON:
        play     = False
        restart  = False
        quitGame = False
        goToMenu = True

    elif highlightedButton == EXITBUTTON:
        play     = False
        restart  = False
        quitGame = True
        goToMenu = False

    return play, restart, quitGame, goToMenu

def changeHighlightedGameOverMenuButtonByKeyboard(highlightedButton: "surf", highlightedButtonRect: "rect",
                                                  direction: str) -> ("surf", "rect"):
    if direction == RIGHT:
        if highlightedButton == RESTARTBUTTON:
            BUTTONCLICKSOUND.play()
            highlightedButton     = MENUBUTTON
            highlightedButtonRect = MENUBUTTONRECT
        elif highlightedButton == MENUBUTTON:
            BUTTONCLICKSOUND.play()
            highlightedButton     = EXITBUTTON
            highlightedButtonRect = EXITBUTTONRECT

    elif direction == LEFT:
        if highlightedButton == MENUBUTTON:
            BUTTONCLICKSOUND.play()
            highlightedButton     = RESTARTBUTTON
            highlightedButtonRect = RESTARTBUTTONRECT
        elif highlightedButton == EXITBUTTON:
            BUTTONCLICKSOUND.play()
            highlightedButton     = MENUBUTTON
            highlightedButtonRect = MENUBUTTONRECT

    return highlightedButton, highlightedButtonRect

def changeHighlightedGameOverButtonByMouse(highlightedButton: "surf", highlightedButtonRect: "rect",
                                           mousex: int, mousey: int) -> ("surf", "rect"):

    if RESTARTBUTTONRECT.collidepoint(mousex, mousey):
        highlightedButton     = RESTARTBUTTON
        highlightedButtonRect = RESTARTBUTTONRECT
    elif MENUBUTTONRECT.collidepoint(mousex, mousey):
        highlightedButton     = MENUBUTTON
        highlightedButtonRect = MENUBUTTONRECT
    elif EXITBUTTONRECT.collidepoint(mousex, mousey):
        highlightedButton     = EXITBUTTON
        highlightedButtonRect = EXITBUTTONRECT

    return highlightedButton, highlightedButtonRect

def checkGameOverMenuBar(highlightedButton: "rect") -> (bool, bool, bool):
    BUTTONCLICKSOUND.play()
    if highlightedButton == RESTARTBUTTON:
        restart  = True
        quitGame = False
        goToMenu = False

    elif highlightedButton == MENUBUTTON:
        restart  = False
        quitGame = False
        goToMenu = True

    elif highlightedButton == EXITBUTTON:
        restart  = False
        quitGame = True
        goToMenu = False

    return restart, quitGame, goToMenu

def mouseIsOverPauseMenuButton(mousex: int, mousey: int) -> (bool):

    if RESUMEGAMEBUTTONRECT.collidepoint(mousex, mousey) or \
       RESTARTBUTTONRECT.collidepoint(mousex, mousey)    or \
       MENUBUTTONRECT.collidepoint(mousex, mousey)       or \
       EXITBUTTONRECT.collidepoint(mousex, mousey):
        return True
    else:
        return False

def mouseIsOverGameOverMenuButton(mousex: int, mousey: int) -> (bool):

    if RESTARTBUTTONRECT.collidepoint(mousex, mousey)    or \
       MENUBUTTONRECT.collidepoint(mousex, mousey)       or \
       EXITBUTTONRECT.collidepoint(mousex, mousey):
        return True
    else:
        return False

def changeHighlightedQuitButtonByKeyboard(highlightedButton: "rect", highlightedButtonRect: "rect",
                                          direction: str) -> ("surf", "rect"):

    if direction == RIGHT:
        if highlightedButton == CHECKBUTTON:
            BUTTONCLICKSOUND.play()
            highlightedButton     = CLOSEBUTTON
            highlightedButtonRect = CLOSEBUTTONRECT

    elif direction == LEFT:
        if highlightedButton == CLOSEBUTTON:
            BUTTONCLICKSOUND.play()
            highlightedButton     = CHECKBUTTON
            highlightedButtonRect = CHECKBUTTONRECT

    return highlightedButton, highlightedButtonRect

def changeHighlightedQuitButtonByMouse(highlightedButton: "surf", highlightedButtonRect: "rect",
                                           mousex: int, mousey: int) -> ("surf", "rect"):

    if CHECKBUTTONRECT.collidepoint(mousex, mousey):
        highlightedButton     = CHECKBUTTON
        highlightedButtonRect = CHECKBUTTONRECT

    elif CLOSEBUTTONRECT.collidepoint(mousex, mousey):
        highlightedButton     = CLOSEBUTTON
        highlightedButtonRect = CLOSEBUTTONRECT

    return highlightedButton, highlightedButtonRect

def mouseIsOverQuitMenuButton(mousex: int, mousey: int) -> (bool):

    if CHECKBUTTONRECT.collidepoint(mousex, mousey) or \
       CLOSEBUTTONRECT.collidepoint(mousex, mousey):
        return True
    else:
        return False

def checkQuitMenuBar(highlightedButton: "rect") -> (bool):
    BUTTONCLICKSOUND.play()
    if highlightedButton == CHECKBUTTON:
        quitGame = True
    elif highlightedButton == CLOSEBUTTON:
        quitGame = False

    return quitGame

# AUDIO
def beginBackgroundMusic() -> ("void"):
    pygame.mixer.music.play(-1, 0.0)

def stopBackgroundMusic() -> ("void"):
    pygame.mixer.music.stop()

def changeAudioState() -> ("void"):
    global backgroundMusicState
    if backgroundMusicState == ON:
        backgroundMusicState = OFF
        stopBackgroundMusic()
    elif backgroundMusicState == OFF:
        backgroundMusicState = ON
        beginBackgroundMusic()

def checkAudioState(mousex: int, mousey: int) -> ("void"):
    global backgroundMusicState
    if backgroundMusicState == ON:
        if AUDIOBUTTONRECT.collidepoint(mousex, mousey):
            BUTTONCLICKSOUND.play()
            changeAudioState()
    elif backgroundMusicState == OFF:
        if MUTEBUTTONRECT.collidepoint(mousex, mousey):
            BUTTONCLICKSOUND.play()
            changeAudioState()

########################
####### GRAPHICS #######
########################

### OBJETS ###
def drawSnake(snakeCoords: [{int}], snakeLenght: int) -> ("void"):

    for snakeSegment in range(snakeLenght):

        # Snake segment grid coordinates
        snakeSegmentGridCoordX = snakeCoords[snakeSegment]["x"]
        snakeSegmentGridCoordY = snakeCoords[snakeSegment]["y"]

        # Convert snake segment to pixel coordinates
        snakeSegmentPixelCoordX = convertToPixelCoordinates(snakeSegmentGridCoordX)
        snakeSegmentPixelCoordY = convertToPixelCoordinates(snakeSegmentGridCoordY)

        # Draw each snake segment:

        # Snake segment border
        snakeSegmentBorderRect = pygame.Rect(snakeSegmentPixelCoordX, snakeSegmentPixelCoordY, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(DISPLAYSURF, SNAKE_BORDER_COLOR, snakeSegmentBorderRect)

        # Snake segment interior
        snakeSegmentRect = pygame.Rect(snakeSegmentPixelCoordX + CELL_BORDER_WIDTH, snakeSegmentPixelCoordY + CELL_BORDER_WIDTH,
                                       CELL_SIZE - (2 * CELL_BORDER_WIDTH), CELL_SIZE - (2 * CELL_BORDER_WIDTH))
        pygame.draw.rect(DISPLAYSURF, SNAKE_COLOR, snakeSegmentRect)

def drawApple(appleCoords: [{int}]) -> ("void"):

    # Apple grid coordinates
    appleGridCoordX = appleCoords["x"]
    appleGridCoordY = appleCoords["y"]

    # convert apple to pixel coordinates
    applePixelCoordX = convertToPixelCoordinates(appleGridCoordX)
    applePixelCoordY = convertToPixelCoordinates(appleGridCoordY)

    # Draw apple:

    # Apple border
    appleBorderRect = pygame.Rect(applePixelCoordX, applePixelCoordY, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(DISPLAYSURF, APPLE_BORDER_COLOR, appleBorderRect)

    # Apple interior
    appleRect = pygame.Rect(applePixelCoordX + CELL_BORDER_WIDTH, applePixelCoordY + CELL_BORDER_WIDTH,
                            CELL_SIZE - (2 * CELL_BORDER_WIDTH), CELL_SIZE - (2 * CELL_BORDER_WIDTH))
    pygame.draw.rect(DISPLAYSURF, APPLE_COLOR, appleRect)

def drawBackgroundImage() -> ("void"):

    numberOfTimesPerRow    = (WINDOW_WIDTH  // BACKGROUND_IMAGE_WIDTH)  + 1
    numberOfTimesPerColumn = (WINDOW_HEIGHT // BACKGROUND_IMAGE_HEIGHT) + 1

    for i in range(numberOfTimesPerColumn):
        for j in range(numberOfTimesPerRow):
            DISPLAYSURF.blit(BACKGROUND_IMAGE, (BACKGROUND_IMAGE_WIDTH * j, BACKGROUND_IMAGE_HEIGHT * i))

def highlightLevelButton(buttonRect: "rect", button: "surf") -> ("void"):

    # Draw highlight box
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHT_COLOR, buttonRect, HIGHLIGHT_MARGIN_WIDTH)

    # Draw rounded corners
    DISPLAYSURF.blit(BACKGROUND_MINIIMAGE,
                    (buttonRect.topleft[0] - (HIGHLIGHT_MARGIN_WIDTH // 2),
                     buttonRect.topleft[1] - (HIGHLIGHT_MARGIN_WIDTH // 2)))
    DISPLAYSURF.blit(BACKGROUND_MINIIMAGE,
                    (buttonRect.topright[0] - HIGHLIGHT_BORDER_SQUARE_SIZE + (HIGHLIGHT_MARGIN_WIDTH // 2),
                     buttonRect.topright[1] - (HIGHLIGHT_MARGIN_WIDTH // 2)))
    DISPLAYSURF.blit(BACKGROUND_MINIIMAGE,
                    (buttonRect.bottomleft[0] - (HIGHLIGHT_MARGIN_WIDTH // 2),
                     buttonRect.bottomleft[1] - HIGHLIGHT_BORDER_SQUARE_SIZE + (HIGHLIGHT_MARGIN_WIDTH // 2)))
    DISPLAYSURF.blit(BACKGROUND_MINIIMAGE,
                    (buttonRect.bottomright[0] - HIGHLIGHT_BORDER_SQUARE_SIZE + (HIGHLIGHT_MARGIN_WIDTH // 2),
                     buttonRect.bottomright[1] - HIGHLIGHT_BORDER_SQUARE_SIZE + (HIGHLIGHT_MARGIN_WIDTH // 2)))
    pygame.draw.circle(DISPLAYSURF, HIGHLIGHT_COLOR, (buttonRect.topleft[0]     + (HIGHLIGHT_MARGIN_WIDTH // 2) + 1 ,
                                                      buttonRect.topleft[1]     + (HIGHLIGHT_MARGIN_WIDTH // 2) + 1),
                                                      HIGHLIGHT_BORDER_SQUARE_SIZE)
    pygame.draw.circle(DISPLAYSURF, HIGHLIGHT_COLOR, (buttonRect.topright[0]    - (HIGHLIGHT_MARGIN_WIDTH // 2)     ,
                                                      buttonRect.topright[1]    + (HIGHLIGHT_MARGIN_WIDTH // 2) + 1),
                                                      HIGHLIGHT_BORDER_SQUARE_SIZE)
    pygame.draw.circle(DISPLAYSURF, HIGHLIGHT_COLOR, (buttonRect.bottomleft[0]  + (HIGHLIGHT_MARGIN_WIDTH // 2) + 1,
                                                      buttonRect.bottomleft[1]  - (HIGHLIGHT_MARGIN_WIDTH // 2) ),
                                                      HIGHLIGHT_BORDER_SQUARE_SIZE)
    pygame.draw.circle(DISPLAYSURF, HIGHLIGHT_COLOR, (buttonRect.bottomright[0] - (HIGHLIGHT_MARGIN_WIDTH // 2) ,
                                                      buttonRect.bottomright[1] - (HIGHLIGHT_MARGIN_WIDTH // 2) ),
                                                      HIGHLIGHT_BORDER_SQUARE_SIZE)

    DISPLAYSURF.blit(button, (buttonRect.topleft[0], buttonRect.topleft[1]))

def highlightMenuButton(buttonRect: "rect", button: "surf", buttonsize: int) -> ("void"):

    buttonGap = HIGHLIGHTRING_SIZE - buttonsize
    DISPLAYSURF.blit(HIGHLIGHTRING, (buttonRect.topleft[0] - (buttonGap // 2),
                                     buttonRect.topleft[1] - (buttonGap // 2)))
    DISPLAYSURF.blit(button, (buttonRect.topleft[0], buttonRect.topleft[1]))

### TEXT ###
def drawScore(score: int) -> ("void"):

    scoreSurf            = BASINFONT.render(SCORE_TEXT + "  " + str(score), True, TEXT_COLOR)
    scoreRect            = scoreSurf.get_rect()
    scoreRect.topleft    = (SCORE_TEXT_TOPLEFT_X, SCORE_TEXT_TOPLEFT_Y)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

def drawRecord(record: int) -> ("void"):

    recordSurf           = BASINFONT.render(RECORD_TEXT + "  " + str(record), True, TEXT_COLOR)
    recordRect           = recordSurf.get_rect()
    recordRect.topleft   = (RECORD_TEXT_TOPLEFT_X, RECORD_TEXT_TOPLEFT_Y)
    DISPLAYSURF.blit(recordSurf, recordRect)

def drawNewRecord() -> ("void"):

    newRecordFont        = pygame.font.Font(TEXT_FONT, 25)
    newRecordSurf        = newRecordFont.render(NEWRECORD_MESSAGE, True, LIGHTESTGRAY)
    newRecordRect        = newRecordSurf.get_rect()
    newRecordRect.center = (WINDOW_WIDTH_CENTER, WINDOW_HEIGHT_CENTER + 150)
    DISPLAYSURF.blit(newRecordSurf, newRecordRect)

def drawTitle() -> ("void"):

    DISPLAYSURF.blit(SNAKELOGO, (SNAKELOGO_TOPLEFT_X, SNAKELOGO_TOPLEFT_Y))

def drawCredits() -> ("void"):

    creditsFont          = pygame.font.Font(TEXT_FONT, CREDITS_TEXT_SIZE)
    creditsSurf          = creditsFont.render(CREDITS_TEXT, True, CREDITS_TEXT_COLOR)
    creditsRect          = creditsSurf.get_rect()
    creditsRect.center   = (CREDITS_CENTER_X, CREDITS_CENTER_Y)
    DISPLAYSURF.blit(creditsSurf, creditsRect)    

def drawGameOverImage() -> ("void"):
    DISPLAYSURF.blit(GAMEOVERIMAGE, (GAMEOVERIMAGE_TOPLEFT_X, GAMEOVERIMAGE_TOPLEFT_Y))


def drawPauseImage() -> ("void"):
    DISPLAYSURF.blit(PAUSEIMAGE, (WINDOW_WIDTH_CENTER  - (PAUSEIMAGE_WIDTH  // 2),
                                  WINDOW_HEIGHT_CENTER - (PAUSEIMAGE_HEIGHT * 2)))

def drawSureToQuitImage(coordX: int, coordY: int) -> ("void"):
    DISPLAYSURF.blit(SURETOQUITIMAGE, (coordX, coordY))

### BUTTONS ###
def drawPlayButton() -> ("void"):
    global PLAYBUTTONRECT

    DISPLAYSURF.blit(PLAYBUTTON ,(PLAYBUTTON_TOPLEFT_X, PLAYBUTTON_TOPLEFT_Y))
    PLAYBUTTONRECT         = PLAYBUTTON.get_rect()
    PLAYBUTTONRECT.topleft = (PLAYBUTTON_TOPLEFT_X, PLAYBUTTON_TOPLEFT_Y)

def drawAudioButton() -> ("void"):
    global AUDIOBUTTONRECT

    DISPLAYSURF.blit(AUDIOBUTTON, (AUDIOBUTTON_TOPLEFT_X, AUDIOBUTTON_TOPLEFT_Y))
    AUDIOBUTTONRECT          = AUDIOBUTTON.get_rect()
    AUDIOBUTTONRECT.topleft  = (AUDIOBUTTON_TOPLEFT_X, AUDIOBUTTON_TOPLEFT_Y)

def drawMuteButton() -> ("void"):
    global MUTEBUTTONRECT

    DISPLAYSURF.blit(MUTEBUTTON, (AUDIOBUTTON_TOPLEFT_X, AUDIOBUTTON_TOPLEFT_Y))
    MUTEBUTTONRECT          = MUTEBUTTON.get_rect()
    MUTEBUTTONRECT.topleft  = (AUDIOBUTTON_TOPLEFT_X, AUDIOBUTTON_TOPLEFT_Y)

def drawSoundButton() -> ("void"):
    if backgroundMusicState == ON:
        drawAudioButton()
    elif backgroundMusicState == OFF:
        drawMuteButton()

def drawResumeGameButton(coordX: int, coordY: int) -> ("void"):
    global RESUMEGAMEBUTTONRECT

    DISPLAYSURF.blit(RESUMEGAMEBUTTON, (coordX, coordY))
    RESUMEGAMEBUTTONRECT         = RESUMEGAMEBUTTON.get_rect()
    RESUMEGAMEBUTTONRECT.topleft = (coordX, coordY)

def drawMenuButton(coordX: int, coordY: int) -> ("void"):
    global MENUBUTTONRECT

    DISPLAYSURF.blit(MENUBUTTON, (coordX, coordY))
    MENUBUTTONRECT         = MENUBUTTON.get_rect()
    MENUBUTTONRECT.topleft = (coordX, coordY)

def drawExitButton(coordX: int, coordY: int) -> ("void"):
    global EXITBUTTONRECT

    DISPLAYSURF.blit(EXITBUTTON, (coordX, coordY))
    EXITBUTTONRECT         = EXITBUTTON.get_rect()
    EXITBUTTONRECT.topleft = (coordX, coordY)

def drawRestartButton(coordX: int, coordY: int) -> ("void"):
    global RESTARTBUTTONRECT

    DISPLAYSURF.blit(RESTARTBUTTON, (coordX, coordY))
    RESTARTBUTTONRECT         = RESTARTBUTTON.get_rect()
    RESTARTBUTTONRECT.topleft = (coordX, coordY)

def drawCheckButton(coordX: int, coordY: int) -> ("void"):
    global CHECKBUTTONRECT

    DISPLAYSURF.blit(CHECKBUTTON, (coordX, coordY))
    CHECKBUTTONRECT         = CHECKBUTTON.get_rect()
    CHECKBUTTONRECT.topleft = (coordX, coordY)

def drawCloseButton(coordX: int, coordY: int) -> ("void"):
    global CLOSEBUTTONRECT

    DISPLAYSURF.blit(CLOSEBUTTON, (coordX, coordY))
    CLOSEBUTTONRECT         = CLOSEBUTTON.get_rect()
    CLOSEBUTTONRECT.topleft = (coordX, coordY)

### MENU BARS ###
def drawLevelMenu() -> ("void"):
    global EASYLEVELBUTTONRECT, MEDIUMLEVELBUTTONRECT, HARDLEVELBUTTONRECT

    DISPLAYSURF.blit(EASYLEVELBUTTON  , (EASYLEVELBUTTON_TOPLEFT_X  , EASYLEVELBUTTON_TOPLEFT_Y  ))
    DISPLAYSURF.blit(MEDIUMLEVELBUTTON, (MEDIUMLEVELBUTTON_TOPLEFT_X, MEDIUMLEVELBUTTON_TOPLEFT_Y))
    DISPLAYSURF.blit(HARDLEVELBUTTON  , (HARDLEVELBUTTON_TOPLEFT_X  , HARDLEVELBUTTON_TOPLEFT_Y  ))
    EASYLEVELBUTTONRECT               = EASYLEVELBUTTON.get_rect()
    MEDIUMLEVELBUTTONRECT             = MEDIUMLEVELBUTTON.get_rect()
    HARDLEVELBUTTONRECT               = HARDLEVELBUTTON.get_rect()
    EASYLEVELBUTTONRECT.topleft       = (EASYLEVELBUTTON_TOPLEFT_X  , EASYLEVELBUTTON_TOPLEFT_Y  )
    MEDIUMLEVELBUTTONRECT.topleft     = (MEDIUMLEVELBUTTON_TOPLEFT_X, MEDIUMLEVELBUTTON_TOPLEFT_Y)
    HARDLEVELBUTTONRECT.topleft       = (HARDLEVELBUTTON_TOPLEFT_X  , HARDLEVELBUTTON_TOPLEFT_Y  )

def drawGameOverMenuBar(score: int, record: int) -> ("void"):

    textFont   = pygame.font.Font(TEXT_FONT, TEXT_SIZE)
    scoreSurf  = textFont.render("SCORE: "  + str(score) , True, TEXT_COLOR)
    recordSurf = textFont.render("RECORD: " + str(record), True, TEXT_COLOR)
    scoreRect  = scoreSurf.get_rect()
    recordRect = recordSurf.get_rect()
    scoreRect.center  = (250,400)
    recordRect.center = (490,400)

    DISPLAYSURF.blit(scoreSurf, scoreRect)
    DISPLAYSURF.blit(recordSurf, recordRect)
    drawRestartButton(WINDOW_WIDTH_CENTER - (MENUBARBUTTON_SIZE * 2) - (MENUBARBUTTON_SIZE // 2), WINDOW_HEIGHT_CENTER + (CELL_SIZE * 2))
    drawMenuButton(WINDOW_WIDTH_CENTER - (MENUBARBUTTON_SIZE // 2), WINDOW_HEIGHT_CENTER + (CELL_SIZE * 2))
    drawExitButton(WINDOW_WIDTH_CENTER + MENUBARBUTTON_SIZE + (MENUBARBUTTON_SIZE // 2)  , WINDOW_HEIGHT_CENTER + (CELL_SIZE * 2))

def drawPauseGameMenuBar() -> ("void"):
    drawResumeGameButton(WINDOW_WIDTH_CENTER - (MENUBARBUTTON_SIZE * 3) - (MENUBARBUTTON_SIZE // 2),
                                                WINDOW_HEIGHT_CENTER - (PAUSEIMAGE_HEIGHT // 2))
    drawRestartButton(WINDOW_WIDTH_CENTER    - (MENUBARBUTTON_SIZE * 1) - (MENUBARBUTTON_SIZE // 2),
                                                WINDOW_HEIGHT_CENTER - (PAUSEIMAGE_HEIGHT // 2))
    drawMenuButton(WINDOW_WIDTH_CENTER       + (MENUBARBUTTON_SIZE * 1) - (MENUBARBUTTON_SIZE // 2),
                                                WINDOW_HEIGHT_CENTER - (PAUSEIMAGE_HEIGHT // 2))
    drawExitButton(WINDOW_WIDTH_CENTER       + (MENUBARBUTTON_SIZE * 3) - (MENUBARBUTTON_SIZE // 2),
                                                WINDOW_HEIGHT_CENTER - (PAUSEIMAGE_HEIGHT // 2))
def drawSureToQuitMenu(pause: bool, gameOver: int) -> ("void"):

    if pause:
        sureToQuitImageCenter = (WINDOW_WIDTH_CENTER  - (SURETOQUITIMAGE_WDITH //2),
                                 WINDOW_HEIGHT_CENTER + PAUSEIMAGE_HEIGHT)
        checkButtonTopLeft    = (WINDOW_WIDTH_CENTER  - MENUBARBUTTON_SIZE - (MENUBARBUTTON_SIZE // 2),
                                 WINDOW_HEIGHT_CENTER + (PAUSEIMAGE_HEIGHT * 2))
        closeButtonTopleft    = (WINDOW_WIDTH_CENTER  + MENUBARBUTTON_SIZE - (MENUBARBUTTON_SIZE // 2),
                                 WINDOW_HEIGHT_CENTER + (PAUSEIMAGE_HEIGHT * 2))

    elif gameOver:
        sureToQuitImageCenter = (WINDOW_WIDTH_CENTER  - (SURETOQUITIMAGE_WDITH //2),
                                 WINDOW_HEIGHT_CENTER + (WINDOW_WIDTH_CENTER // 3) + 10)
        checkButtonTopLeft    = (WINDOW_WIDTH_CENTER  - MENUBARBUTTON_SIZE - (MENUBARBUTTON_SIZE // 2),
                                 WINDOW_HEIGHT_CENTER + (WINDOW_WIDTH_CENTER // 2))
        closeButtonTopleft    = (WINDOW_WIDTH_CENTER  + MENUBARBUTTON_SIZE - (MENUBARBUTTON_SIZE // 2),
                                 WINDOW_HEIGHT_CENTER + (WINDOW_WIDTH_CENTER // 2))

    drawSureToQuitImage(sureToQuitImageCenter[0], sureToQuitImageCenter[1])
    drawCheckButton(checkButtonTopLeft[0]       , checkButtonTopLeft[1])
    drawCloseButton(closeButtonTopleft[0]       , closeButtonTopleft[1])

############################
#######  GAME PHASES #######
############################

def displayMainMenu() -> ("void"):
    global backgroundMusicState
    backgroundMusicState = ON
    play = False
    while not play:
        drawBackgroundImage()
        drawTitle()
        drawCredits()
        drawPlayButton()
        drawSoundButton()

        # Event handling loop
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            elif event.type == KEYUP:
                if event.key == K_RETURN or event.key == K_SPACE:
                    BUTTONCLICKSOUND.play()
                    play = True
                elif event.key == K_m:
                    changeAudioState()
            
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if PLAYBUTTONRECT.collidepoint(mousex, mousey):
                    BUTTONCLICKSOUND.play()
                    play = True

                checkAudioState(mousex, mousey)
        
        pygame.display.update()
    pygame.event.get()

def displayLevelSelectionMenu() -> ("void"):
    
    global gameSpeed, backgroundMusicState

    play = False
    drawLevelMenu()
    highlightedButton     = EASYLEVELBUTTON
    highlightedButtonRect = EASYLEVELBUTTONRECT
    while not play:
        drawBackgroundImage()
        drawTitle()
        drawCredits()
        drawLevelMenu()
        drawSoundButton()
        highlightLevelButton(highlightedButtonRect, highlightedButton)

        # Event handling loop
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
                if EASYLEVELBUTTONRECT.collidepoint(mousex, mousey):
                    highlightedButton, highlightedButtonRect = EASYLEVELBUTTON, EASYLEVELBUTTONRECT
                elif MEDIUMLEVELBUTTONRECT.collidepoint(mousex, mousey):
                    highlightedButton, highlightedButtonRect = MEDIUMLEVELBUTTON, MEDIUMLEVELBUTTONRECT
                elif HARDLEVELBUTTONRECT.collidepoint(mousex, mousey):
                    highlightedButton, highlightedButtonRect = HARDLEVELBUTTON, HARDLEVELBUTTONRECT

            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if EASYLEVELBUTTONRECT.collidepoint(mousex, mousey):
                    gameSpeed = GAME_SPEED_EASY
                    play      = True
                    BUTTONCLICKSOUND.play()
                elif MEDIUMLEVELBUTTONRECT.collidepoint(mousex, mousey):
                    gameSpeed = GAME_SPEED_MEDIUM
                    play      = True
                    BUTTONCLICKSOUND.play()
                elif HARDLEVELBUTTONRECT.collidepoint(mousex, mousey):
                    gameSpeed = GAME_SPEED_HARD
                    play      = True
                    BUTTONCLICKSOUND.play()

                checkAudioState(mousex, mousey)   

            elif event.type == KEYUP:
                if event.key == K_UP:
                    highlightedButton, highlightedButtonRect = changeHighlightedLevelButton(highlightedButton, highlightedButtonRect, UP)
                elif event.key == K_DOWN:
                    highlightedButton, highlightedButtonRect = changeHighlightedLevelButton(highlightedButton, highlightedButtonRect, DOWN)
                elif event.key == K_RETURN or event.key == K_SPACE:
                    BUTTONCLICKSOUND.play()
                    if highlightedButton == EASYLEVELBUTTON:
                        gameSpeed = GAME_SPEED_EASY
                        play      = True
                    elif highlightedButton == MEDIUMLEVELBUTTON:
                        gameSpeed = GAME_SPEED_MEDIUM
                        play      = True
                    elif highlightedButton == HARDLEVELBUTTON:
                        gameSpeed = GAME_SPEED_HARD
                        play      = True
                elif event.key == K_m:
                    changeAudioState()

        pygame.display.update()
    pygame.event.get()

def gameCountdown() -> ("void"):
    global backgroundMusicState
    countDownNumber = 3
    timeMark  = time.time()
    countDown = [ GOIMAGE, NUMBER1IMAGE, NUMBER2IMAGE, NUMBER3IMAGE ]
    while countDownNumber >= 0:

        # Event handling loop
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos            
                checkAudioState(mousex, mousey)

            if event.type == KEYUP:
                if event.key == K_m:
                    changeAudioState()

        drawBackgroundImage()
        drawSoundButton()
        DISPLAYSURF.blit(countDown[countDownNumber] , 
                        (COUNTDOWN_NUMBER_CENTER_X - (COUNTDOWN_NUMBER_SIZE // 2),
                         COUNTDOWN_NUMBER_CENTER_Y - (COUNTDOWN_NUMBER_SIZE // 2)))
        if time.time() - timeMark > COUNTDOWN_LENGHT:
            countDownNumber -= 1
            timeMark = time.time()

        pygame.display.update()
    pygame.event.get()

def runGame() -> (bool, bool):
    global backgroundMusicState
    restart  = False
    quitGame = False
    goToMenu = False
    snakeCoords, snakeLenght, appleCoords, direction, \
    score, record, newRecord, gameOver = initializeGame()

    while not gameOver and not restart and not quitGame and not goToMenu:

        # 1: Event handling loop
        for event in pygame.event.get():

            # Player closed window
            if event.type == QUIT:
                terminate()

            # Player pressed a key
            elif event.type == KEYDOWN:

                if   event.key == K_UP or event.key == K_w:
                    if validDirection(snakeCoords, UP):
                        direction = updateDirection(direction, UP)

                elif event.key == K_DOWN or event.key == K_s:
                    if validDirection(snakeCoords, DOWN):
                        direction = updateDirection(direction, DOWN)

                elif event.key == K_RIGHT or event.key == K_d:
                    if validDirection(snakeCoords, RIGHT):
                        direction = updateDirection(direction, RIGHT)

                elif event.key == K_LEFT or event.key == K_a:
                    if validDirection(snakeCoords, LEFT):
                        direction = updateDirection(direction, LEFT)

            elif event.type == KEYUP:

                if event.key == K_m:
                    changeAudioState()

                elif event.key == K_SPACE:
                     restart, quitGame, goToMenu = displayPauseScreen(snakeCoords, snakeLenght, appleCoords, score, record)

            # Player clicked
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                checkAudioState(mousex, mousey)

        # 2: update game
        moveSnake(snakeCoords, snakeLenght, appleCoords, direction)
        snakeLenght, appleCoords, score = checkAppleEaten(snakeCoords, snakeLenght, appleCoords, score)
        record, newRecord               = CompareScoreAndRecord(score, record, newRecord)
        gameOver                        = endOfGame(snakeCoords, snakeLenght)
        
        # 3: Display game
        displayGame(snakeCoords, snakeLenght, appleCoords, score, record)

    if not restart and not quitGame and not goToMenu:
        restart ,quitGame, goToMenu = CheckGameRecord(snakeCoords, snakeLenght, appleCoords, score, record, newRecord)
    
    pygame.event.get()

    return restart, quitGame

def displayGameOver(snakeCoords: [{int}], snakeLenght: int, appleCoords: {int},
                    score: int, record: int, newRecord: bool) -> (bool, bool, bool):
    
    drawGameOverMenuBar(score, record)
    restart  = False
    quitGame = False
    goToMenu = False
    highlightedButton     = RESTARTBUTTON
    highlightedButtonRect = RESTARTBUTTONRECT
    highlightedButtonSize = MENUBARBUTTON_SIZE
    while not restart and not quitGame and not goToMenu:

        # Event handling loop
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYUP: 
                if event.key == K_m:
                    changeAudioState()
                elif event.key == K_RIGHT:
                    highlightedButton, highlightedButtonRect = \
                    changeHighlightedGameOverMenuButtonByKeyboard(highlightedButton, highlightedButtonRect, RIGHT)
                elif event.key == K_LEFT:
                    highlightedButton, highlightedButtonRect = \
                    changeHighlightedGameOverMenuButtonByKeyboard(highlightedButton, highlightedButtonRect, LEFT)
                elif event.key == K_SPACE or event.key == K_RETURN:
                    restart, quitGame, goToMenu = checkGameOverMenuBar(highlightedButton)
                    if quitGame:
                        quitGame = displaySureToQuit(snakeCoords, snakeLenght, appleCoords, score, record, False, True)

            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if mouseIsOverGameOverMenuButton(mousex, mousey):
                    restart, quitGame, goToMenu = checkGameOverMenuBar(highlightedButton)
                    if quitGame:
                        quitGame = displaySureToQuit(snakeCoords, snakeLenght, appleCoords, score, record, False, True)

                checkAudioState(mousex, mousey) 

            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
                highlightedButton, highlightedButtonRect = changeHighlightedGameOverButtonByMouse(highlightedButton, highlightedButtonRect, mousex, mousey)

        drawBackgroundImage()
        drawGameOverImage()
        drawGameOverMenuBar(score, record)
        drawSoundButton()
        highlightMenuButton(highlightedButtonRect, highlightedButton, highlightedButtonSize)
 
        if newRecord:
            drawNewRecord()

        pygame.display.update()
    pygame.event.get()  

    return restart, quitGame, goToMenu  

def displayGame(snakeCoords: [{int}], snakeLenght: int, appleCoords: {int}, score: int, record: int) -> ("void"):

    DISPLAYSURF.fill(GAME_BACKGROUND_COLOR)
    drawBackgroundImage()
    drawSnake(snakeCoords, snakeLenght)
    drawApple(appleCoords)
    drawScore(score)
    drawRecord(record)
    drawSoundButton()
    pygame.display.update()
    FPSCLOCK.tick(gameSpeed)

def displayPauseScreen(snakeCoords: [{int}], snakeLenght: int, appleCoords: {int},
                       score: int, record: int) -> (bool, bool, bool):
    play     = False
    restart  = False
    quitGame = False
    goToMenu = False
    drawPauseGameMenuBar()
    highlightedButton     = RESUMEGAMEBUTTON
    highlightedButtonRect = RESUMEGAMEBUTTONRECT
    highlightedButtonSize = MENUBARBUTTON_SIZE

    while not play and not restart and not quitGame and not goToMenu:
        drawBackgroundImage()
        drawSnake(snakeCoords, snakeLenght)
        drawApple(appleCoords)
        drawScore(score)
        drawRecord(record)
        drawSoundButton()
        drawPauseImage()
        drawPauseGameMenuBar()
        highlightMenuButton(highlightedButtonRect, highlightedButton, highlightedButtonSize)

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYUP:
                if event.key == K_m:
                    changeAudioState()
                elif event.key == K_SPACE:
                    BUTTONCLICKSOUND.play()
                    play = True
                elif event.key == K_RIGHT:
                    highlightedButton, highlightedButtonRect = changeHighlightedMenuButtonByKeyboard(highlightedButton, highlightedButtonRect, RIGHT)
                elif event.key == K_LEFT:
                    highlightedButton, highlightedButtonRect = changeHighlightedMenuButtonByKeyboard(highlightedButton, highlightedButtonRect, LEFT)
                elif event.key == K_RETURN:
                    play, restart, quitGame, goToMenu = checkPauseMenuBar(highlightedButton)
                    if quitGame:
                        quitGame = displaySureToQuit(snakeCoords, snakeLenght, appleCoords, score, record, True, False)

            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if mouseIsOverPauseMenuButton(mousex, mousey):
                    play, restart, quitGame, goToMenu = checkPauseMenuBar(highlightedButton)
                    if quitGame:
                        quitGame = displaySureToQuit(snakeCoords, snakeLenght, appleCoords, score, record, True, False)

                checkAudioState(mousex, mousey) 

            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
                highlightedButton, highlightedButtonRect = changeHighlightedMenuButtonByMouse(highlightedButton, highlightedButtonRect, mousex, mousey)

        pygame.display.update()
    pygame.event.get()

    return restart, quitGame, goToMenu

def displaySureToQuit(snakeCoords: [{int}], snakeLenght: int, appleCoords: {int},
                      score: int, record: int, pause: bool, gameOver: bool) -> (bool):
    
    closeQuitMenu = False
    drawSureToQuitMenu(pause, gameOver)
    highlightedButton     = CHECKBUTTON
    highlightedButtonRect = CHECKBUTTONRECT
    highlightedButtonSize = MENUBARBUTTON_SIZE

    while not closeQuitMenu:
        if pause:
            drawBackgroundImage()
            drawSnake(snakeCoords, snakeLenght)
            drawApple(appleCoords)
            drawScore(score)
            drawRecord(record)
            drawSoundButton()
            drawPauseImage()
            drawPauseGameMenuBar()            
            drawSureToQuitMenu(pause, gameOver)

        elif gameOver:
            drawBackgroundImage()
            drawGameOverImage()
            drawGameOverMenuBar(score, record)
            drawSoundButton()
            drawSureToQuitMenu(pause, gameOver)
        
        highlightMenuButton(highlightedButtonRect, highlightedButton, highlightedButtonSize)

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            elif event.type == KEYUP:
                if event.key == K_RIGHT:
                    highlightedButton, highlightedButtonRect = changeHighlightedQuitButtonByKeyboard(highlightedButton, highlightedButtonRect, RIGHT)
                elif event.key == K_LEFT:
                    highlightedButton, highlightedButtonRect = changeHighlightedQuitButtonByKeyboard(highlightedButton, highlightedButtonRect, LEFT)
                elif event.key == K_RETURN:
                    quitGame = checkQuitMenuBar(highlightedButton)
                    closeQuitMenu = True

            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
                highlightedButton, highlightedButtonRect = changeHighlightedQuitButtonByMouse(highlightedButton, highlightedButtonRect, mousex, mousey)

            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if mouseIsOverQuitMenuButton(mousex, mousey):
                    quitGame = checkQuitMenuBar(highlightedButton)
                    closeQuitMenu = True

                checkAudioState(mousex, mousey)

        pygame.display.update()
    pygame.event.get()
    return quitGame

###############################
########## MAIN GAME ##########
###############################

exit = False
beginBackgroundMusic()
while not exit:
    restartGame = True
    displayMainMenu()
    displayLevelSelectionMenu()
    while restartGame:
        gameCountdown()
        restartGame, exit = runGame()