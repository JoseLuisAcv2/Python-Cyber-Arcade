# Simon Says Game
#
# By Jose Acevedo
#
# © Copyright 2015.

import pygame
import time
import sys
import os
import random

pygame.init()

# COLORS         R    G    B
WHITE        = (255, 255, 255)
GRAY         = (28 , 41 , 41 )
LIGHTGRAY    = (50 , 80 , 80 )
BLACK        = (0  , 0  , 0  )
SKYBLUE      = (135, 206, 234)
YELLOW       = (155, 155, 0  )
BRIGHTYELLOW = (255, 255, 50 )
BLUE         = (0  , 0  , 155)
BRIGHTBLUE   = (50 , 50 , 255)
RED          = (155, 0  , 0  )
BRIGHTRED    = (255, 50 , 50 )
GREEN        = (0  , 155, 0  )
BRIGHTGREEN  = (50 , 255, 50 )

# GAME SETTINGS
# DISPLAY
BACKGROUND_COLOR           = SKYBLUE
BACKGROUND_COLOR_GAME_OVER = RED
BACKGROUND_COLOR_WIN       = BRIGHTGREEN
BOARD_COLOR                = LIGHTGRAY
WINDOW_WIDTH               = 710
WINDOW_HEIGHT              = 750
WINDOW_WIDTH_CENTER        = WINDOW_WIDTH  // 2
WINDOW_HEIGHT_CENTER       = WINDOW_HEIGHT // 2
BUTTON_SIZE                = 230
BUTTON_GAP_SIZE            = 25
BUTTONS_PER_ROW            = 2
BUTTONS_PER_COLUMN         = 2
BOARD_WIDTH                = BUTTONS_PER_ROW    * ( BUTTON_SIZE + BUTTON_GAP_SIZE ) + BUTTON_GAP_SIZE
BOARD_HEIGHT               = BUTTONS_PER_COLUMN * ( BUTTON_SIZE + BUTTON_GAP_SIZE ) + BUTTON_GAP_SIZE
BOARD_WIDTH_CENTER         = WINDOW_WIDTH_CENTER
BOARD_HEIGHT_CENTER        = WINDOW_HEIGHT_CENTER
CORNER_ROUNDNESS           = 20
BOARD_CORNER_SQUARE_WIDTH  = BOARD_WIDTH  // CORNER_ROUNDNESS
BOARD_CORNER_SQUARE_HEIGHT = BOARD_HEIGHT // CORNER_ROUNDNESS
BOARD_CORNER_CIRCLE_RADIUS = BOARD_WIDTH  // CORNER_ROUNDNESS
BOARD_TOPLEFT_X            = BOARD_WIDTH_CENTER  - (BOARD_WIDTH  // 2)
BOARD_TOPLEFT_Y            = BOARD_HEIGHT_CENTER - (BOARD_HEIGHT // 2)
BOARD_TOPRIGHT_X           = BOARD_TOPLEFT_X + BOARD_WIDTH - BOARD_CORNER_SQUARE_WIDTH
BOARD_TOPRIGHT_Y           = BOARD_TOPLEFT_Y
BOARD_BOTTOMLEFT_X         = BOARD_TOPLEFT_X
BOARD_BOTTOMLEFT_Y         = BOARD_TOPLEFT_Y + BOARD_HEIGHT - BOARD_CORNER_SQUARE_HEIGHT
BOARD_BOTTOMRIGHT_X        = BOARD_TOPRIGHT_X
BOARD_BOTTOMRIGHT_Y        = BOARD_BOTTOMLEFT_Y
PLAYBUTTON_WIDTH           = 200
PLAYBUTTON_HEIGHT          = 150
PLAYBUTTON_TOPLEFT_X       = WINDOW_WIDTH_CENTER  - (PLAYBUTTON_WIDTH // 2)
PLAYBUTTON_TOPLEFT_Y       = WINDOW_HEIGHT_CENTER
FLASHSPEED                 = 800
TIMEOUT                    = 4

# TEXT
FONT_STYLE                 = "freesansbold.ttf"
GAME_TITLE                 = "SIMON SAYS"
CREDITS_TEXT               = "© Jose Acevedo"
SCORE_TEXT                 = "SCORE"
RECORD_TEXT                = "RECORD"
TURN_MESSAGE               = "Your turn!"
WRONG_MESSAGE              = "Wrong!"
CORRECT_MESSAGE            = "Correct!"
TITLE_TEXT_COLOR           = LIGHTGRAY
CREDITS_TEXT_COLOR         = BLACK
SCORE_TEXT_COLOR           = GRAY
SCORE_FONT_SIZE            = 35
TITLE_FONT_SIZE            = 85
CREDITS_FONT_SIZE          = 13
TITLE_CENTER_X             = WINDOW_WIDTH_CENTER
TITLE_CENTER_Y             = WINDOW_HEIGHT_CENTER - (WINDOW_HEIGHT_CENTER // 3)
CREDITS_CENTER_X           = TITLE_CENTER_X + 200
CREDITS_CENTER_Y           = TITLE_CENTER_Y + 40
SCORE_TEXT_CENTER_X        = BOARD_TOPLEFT_X  + BUTTON_GAP_SIZE + (BUTTON_SIZE // 4)
SCORE_TEXT_CENTER_Y        = BOARD_TOPLEFT_Y  - (2 * BUTTON_GAP_SIZE)
SCORE_VALUE_CENTER_X       = BOARD_TOPLEFT_X  + BUTTON_GAP_SIZE + (BUTTON_SIZE * 2 // 3)
SCORE_VALUE_CENTER_Y       = BOARD_TOPLEFT_Y  - (2 * BUTTON_GAP_SIZE)
RECORD_TEXT_CENTER_X       = BOARD_TOPRIGHT_X - BUTTON_GAP_SIZE - (BUTTON_SIZE // 2)
RECORD_TEXT_CENTER_Y       = BOARD_TOPLEFT_Y  - (2 * BUTTON_GAP_SIZE)
RECORD_VALUE_CENTER_X      = BOARD_TOPRIGHT_X - BUTTON_GAP_SIZE
RECORD_VALUE_CENTER_Y      = BOARD_TOPLEFT_Y  - (2 * BUTTON_GAP_SIZE)
TURN_TEXT_CENTER_X         = BOARD_WIDTH_CENTER
TURN_TEXT_CENTER_Y         = BOARD_BOTTOMRIGHT_Y + (PLAYBUTTON_WIDTH // 4)

# BUTTONS
PLAYBUTTON = pygame.image.load("PlayButton.png")
PLAYBUTTON = pygame.transform.scale(PLAYBUTTON,(PLAYBUTTON_WIDTH, PLAYBUTTON_HEIGHT))

# SOUNDS
YELLOWSOUND  = pygame.mixer.Sound("NoteC.wav")
BLUESOUND    = pygame.mixer.Sound("NoteD.wav")
REDSOUND     = pygame.mixer.Sound("NoteE.wav")
GREENSOUND   = pygame.mixer.Sound("NoteF.wav")
BUTTONPRESS  = pygame.mixer.Sound("ButtonPress.wav")
WRONGSOUND   = pygame.mixer.Sound("Wrong.wav")
CORRECTSOUND = pygame.mixer.Sound("Win.wav")

# SCREEN
DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("SIMON SAYS")

def InitializeGame() -> ([(int)], int, int, bool, bool, bool, bool):
    colorPattern  = []
    patternLenght = 0
    currentStep   = 0
    score         = 0
    playerTurn    = False
    gameOver      = False
    waitingInput  = False
    win           = False

    patternLenght = AddNewColorToPattern(colorPattern, patternLenght)

    return colorPattern, patternLenght, currentStep, score, playerTurn, gameOver, waitingInput, win

def ButtonSetUp() -> ("rect", "rect", "rect", "rect", "rect"):
    YELLOWRECT = pygame.Rect(BOARD_WIDTH_CENTER  - BUTTON_SIZE - (BUTTON_GAP_SIZE // 2),
                             BOARD_HEIGHT_CENTER - BUTTON_SIZE - (BUTTON_GAP_SIZE // 2),
                             BUTTON_SIZE, BUTTON_SIZE)
    BLUERECT   = pygame.Rect(BOARD_WIDTH_CENTER + (BUTTON_GAP_SIZE // 2),
                             BOARD_HEIGHT_CENTER - BUTTON_SIZE - (BUTTON_GAP_SIZE // 2),
                             BUTTON_SIZE, BUTTON_SIZE)
    REDRECT    = pygame.Rect(BOARD_WIDTH_CENTER  - BUTTON_SIZE - (BUTTON_GAP_SIZE // 2),
                             BOARD_HEIGHT_CENTER + (BUTTON_GAP_SIZE // 2),
                             BUTTON_SIZE, BUTTON_SIZE)
    GREENRECT  = pygame.Rect(BOARD_WIDTH_CENTER  + (BUTTON_GAP_SIZE // 2),
                             BOARD_HEIGHT_CENTER + (BUTTON_GAP_SIZE // 2),
                             BUTTON_SIZE, BUTTON_SIZE)
    BOARDRECT  = pygame.Rect(BOARD_TOPLEFT_X, BOARD_TOPLEFT_Y , BOARD_WIDTH, BOARD_HEIGHT)

    return YELLOWRECT, BLUERECT, REDRECT, GREENRECT, BOARDRECT

def AddNewColorToPattern(colorPattern: [(int)], patternLenght: int) -> ([(int)], int):
    newColor = random.choice([YELLOW, BLUE, RED, GREEN])
    colorPattern.append(newColor)
    patternLenght = patternLenght + 1

    return patternLenght

def GetButtonClicked(mousex: int, mousey: int, YELLOWRECT: "rect", BLUERECT: "rect", REDRECT: "rect", GREENRECT: "rect") -> ([(int)]):
    if YELLOWRECT.collidepoint(mousex, mousey):
        buttonClicked = YELLOW
        YELLOWSOUND.play()

    elif BLUERECT.collidepoint(mousex, mousey):
        buttonClicked = BLUE
        BLUESOUND.play()

    elif REDRECT.collidepoint(mousex, mousey):
        buttonClicked = RED
        REDSOUND.play()

    elif GREENRECT.collidepoint(mousex, mousey):
        buttonClicked = GREEN
        GREENSOUND.play()

    else:
        buttonClicked = None

    return buttonClicked

def ClickedButton(mousex: int, mousey: int, YELLOWRECT: "rect", BLUERECT: "rect", REDRECT: "rect", GREENRECT: "rect") -> (bool):
    if YELLOWRECT.collidepoint(mousex, mousey) or BLUERECT.collidepoint(mousex, mousey) or \
       REDRECT.collidepoint(mousex, mousey)    or GREENRECT.collidepoint(mousex, mousey):
       return True
    else:
        return False

def ChoseWell(chosenColor: (int), colorPattern: [(int)], currentStep: int) -> (bool):
    rightColor = colorPattern[currentStep]
    if chosenColor == rightColor:
        return True
    else:
        return False

##################
#### GRAPHICS ####
##################

def DisplayMenu() -> ("rect"):

    titleFont              = pygame.font.Font(FONT_STYLE, TITLE_FONT_SIZE)
    creditsFont            = pygame.font.Font(FONT_STYLE, CREDITS_FONT_SIZE)

    titleSurf              = titleFont.render(GAME_TITLE    , True, TITLE_TEXT_COLOR)
    creditsSurf            = creditsFont.render(CREDITS_TEXT, True, CREDITS_TEXT_COLOR)

    titleRect              = titleSurf.get_rect()
    creditsRect            = creditsSurf.get_rect()
    playButtonRect         = PLAYBUTTON.get_rect()

    titleRect.center       = (TITLE_CENTER_X      , TITLE_CENTER_Y)
    creditsRect.center     = (CREDITS_CENTER_X    , CREDITS_CENTER_Y)
    playButtonRect.topleft = (PLAYBUTTON_TOPLEFT_X, PLAYBUTTON_TOPLEFT_Y)   

    DISPLAYSURF.fill(BACKGROUND_COLOR)

    DISPLAYSURF.blit(titleSurf  , titleRect)
    DISPLAYSURF.blit(creditsSurf, creditsRect)
    DISPLAYSURF.blit(PLAYBUTTON ,(PLAYBUTTON_TOPLEFT_X, PLAYBUTTON_TOPLEFT_Y))

    pygame.display.update()

    return playButtonRect

def DisplayGame(YELLOWRECT: "rect", BLUERECT: "rect", REDRECT: "rect", GREENRECT: "rect", BOARDRECT: "rect", score: int, record: int, gameOver: bool, win: bool) -> ("void"):

    scoreFont = pygame.font.Font(FONT_STYLE, SCORE_FONT_SIZE)

    if gameOver:

        WRONGSOUND.play()
        DISPLAYSURF.fill(BACKGROUND_COLOR_GAME_OVER)

        # BACKGROUND BOARD
        pygame.draw.rect(DISPLAYSURF, BOARD_COLOR, BOARDRECT)

        pygame.draw.rect(DISPLAYSURF, BACKGROUND_COLOR_GAME_OVER, (BOARD_TOPLEFT_X    , BOARD_TOPLEFT_Y    , BOARD_CORNER_SQUARE_WIDTH, BOARD_CORNER_SQUARE_HEIGHT))
        pygame.draw.rect(DISPLAYSURF, BACKGROUND_COLOR_GAME_OVER, (BOARD_TOPRIGHT_X   , BOARD_TOPRIGHT_Y   , BOARD_CORNER_SQUARE_WIDTH, BOARD_CORNER_SQUARE_HEIGHT))
        pygame.draw.rect(DISPLAYSURF, BACKGROUND_COLOR_GAME_OVER, (BOARD_BOTTOMLEFT_X , BOARD_BOTTOMLEFT_Y , BOARD_CORNER_SQUARE_WIDTH, BOARD_CORNER_SQUARE_HEIGHT))
        pygame.draw.rect(DISPLAYSURF, BACKGROUND_COLOR_GAME_OVER, (BOARD_BOTTOMRIGHT_X, BOARD_BOTTOMRIGHT_Y, BOARD_CORNER_SQUARE_WIDTH, BOARD_CORNER_SQUARE_HEIGHT))
        pygame.draw.circle(DISPLAYSURF, BOARD_COLOR, (BOARD_TOPLEFT_X + BOARD_CORNER_CIRCLE_RADIUS, BOARD_TOPLEFT_Y + BOARD_CORNER_CIRCLE_RADIUS), BOARD_CORNER_CIRCLE_RADIUS)
        pygame.draw.circle(DISPLAYSURF, BOARD_COLOR, (BOARD_TOPRIGHT_X, BOARD_TOPRIGHT_Y + BOARD_CORNER_CIRCLE_RADIUS), BOARD_CORNER_CIRCLE_RADIUS)
        pygame.draw.circle(DISPLAYSURF, BOARD_COLOR, (BOARD_BOTTOMLEFT_X + BOARD_CORNER_CIRCLE_RADIUS, BOARD_BOTTOMLEFT_Y), BOARD_CORNER_CIRCLE_RADIUS)
        pygame.draw.circle(DISPLAYSURF, BOARD_COLOR, (BOARD_BOTTOMRIGHT_X, BOARD_BOTTOMRIGHT_Y), BOARD_CORNER_CIRCLE_RADIUS)

        turnTextSurf        = scoreFont.render(WRONG_MESSAGE, True, SCORE_TEXT_COLOR)
        turnTextRect        = turnTextSurf.get_rect()
        turnTextRect.center = (TURN_TEXT_CENTER_X, TURN_TEXT_CENTER_Y)
        DISPLAYSURF.blit(turnTextSurf, turnTextRect)
    
    elif win:

        CORRECTSOUND.play()
        DISPLAYSURF.fill(BACKGROUND_COLOR_WIN)

        # BACKGROUND BOARD
        pygame.draw.rect(DISPLAYSURF, BOARD_COLOR, BOARDRECT)

        pygame.draw.rect(DISPLAYSURF, BACKGROUND_COLOR_WIN, (BOARD_TOPLEFT_X    , BOARD_TOPLEFT_Y    , BOARD_CORNER_SQUARE_WIDTH, BOARD_CORNER_SQUARE_HEIGHT))
        pygame.draw.rect(DISPLAYSURF, BACKGROUND_COLOR_WIN, (BOARD_TOPRIGHT_X   , BOARD_TOPRIGHT_Y   , BOARD_CORNER_SQUARE_WIDTH, BOARD_CORNER_SQUARE_HEIGHT))
        pygame.draw.rect(DISPLAYSURF, BACKGROUND_COLOR_WIN, (BOARD_BOTTOMLEFT_X , BOARD_BOTTOMLEFT_Y , BOARD_CORNER_SQUARE_WIDTH, BOARD_CORNER_SQUARE_HEIGHT))
        pygame.draw.rect(DISPLAYSURF, BACKGROUND_COLOR_WIN, (BOARD_BOTTOMRIGHT_X, BOARD_BOTTOMRIGHT_Y, BOARD_CORNER_SQUARE_WIDTH, BOARD_CORNER_SQUARE_HEIGHT))
        pygame.draw.circle(DISPLAYSURF, BOARD_COLOR, (BOARD_TOPLEFT_X + BOARD_CORNER_CIRCLE_RADIUS, BOARD_TOPLEFT_Y + BOARD_CORNER_CIRCLE_RADIUS), BOARD_CORNER_CIRCLE_RADIUS)
        pygame.draw.circle(DISPLAYSURF, BOARD_COLOR, (BOARD_TOPRIGHT_X, BOARD_TOPRIGHT_Y + BOARD_CORNER_CIRCLE_RADIUS), BOARD_CORNER_CIRCLE_RADIUS)
        pygame.draw.circle(DISPLAYSURF, BOARD_COLOR, (BOARD_BOTTOMLEFT_X + BOARD_CORNER_CIRCLE_RADIUS, BOARD_BOTTOMLEFT_Y), BOARD_CORNER_CIRCLE_RADIUS)
        pygame.draw.circle(DISPLAYSURF, BOARD_COLOR, (BOARD_BOTTOMRIGHT_X, BOARD_BOTTOMRIGHT_Y), BOARD_CORNER_CIRCLE_RADIUS)

        turnTextSurf        = scoreFont.render(CORRECT_MESSAGE, True, SCORE_TEXT_COLOR)
        turnTextRect        = turnTextSurf.get_rect()
        turnTextRect.center = (TURN_TEXT_CENTER_X, TURN_TEXT_CENTER_Y)
        DISPLAYSURF.blit(turnTextSurf, turnTextRect)

    else:
        DISPLAYSURF.fill(BACKGROUND_COLOR)
    
        # BACKGROUND BOARD
        pygame.draw.rect(DISPLAYSURF, BOARD_COLOR, BOARDRECT)
    
        # ROUNDED CORNERS
        pygame.draw.rect(DISPLAYSURF, BACKGROUND_COLOR, (BOARD_TOPLEFT_X    , BOARD_TOPLEFT_Y    , BOARD_CORNER_SQUARE_WIDTH, BOARD_CORNER_SQUARE_HEIGHT))
        pygame.draw.rect(DISPLAYSURF, BACKGROUND_COLOR, (BOARD_TOPRIGHT_X   , BOARD_TOPRIGHT_Y   , BOARD_CORNER_SQUARE_WIDTH, BOARD_CORNER_SQUARE_HEIGHT))
        pygame.draw.rect(DISPLAYSURF, BACKGROUND_COLOR, (BOARD_BOTTOMLEFT_X , BOARD_BOTTOMLEFT_Y , BOARD_CORNER_SQUARE_WIDTH, BOARD_CORNER_SQUARE_HEIGHT))
        pygame.draw.rect(DISPLAYSURF, BACKGROUND_COLOR, (BOARD_BOTTOMRIGHT_X, BOARD_BOTTOMRIGHT_Y, BOARD_CORNER_SQUARE_WIDTH, BOARD_CORNER_SQUARE_HEIGHT))
        pygame.draw.circle(DISPLAYSURF, BOARD_COLOR, (BOARD_TOPLEFT_X + BOARD_CORNER_CIRCLE_RADIUS, BOARD_TOPLEFT_Y + BOARD_CORNER_CIRCLE_RADIUS), BOARD_CORNER_CIRCLE_RADIUS)
        pygame.draw.circle(DISPLAYSURF, BOARD_COLOR, (BOARD_TOPRIGHT_X, BOARD_TOPRIGHT_Y + BOARD_CORNER_CIRCLE_RADIUS), BOARD_CORNER_CIRCLE_RADIUS)
        pygame.draw.circle(DISPLAYSURF, BOARD_COLOR, (BOARD_BOTTOMLEFT_X + BOARD_CORNER_CIRCLE_RADIUS, BOARD_BOTTOMLEFT_Y), BOARD_CORNER_CIRCLE_RADIUS)
        pygame.draw.circle(DISPLAYSURF, BOARD_COLOR, (BOARD_BOTTOMRIGHT_X, BOARD_BOTTOMRIGHT_Y), BOARD_CORNER_CIRCLE_RADIUS)

    # BUTTONS
    pygame.draw.rect(DISPLAYSURF, YELLOW, YELLOWRECT)
    pygame.draw.rect(DISPLAYSURF, BLUE  , BLUERECT)
    pygame.draw.rect(DISPLAYSURF, RED   , REDRECT)
    pygame.draw.rect(DISPLAYSURF, GREEN , GREENRECT)

    # SCORE & RECORD
    scoreTextSurf   = scoreFont.render(SCORE_TEXT , True, SCORE_TEXT_COLOR)
    scoreValueSurf  = scoreFont.render(str(score) , True, SCORE_TEXT_COLOR)
    recordTextSurf  = scoreFont.render(RECORD_TEXT, True, SCORE_TEXT_COLOR)
    recordValueSurf = scoreFont.render(str(record), True, SCORE_TEXT_COLOR)

    scoreTextRect   = scoreTextSurf.get_rect()
    scoreValueRect  = scoreValueSurf.get_rect()
    recordTextRect  = recordTextSurf.get_rect()
    recordValueRect = recordValueSurf.get_rect()

    scoreTextRect.center   = (SCORE_TEXT_CENTER_X  , SCORE_TEXT_CENTER_Y  )
    scoreValueRect.center  = (SCORE_VALUE_CENTER_X , SCORE_VALUE_CENTER_Y )
    recordTextRect.center  = (RECORD_TEXT_CENTER_X , RECORD_TEXT_CENTER_Y )
    recordValueRect.center = (RECORD_VALUE_CENTER_X, RECORD_VALUE_CENTER_Y)

    DISPLAYSURF.blit(scoreTextSurf  , scoreTextRect  )
    DISPLAYSURF.blit(scoreValueSurf , scoreValueRect )
    DISPLAYSURF.blit(recordTextSurf , recordTextRect )
    DISPLAYSURF.blit(recordValueSurf, recordValueRect)

    if playerTurn and not win and not gameOver:

        turnTextSurf        = scoreFont.render(TURN_MESSAGE, True, SCORE_TEXT_COLOR)
        turnTextRect        = turnTextSurf.get_rect()
        turnTextRect.center = (TURN_TEXT_CENTER_X, TURN_TEXT_CENTER_Y)
        DISPLAYSURF.blit(turnTextSurf, turnTextRect)

    pygame.display.update()

def FlashButton(colorPattern: [(int)], currentStep: int, YELLOWRECT: "rect", BLUERECT: "rect", REDRECT: "rect", GREENRECT: "rect") -> (int):
    color = colorPattern[currentStep]
    if color == YELLOW:
        pygame.draw.rect(DISPLAYSURF, BRIGHTYELLOW, YELLOWRECT)
        YELLOWSOUND.play()

    elif color == BLUE:
        pygame.draw.rect(DISPLAYSURF, BRIGHTBLUE, BLUERECT)
        BLUESOUND.play()

    elif color == RED:
        pygame.draw.rect(DISPLAYSURF, BRIGHTRED, REDRECT)
        REDSOUND.play()

    elif color == GREEN:
        pygame.draw.rect(DISPLAYSURF, BRIGHTGREEN, GREENRECT)
        GREENSOUND.play()

    pygame.display.update()
    pygame.time.wait(FLASHSPEED)

    pygame.draw.rect(DISPLAYSURF, YELLOW, YELLOWRECT)
    pygame.draw.rect(DISPLAYSURF, BLUE  , BLUERECT)
    pygame.draw.rect(DISPLAYSURF, RED   , REDRECT)
    pygame.draw.rect(DISPLAYSURF, GREEN , GREENRECT)
    pygame.display.update()

    currentStep = currentStep + 1
    return currentStep

##############
#### GAME ####
##############

play = False
while not play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            mousex, mousey = event.pos
            if playButton.collidepoint(mousex, mousey):
                play = True
                BUTTONPRESS.play()
    playButton = DisplayMenu()

colorPattern, patternLenght, currentStep, score, playerTurn, gameOver, waitingInput, win = InitializeGame()
buttonYellow, buttonBlue, buttonRed, buttonGreen, board = ButtonSetUp()
clicked   = False
newRecord = False
record    = 0
DisplayGame(buttonYellow, buttonBlue, buttonRed, buttonGreen, board, score, record, gameOver, win)
time.sleep(1)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            mousex, mousey = event.pos
            clicked = True

    DisplayGame(buttonYellow, buttonBlue, buttonRed, buttonGreen, board, score, record, gameOver, win)
    
    # SHOW PATTERN PHASE
    if not playerTurn:
        win = False
        if currentStep != patternLenght:
            currentStep = FlashButton(colorPattern, currentStep, buttonYellow, buttonBlue, buttonRed, buttonGreen)
        elif currentStep == patternLenght:
            currentStep   = 0
            playerTurn    = True

    # PLAYER TURN PHASE
    if playerTurn:
        if clicked and not waitingInput:
            if ClickedButton(mousex, mousey, buttonYellow, buttonBlue, buttonRed, buttonGreen):
                buttonClicked = GetButtonClicked(mousex, mousey, buttonYellow, buttonBlue, buttonRed, buttonGreen)
                if ChoseWell(buttonClicked, colorPattern, currentStep):
                    waitingInput    = True
                    currentStep     = 1
                    timeLastClicked = time.time()
                else:
                    gameOver = True
                    DisplayGame(buttonYellow, buttonBlue, buttonRed, buttonGreen, board, score, record, gameOver, win)
                    time.sleep(1)
                    colorPattern, patternLenght, currentStep, score, playerTurn, gameOver, waitingInput, win = InitializeGame()
            clicked = False

        if waitingInput:
            if clicked:
                buttonClicked = GetButtonClicked(mousex, mousey, buttonYellow, buttonBlue, buttonRed, buttonGreen)
                if buttonClicked != colorPattern[currentStep] and buttonClicked != None:
                    gameOver = True
                    DisplayGame(buttonYellow, buttonBlue, buttonRed, buttonGreen, board, score, record, gameOver, win)
                    time.sleep(1)
                    colorPattern, patternLenght, currentStep, score, playerTurn, gameOver, waitingInput, win = InitializeGame()
                elif buttonClicked == colorPattern[currentStep]:
                    currentStep += 1
                    timeLastClicked = time.time()

            if time.time() - timeLastClicked > TIMEOUT:
                gameOver = True
                DisplayGame(buttonYellow, buttonBlue, buttonRed, buttonGreen, board, score, record, gameOver, win)
                time.sleep(1)
                colorPattern, patternLenght, currentStep, score, playerTurn, gameOver, waitingInput, win = InitializeGame()

            if currentStep == patternLenght:
                win           = True
                DisplayGame(buttonYellow, buttonBlue, buttonRed, buttonGreen, board, score, record, gameOver, win)
                win           = False
                score        += 1
                currentStep   = 0
                playerTurn    = False
                waitingInput  = False
                patternLenght = AddNewColorToPattern(colorPattern, patternLenght)
                time.sleep(1)
    if score > record:
        record = score

    clicked = False