# 2048
#
# By Jose Acevedo
#
# © Copyright 2015.

import pygame
import sys
import random
import os.path
from pygame.locals import *

pygame.init()
pygame.mixer.init()

# GAME CONSTANTS

WHITE     = (255, 255, 255)
YELLOW    = (195, 195, 0  )
BLACK     = (0  , 0  , 0  )
GREEN     = (0  , 255, 0  )
GRAY      = (37 , 50 , 50 )
LIGHTGRAY = (47 , 79 , 79 )
CREAM     = (255, 253, 208)
SKYBLUE   = (135, 206, 234)

GREEN2    = (150, 177, 0  )
BLUE4     = (100 ,150, 210)
BLUE8     = (42 , 106, 255)
BLUE16    = (0  , 75 , 255)
BLUE32    = (0  , 50 , 255)
BLUE64    = (30 , 24 , 225)
BLUE128   = (15 , 15 , 185)
BLUE256   = (0  , 0  , 156)
BLUE512   = (0  , 0  , 112)
BLUE1024  = (0  , 0  , 82 )
BLUE2048  = (0  , 0  , 51 )

BACKGROUNDCOLOR                  = SKYBLUE
BOARD_BACKGROUND_COLOR           = LIGHTGRAY
END_OF_GAME_BOX_BACKGROUND_COLOR = YELLOW
EMPTYBOX_COLOR                   = CREAM
BOARD_WIDTH                      = 4
BOARD_HEIGHT                     = 4
NEW_TILE_POSSIBLE_VALUES         = [2, 4]
TILES_AT_BEGINNING               = 2 
UP                               = "up"
DOWN                             = "down"
RIGHT                            = "right"
LEFT                             = "left"
WINDOW_HEIGHT                    = 700
WINDOW_WIDTH                     = 700
WINDOW_WIDTH_CENTER              = WINDOW_WIDTH  // 2
WINDOW_HEIGHT_CENTER             = WINDOW_HEIGHT // 2 + 30
TILE_SIZE                        = 100
TILE_GAP                         = TILE_SIZE // 30
BOARD_TOPLEFT_CORNER_X           = WINDOW_WIDTH_CENTER  - ((BOARD_WIDTH  // 2) * (TILE_SIZE + TILE_GAP))
BOARD_TOPLEFT_CORNER_Y           = WINDOW_HEIGHT_CENTER - ((BOARD_HEIGHT // 2) * (TILE_SIZE + TILE_GAP))
BOARD_MARGIN_WIDTH               = TILE_GAP * 5
BOARD_MARGIN_TOPLEFTCORNER_X     = BOARD_TOPLEFT_CORNER_X - BOARD_MARGIN_WIDTH
BOARD_MARGIN_TOPLEFTCORNER_Y     = BOARD_TOPLEFT_CORNER_Y - BOARD_MARGIN_WIDTH
CORNER_ROUNDNESS                 = 15
BOARD_CORNER_ROUNDNESS           = 15
CORNER_SQUARE_WIDTH              = TILE_SIZE // CORNER_ROUNDNESS
CORNER_SQUARE_HEIGHT             = TILE_SIZE // CORNER_ROUNDNESS
CORNER_CIRLCE_RADIUS             = TILE_SIZE // CORNER_ROUNDNESS
BOARD_CORNER_SQUARE_WIDTH        = 2 * BOARD_MARGIN_WIDTH
BOARD_CORNER_SQUARE_HEIGHT       = 2 * BOARD_MARGIN_WIDTH
BOARD_CORNER_CIRLCE_RADIUS       = 2 * BOARD_MARGIN_WIDTH
TITLE_FONT_SIZE                  = 100
TEXT_FONT_SIZE                   = 40
CREDITS_FONT_SIZE                = 13
END_OF_GAME_FONT_SIZE            = 50
TITLE_CENTER_X                   = WINDOW_WIDTH_CENTER - TILE_SIZE - (TILE_SIZE // 2)
TITLE_CENTER_Y                   = BOARD_MARGIN_TOPLEFTCORNER_Y // 2
SCORE_TEXT_CENTER_X              = WINDOW_WIDTH_CENTER + (TILE_SIZE // 2)
SCORE_TEXT_CENTER_Y              = TITLE_CENTER_Y - (TEXT_FONT_SIZE // 2)
SCORE_VALUE_CENTER_X             = WINDOW_WIDTH_CENTER + (TILE_SIZE // 2)
SCORE_VALUE_CENTER_Y             = TITLE_CENTER_Y + (TEXT_FONT_SIZE // 2)
RECORD_TEXT_CENTER_X             = WINDOW_WIDTH_CENTER + 2 * TILE_SIZE + (TILE_SIZE // 4)
RECORD_TEXT_CENTER_Y             = TITLE_CENTER_Y - (TEXT_FONT_SIZE // 2)
RECORD_VALUE_CENTER_X            = WINDOW_WIDTH_CENTER + 2 * TILE_SIZE + (TILE_SIZE // 4)
RECORD_VALUE_CENTER_Y            = TITLE_CENTER_Y + (TEXT_FONT_SIZE // 2)
CREDITS_CENTER_X                 = BOARD_MARGIN_TOPLEFTCORNER_X + (BOARD_WIDTH * (TILE_SIZE + TILE_GAP)) + BOARD_MARGIN_WIDTH - (TILE_SIZE // 2)
CREDITS_CENTER_Y                 = BOARD_MARGIN_TOPLEFTCORNER_Y + (BOARD_WIDTH * (TILE_SIZE + TILE_GAP)) + (2 * BOARD_MARGIN_WIDTH) + (2 * TILE_GAP)

# WINDOW
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("2048")

# SOUNDS
mergeTilesSound1 = pygame.mixer.Sound("MergeTilesSound1.wav")
mergeTilesSound2 = pygame.mixer.Sound("MergeTilesSound2.wav")
mergeTilesSound3 = pygame.mixer.Sound("MergeTilesSound3.wav")
mergeTilesSounds = [mergeTilesSound1, mergeTilesSound2, mergeTilesSound2]
newRecordSound   = pygame.mixer.Sound("NewRecordSound.wav")
endOfGameSound   = pygame.mixer.Sound("EndOfGameSound.wav")
gameStartSound   = pygame.mixer.Sound("GameStartSound.wav")

try:
    assert(TILES_AT_BEGINNING <= BOARD_HEIGHT*BOARD_WIDTH)
except:
    print("ERROR: Number of tiles exceed board size.")
    sys.exit()  

def InitializeGame() -> ([[int]], [[int]], int):
    score = 0
    board    = [ [ 0 for j in range(BOARD_WIDTH) ] for i in range(BOARD_HEIGHT) ]

    for i in range(TILES_AT_BEGINNING):
        AddNewTile(board)

    # Keeps track of tiles merged in the turn
    boardAux = [ [ 0 for j in range(BOARD_WIDTH) ] for i in range(BOARD_HEIGHT) ]

    # Get game record
    if RecordFileExists():
        with open("record2048.txt", "r") as recordFile:
            record = int(recordFile.read())
    else:
        record = score

    gameStartSound.play()
    return board, boardAux, score, record

def GetNewTileValue() -> (int):
    value = random.choice(NEW_TILE_POSSIBLE_VALUES)
    return value

def GetValidCoordinates(board: [[int]]) -> (int, int):
    validCoordinates = False
    while not validCoordinates:
        row    = random.randint(0, BOARD_HEIGHT-1)
        column = random.randint(0, BOARD_WIDTH -1)
        if board[row][column] == 0:
            validCoordinates = True
    return row, column

def AddNewTile(board: [[int]]) -> ([[int]]):
    # Get new tile to add
    newTileRow, newTileColumn = GetValidCoordinates(board)
    newTileValue = GetNewTileValue()

    # Add new tile to board
    board[newTileRow][newTileColumn] = newTileValue

    return board

def CheckEmptyBox(board: [[int]], tileRow: int, tileColumn: int) -> (bool):
    if board[tileRow][tileColumn] == 0:
        emptyBox = True
    else:
        emptyBox = False

    return emptyBox

def MoveAllTilesUp(board:[[int]], boardAux: [[int]], score: int, tileMoved: bool) -> ([[int]], [[int]], int, bool):
    for i in range(BOARD_HEIGHT):
        for j in range(BOARD_WIDTH):
            tileRow, tileColumn = i, j
            tileCanMove = True
            while tileCanMove:
                if tileRow == 0 or board[tileRow][tileColumn] == 0:
                    tileCanMove = False
                else:
                    emptyBoxUp = CheckEmptyBox(board, tileRow-1, tileColumn)
                    if emptyBoxUp:
                        MoveTile(board, tileRow, tileColumn, UP)
                        tileRow = tileRow - 1
                        tileMoved = True
                    elif not emptyBoxUp:
                        tileCanMove = False
                        if TilesAreEqual(board, tileRow, tileColumn, tileRow-1, tileColumn) and not MergedTile(boardAux, tileRow-1, tileColumn):
                            MergeTiles(board, tileRow, tileColumn, UP)
                            MarkTileAsMerged(boardAux, tileRow-1, tileColumn)
                            score = score + board[tileRow-1][tileColumn]
                            tileMoved = True
    CleanAuxBoard(boardAux)
    return score, tileMoved

def MoveAllTilesDown(board:[[int]], boardAux: [[int]], score: int, tileMoved: bool) -> ([[int]], [[int]], int, bool):
    for i in reversed(range(BOARD_HEIGHT)):
        for j in range(BOARD_WIDTH):
            tileRow, tileColumn = i, j
            tileCanMove = True
            while tileCanMove:
                if tileRow == BOARD_HEIGHT-1 or board[tileRow][tileColumn] == 0:
                    tileCanMove = False
                else:
                    emptyBoxDown = CheckEmptyBox(board, tileRow+1, tileColumn)
                    if emptyBoxDown:
                        MoveTile(board, tileRow, tileColumn, DOWN)
                        tileRow = tileRow + 1
                        tileMoved = True
                    elif not emptyBoxDown:
                        tileCanMove = False
                        if TilesAreEqual(board, tileRow, tileColumn, tileRow+1, tileColumn) and not MergedTile(boardAux, tileRow+1, tileColumn):
                            MergeTiles(board, tileRow, tileColumn, DOWN)
                            MarkTileAsMerged(boardAux, tileRow+1, tileColumn)
                            score = score + board[tileRow+1][tileColumn]
                            tileMoved = True
    CleanAuxBoard(boardAux)
    return score, tileMoved

def MoveAllTilesLeft(board:[[int]], boardAux: [[int]], score: int, tileMoved: bool) -> ([[int]], [[int]], int, bool):
    for j in range(BOARD_WIDTH):
        for i in range(BOARD_HEIGHT):
            tileRow, tileColumn = i, j
            tileCanMove = True
            while tileCanMove:
                if tileColumn == 0 or board[tileRow][tileColumn] == 0:
                    tileCanMove = False
                else:
                    emptyBoxLeft = CheckEmptyBox(board, tileRow, tileColumn-1)
                    if emptyBoxLeft:
                        MoveTile(board, tileRow, tileColumn, LEFT)
                        tileColumn = tileColumn - 1
                        tileMoved = True
                    elif not emptyBoxLeft:
                        tileCanMove = False
                        if TilesAreEqual(board, tileRow, tileColumn, tileRow, tileColumn-1) and not MergedTile(boardAux, tileRow, tileColumn-1):
                            MergeTiles(board, tileRow, tileColumn, LEFT)
                            MarkTileAsMerged(boardAux, tileRow, tileColumn-1)
                            score = score + board[tileRow][tileColumn-1]
                            tileMoved = True
    CleanAuxBoard(boardAux)
    return score, tileMoved

def MoveAllTilesRight(board:[[int]], boardAux: [[int]], score: int, tileMoved: bool) -> ([[int]], [[int]], int, bool):
    for j in reversed(range(BOARD_WIDTH)):
        for i in range(BOARD_HEIGHT):
            tileRow, tileColumn = i, j
            tileCanMove = True
            while tileCanMove:
                if tileColumn == BOARD_WIDTH-1 or board[tileRow][tileColumn] == 0:
                    tileCanMove = False
                else:
                    emptyBoxRight = CheckEmptyBox(board, tileRow, tileColumn+1)
                    if emptyBoxRight:
                        MoveTile(board, tileRow, tileColumn, RIGHT)
                        tileColumn = tileColumn + 1
                        tileMoved = True
                    elif not emptyBoxRight:
                        tileCanMove = False
                        if TilesAreEqual(board, tileRow, tileColumn, tileRow, tileColumn+1) and not MergedTile(boardAux, tileRow, tileColumn+1):
                            MergeTiles(board, tileRow, tileColumn, RIGHT)
                            MarkTileAsMerged(boardAux, tileRow, tileColumn+1)
                            score = score + board[tileRow][tileColumn+1]
                            tileMoved = True
    CleanAuxBoard(boardAux)
    return score, tileMoved

def MoveTile(board: [[int]], tileRow: int, tileColumn: int, direction: str) -> ([[int]]):
    if   direction == UP:
        board[tileRow-1][tileColumn] = board[tileRow][tileColumn]

    elif direction == DOWN:
        board[tileRow+1][tileColumn] = board[tileRow][tileColumn]

    elif direction == RIGHT:
        board[tileRow][tileColumn+1] = board[tileRow][tileColumn]

    elif direction == LEFT:
        board[tileRow][tileColumn-1] = board[tileRow][tileColumn]

    board[tileRow][tileColumn] = 0

def TilesAreEqual(board: [[int]], tile1Row: int, tile1Column: int, tile2Row: int, tile2Column: int) -> (bool):
    if board[tile1Row][tile1Column] == board[tile2Row][tile2Column]:
        areEqual = True
    else:
        areEqual = False

    return areEqual

def MergeTiles(board: [[int]], tileRow: int, tileColumn: int, direction: str) -> ([[int]]):
    if   direction == UP:
        board[tileRow-1][tileColumn] += board[tileRow][tileColumn]

    elif direction == DOWN:
        board[tileRow+1][tileColumn] += board[tileRow][tileColumn]

    elif direction == RIGHT:
        board[tileRow][tileColumn+1] += board[tileRow][tileColumn]

    elif direction == LEFT:
        board[tileRow][tileColumn-1] += board[tileRow][tileColumn]

    board[tileRow][tileColumn] = 0
    PlayMergeTilesSound()

def MarkTileAsMerged(boardAux: [[int]], tileRow: int, tileColumn: int) -> ([[int]]):
    boardAux[tileRow][tileColumn] = 1
    return boardAux

def MergedTile(boardAux: [[int]], tileRow: int, tileColumn: int) -> (bool):
    if boardAux[tileRow][tileColumn] == 1:
        return True
    else:
        return False

def CleanAuxBoard(boardAux: [[int]]) -> ([[int]]):
    for i in range(BOARD_HEIGHT):
        for j in range(BOARD_WIDTH):
            boardAux[i][j] = 0

def EndOfGame(board: [[int]]) -> (bool):
    quantityEmptyBoxes = CountEmptyBoxes(board)
    if quantityEmptyBoxes == 0:
        return True
    else:
        return False

def CountEmptyBoxes(board: [[int]]) -> (int):
    count = 0
    for i in range(BOARD_HEIGHT):
        for j in range(BOARD_WIDTH):
            if board[i][j] == 0:
                count += 1
    return count

def DisplayGameOnCOnsole(board: [[int]], score: int) -> ("void"):
    print("SCORE =" , score)
    print("------------")   
    for i in range(BOARD_HEIGHT):
        print(board[i])
    print("===============")

def UpdateGame(board: [[int]], boardAux: [[int]], score: int, tileMoved: bool) -> ("void"):
    if tileMoved:
        AddNewTile(board)
    DisplayGameOnCOnsole(board, score)

def CheckGameRecord(score: int, record: int, newRecord: bool) -> ("void"):
    if newRecord:
        with open("record2048.txt", "w") as recordFile:
            recordFile.write(str(score))
        print("NEW RECORD!!")

    else:
        print("SCORE  = " + str(score))
        print("RECORD = " + str(record))

def RecordFileExists() -> (bool):
    return os.path.exists("record2048.txt")

def CompareScoreAndRecord(score: int, record: int, newRecord: bool) -> (int, bool):
    if score > record or newRecord:
        record = score
        newRecord = True
    else:
        newRecord = False

    return record, newRecord

def TileColor(board: [[int]], tileRow:int, tileColumn: int) -> (str):
    if   board[tileRow][tileColumn] == 0:
        color = EMPTYBOX_COLOR
    elif board[tileRow][tileColumn] == 2:
        color = GREEN2
    elif board[tileRow][tileColumn] == 4:
        color = BLUE4
    elif board[tileRow][tileColumn] == 8:
        color = BLUE8
    elif board[tileRow][tileColumn] == 16:
        color = BLUE16
    elif board[tileRow][tileColumn] == 32:
        color = BLUE32
    elif board[tileRow][tileColumn] == 64:
        color = BLUE64
    elif board[tileRow][tileColumn] == 128:
        color = BLUE128
    elif board[tileRow][tileColumn] == 256:
        color = BLUE256
    elif board[tileRow][tileColumn] == 512:
        color = BLUE512
    elif board[tileRow][tileColumn] == 1024:
        color = BLUE1024
    elif board[tileRow][tileColumn] == 2048:
        color = BLUE2048
    return color

def PlayMergeTilesSound() -> ("void"):
    mergeTilesSound = random.choice(mergeTilesSounds)
    mergeTilesSound.play()

def DisplayScore(newRecord: bool, score: int, record: int) -> ("void"):
    if newRecord:
        newRecordSound.play()
        while True:
            DisplayNewRecord(score)     
            CloseGame()
    else:
        endOfGameSound.play()
        while True:
            DisplayEndOfGame(score, record)
            CloseGame()

def CloseGame() -> ("void"):
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

##################
#### GRAPHICS ####
##################

def DrawBoard(board: [[int]], score: int, record: int) -> ("void"):
    
    WINDOW.fill(BACKGROUNDCOLOR)
    
    titleFont              = pygame.font.Font("freesansbold.ttf", TITLE_FONT_SIZE  )
    textFont               = pygame.font.Font("freesansbold.ttf", TEXT_FONT_SIZE   )
    creditsFont            = pygame.font.Font("freesansbold.ttf", CREDITS_FONT_SIZE)

    surfaceTitle           = titleFont.render("2048"            , True, GRAY)
    surfaceScore           = textFont.render("SCORE"            , True, GRAY)
    surfaceRecord          = textFont.render("RECORD"           , True, GRAY)
    surfaceScoreValue      = textFont.render(str(score)         , True, GRAY)
    surfaceRecordValue     = textFont.render(str(record)        , True, GRAY)
    surfaceCredits         = creditsFont.render("© Jose Acevedo", True, GRAY)

    titleText              = surfaceTitle.get_rect()
    scoreText              = surfaceScore.get_rect()
    scoreValueText         = surfaceScoreValue.get_rect()
    recordText             = surfaceRecord.get_rect()
    recordValueText        = surfaceRecordValue.get_rect()
    creditsText            = surfaceCredits.get_rect()

    titleText.center       = (TITLE_CENTER_X       , TITLE_CENTER_Y       )
    scoreText.center       = (SCORE_TEXT_CENTER_X  , SCORE_TEXT_CENTER_Y  )
    scoreValueText.center  = (SCORE_VALUE_CENTER_X , SCORE_VALUE_CENTER_Y )
    recordText.center      = (RECORD_TEXT_CENTER_X , RECORD_TEXT_CENTER_Y ) 
    recordValueText.center = (RECORD_VALUE_CENTER_X, RECORD_VALUE_CENTER_Y)
    creditsText.center     = (CREDITS_CENTER_X     , CREDITS_CENTER_Y     )

    WINDOW.blit(surfaceTitle      , titleText      )
    WINDOW.blit(surfaceScore      , scoreText      )
    WINDOW.blit(surfaceScoreValue , scoreValueText )
    WINDOW.blit(surfaceRecord     , recordText     )
    WINDOW.blit(surfaceRecordValue, recordValueText)
    WINDOW.blit(surfaceCredits    , creditsText    )

    tile_TopLeft_Corner_Y     = BOARD_TOPLEFT_CORNER_Y
    tile_TopRight_Corner_Y    = BOARD_TOPLEFT_CORNER_Y
    tile_BottomLeft_Corner_Y  = BOARD_TOPLEFT_CORNER_Y + TILE_SIZE - CORNER_SQUARE_HEIGHT
    tile_BottomRight_Corner_Y = BOARD_TOPLEFT_CORNER_Y + TILE_SIZE - CORNER_SQUARE_HEIGHT
    
    board_TopLeft_Corner_Y     = BOARD_MARGIN_TOPLEFTCORNER_Y
    board_TopRight_Corner_Y    = BOARD_MARGIN_TOPLEFTCORNER_Y
    board_BottomLeft_Corner_Y  = BOARD_MARGIN_TOPLEFTCORNER_Y + (BOARD_HEIGHT * (TILE_SIZE + TILE_GAP))
    board_BottomRight_Corner_Y = BOARD_MARGIN_TOPLEFTCORNER_Y + (BOARD_HEIGHT * (TILE_SIZE + TILE_GAP))
    board_TopLeft_Corner_X     = BOARD_MARGIN_TOPLEFTCORNER_X
    board_TopRight_Corner_X    = BOARD_MARGIN_TOPLEFTCORNER_X + (BOARD_WIDTH  * (TILE_SIZE + TILE_GAP))
    board_BottomLeft_Corner_X  = BOARD_MARGIN_TOPLEFTCORNER_X
    board_BottomRight_Corner_X = BOARD_MARGIN_TOPLEFTCORNER_X + (BOARD_WIDTH  * (TILE_SIZE + TILE_GAP))
    
    pygame.draw.rect(WINDOW, BOARD_BACKGROUND_COLOR, (BOARD_MARGIN_TOPLEFTCORNER_X, BOARD_MARGIN_TOPLEFTCORNER_Y,
                     BOARD_WIDTH*(TILE_SIZE+TILE_GAP) + 2*BOARD_MARGIN_WIDTH, BOARD_HEIGHT*(TILE_SIZE+TILE_GAP) + 2*BOARD_MARGIN_WIDTH))
    pygame.draw.rect(WINDOW, BACKGROUNDCOLOR, (board_TopLeft_Corner_X    , board_TopLeft_Corner_Y    , BOARD_CORNER_SQUARE_WIDTH, BOARD_CORNER_SQUARE_HEIGHT))
    pygame.draw.rect(WINDOW, BACKGROUNDCOLOR, (board_TopRight_Corner_X   , board_TopRight_Corner_Y   , BOARD_CORNER_SQUARE_WIDTH, BOARD_CORNER_SQUARE_HEIGHT))
    pygame.draw.rect(WINDOW, BACKGROUNDCOLOR, (board_BottomLeft_Corner_X , board_BottomLeft_Corner_Y , BOARD_CORNER_SQUARE_WIDTH, BOARD_CORNER_SQUARE_HEIGHT))
    pygame.draw.rect(WINDOW, BACKGROUNDCOLOR, (board_BottomRight_Corner_X, board_BottomRight_Corner_Y, BOARD_CORNER_SQUARE_WIDTH, BOARD_CORNER_SQUARE_HEIGHT))
    pygame.draw.circle(WINDOW, BOARD_BACKGROUND_COLOR, (board_TopLeft_Corner_X + BOARD_CORNER_CIRLCE_RADIUS, board_TopLeft_Corner_Y + BOARD_CORNER_CIRLCE_RADIUS), BOARD_CORNER_CIRLCE_RADIUS)
    pygame.draw.circle(WINDOW, BOARD_BACKGROUND_COLOR, (board_TopRight_Corner_X, board_TopRight_Corner_Y + BOARD_CORNER_CIRLCE_RADIUS), BOARD_CORNER_CIRLCE_RADIUS)
    pygame.draw.circle(WINDOW, BOARD_BACKGROUND_COLOR, (board_BottomLeft_Corner_X + BOARD_CORNER_CIRLCE_RADIUS, board_BottomLeft_Corner_Y), BOARD_CORNER_CIRLCE_RADIUS)
    pygame.draw.circle(WINDOW, BOARD_BACKGROUND_COLOR, (board_BottomRight_Corner_X, board_BottomRight_Corner_Y), BOARD_CORNER_CIRLCE_RADIUS)

    for i in range(BOARD_HEIGHT):
        tile_TopLeft_Corner_X     = BOARD_TOPLEFT_CORNER_X
        tile_TopRight_Corner_X    = BOARD_TOPLEFT_CORNER_X + TILE_SIZE - CORNER_SQUARE_WIDTH
        tile_BottomLeft_Corner_X  = BOARD_TOPLEFT_CORNER_X
        tile_BottomRight_Corner_X = BOARD_TOPLEFT_CORNER_X + TILE_SIZE - CORNER_SQUARE_WIDTH

        for j in range(BOARD_WIDTH):
            color = TileColor(board, i, j)
            pygame.draw.rect(WINDOW, color, (tile_TopLeft_Corner_X, tile_TopLeft_Corner_Y, TILE_SIZE, TILE_SIZE))

            if board[i][j] != 0:
                if board[i][j] <= 8:
                    surfaceTileValue = textFont.render(str(board[i][j]), True, GRAY)
                else:
                    surfaceTileValue = textFont.render(str(board[i][j]), True, WHITE)
                tileValue = surfaceTileValue.get_rect()
                tileValue.center = (tile_TopLeft_Corner_X + (TILE_SIZE // 2), tile_TopLeft_Corner_Y + (TILE_SIZE // 2))
                WINDOW.blit(surfaceTileValue, tileValue)            
            
            # Draw rounded corners
            pygame.draw.rect(WINDOW, BOARD_BACKGROUND_COLOR, (tile_TopLeft_Corner_X    , tile_TopLeft_Corner_Y    , CORNER_SQUARE_WIDTH, CORNER_SQUARE_HEIGHT))
            pygame.draw.rect(WINDOW, BOARD_BACKGROUND_COLOR, (tile_TopRight_Corner_X   , tile_TopRight_Corner_Y   , CORNER_SQUARE_WIDTH, CORNER_SQUARE_HEIGHT))
            pygame.draw.rect(WINDOW, BOARD_BACKGROUND_COLOR, (tile_BottomLeft_Corner_X , tile_BottomLeft_Corner_Y , CORNER_SQUARE_WIDTH, CORNER_SQUARE_HEIGHT))
            pygame.draw.rect(WINDOW, BOARD_BACKGROUND_COLOR, (tile_BottomRight_Corner_X, tile_BottomRight_Corner_Y, CORNER_SQUARE_WIDTH, CORNER_SQUARE_HEIGHT))
            pygame.draw.circle(WINDOW, color, (tile_TopLeft_Corner_X + CORNER_CIRLCE_RADIUS, tile_TopLeft_Corner_Y + CORNER_CIRLCE_RADIUS), CORNER_CIRLCE_RADIUS)
            pygame.draw.circle(WINDOW, color, (tile_TopRight_Corner_X, tile_TopRight_Corner_Y + CORNER_CIRLCE_RADIUS), CORNER_CIRLCE_RADIUS)
            pygame.draw.circle(WINDOW, color, (tile_BottomLeft_Corner_X + CORNER_CIRLCE_RADIUS, tile_BottomLeft_Corner_Y), CORNER_CIRLCE_RADIUS)
            pygame.draw.circle(WINDOW, color, (tile_BottomRight_Corner_X, tile_BottomRight_Corner_Y), CORNER_CIRLCE_RADIUS)

            tile_TopLeft_Corner_X     += TILE_SIZE + TILE_GAP
            tile_TopRight_Corner_X    += TILE_SIZE + TILE_GAP
            tile_BottomLeft_Corner_X  += TILE_SIZE + TILE_GAP
            tile_BottomRight_Corner_X += TILE_SIZE + TILE_GAP

        tile_TopLeft_Corner_Y     += TILE_SIZE + TILE_GAP
        tile_TopRight_Corner_Y    += TILE_SIZE + TILE_GAP
        tile_BottomLeft_Corner_Y  += TILE_SIZE + TILE_GAP
        tile_BottomRight_Corner_Y += TILE_SIZE + TILE_GAP

    pygame.display.update()

def DisplayNewRecord(score: int) -> ("void"):

    pygame.draw.rect(WINDOW, END_OF_GAME_BOX_BACKGROUND_COLOR, (BOARD_MARGIN_TOPLEFTCORNER_X+BOARD_MARGIN_WIDTH,
                                                                BOARD_MARGIN_TOPLEFTCORNER_Y+BOARD_MARGIN_WIDTH,
                                                                BOARD_WIDTH*(TILE_SIZE+TILE_GAP)  + 2*BOARD_MARGIN_WIDTH - 2*BOARD_MARGIN_WIDTH,
                                                                BOARD_HEIGHT*(TILE_SIZE+TILE_GAP) + 2*BOARD_MARGIN_WIDTH - 2*BOARD_MARGIN_WIDTH))

    newRecordFont         = pygame.font.Font("freesansbold.ttf", END_OF_GAME_FONT_SIZE)
    textFont              = pygame.font.Font("freesansbold.ttf", TEXT_FONT_SIZE       )

    surfaceEndOfGame      = textFont.render("END OF GAME"    , True, GRAY)
    surfaceScoreValue     = newRecordFont.render(str(score)  , True, GRAY)
    surfaceNewRecord      = newRecordFont.render("NEW RECORD", True, GRAY)

    endOfGameText         = surfaceEndOfGame.get_rect()
    scoreValueText        = surfaceScoreValue.get_rect()
    newRecordText         = surfaceNewRecord.get_rect()

    endOfGameText.center  = (WINDOW_WIDTH_CENTER, WINDOW_HEIGHT_CENTER - (BOARD_HEIGHT * (TILE_SIZE+TILE_GAP) // 4))
    scoreValueText.center = (WINDOW_WIDTH_CENTER, WINDOW_HEIGHT_CENTER + (BOARD_HEIGHT * (TILE_SIZE+TILE_GAP) // 4))
    newRecordText.center  = (WINDOW_WIDTH_CENTER, WINDOW_HEIGHT_CENTER)

    WINDOW.blit(surfaceEndOfGame , endOfGameText )
    WINDOW.blit(surfaceScoreValue, scoreValueText)
    WINDOW.blit(surfaceNewRecord , newRecordText )

    pygame.display.update()

def DisplayEndOfGame(score: int, record: int) -> ("void"):

    pygame.draw.rect(WINDOW, END_OF_GAME_BOX_BACKGROUND_COLOR, (BOARD_MARGIN_TOPLEFTCORNER_X+BOARD_MARGIN_WIDTH,
                                                                BOARD_MARGIN_TOPLEFTCORNER_Y+BOARD_MARGIN_WIDTH,
                                                                BOARD_WIDTH*(TILE_SIZE+TILE_GAP)  + 2*BOARD_MARGIN_WIDTH - 2*BOARD_MARGIN_WIDTH,
                                                                BOARD_HEIGHT*(TILE_SIZE+TILE_GAP) + 2*BOARD_MARGIN_WIDTH - 2*BOARD_MARGIN_WIDTH))
   
    textFont               = pygame.font.Font("freesansbold.ttf", TEXT_FONT_SIZE       )
    endOfGameFont          = pygame.font.Font("freesansbold.ttf", END_OF_GAME_FONT_SIZE)

    surfaceEndOfGame       = textFont.render("END OF GAME", True, GRAY)
    surfaceScore           = textFont.render("SCORE"      , True, GRAY)
    surfaceRecord          = textFont.render("RECORD"     , True, GRAY)
    surfaceScoreValue      = textFont.render(str(score)   , True, GRAY)
    surfaceRecordValue     = textFont.render(str(record)  , True, GRAY)
    
    endOfGameText          = surfaceEndOfGame.get_rect()
    scoreText              = surfaceScore.get_rect()
    scoreValueText         = surfaceScoreValue.get_rect()
    recordText             = surfaceRecord.get_rect()
    recordValueText        = surfaceRecordValue.get_rect()

    endOfGameText.center   = (WINDOW_WIDTH_CENTER, WINDOW_HEIGHT_CENTER - (BOARD_HEIGHT * (TILE_SIZE+TILE_GAP) // 4))
    scoreText.center       = (WINDOW_WIDTH_CENTER - (BOARD_WIDTH*(TILE_SIZE+TILE_GAP)//4), WINDOW_HEIGHT_CENTER)
    scoreValueText.center  = (WINDOW_WIDTH_CENTER - (BOARD_WIDTH*(TILE_SIZE+TILE_GAP)//4), WINDOW_HEIGHT_CENTER + BOARD_HEIGHT*(TILE_SIZE+TILE_GAP)//8)
    recordText.center      = (WINDOW_WIDTH_CENTER + (BOARD_WIDTH*(TILE_SIZE+TILE_GAP)//4), WINDOW_HEIGHT_CENTER) 
    recordValueText.center = (WINDOW_WIDTH_CENTER + (BOARD_WIDTH*(TILE_SIZE+TILE_GAP)//4), WINDOW_HEIGHT_CENTER + BOARD_HEIGHT*(TILE_SIZE+TILE_GAP)//8)

    WINDOW.blit(surfaceEndOfGame  , endOfGameText  )
    WINDOW.blit(surfaceScore      , scoreText      )
    WINDOW.blit(surfaceScoreValue , scoreValueText )
    WINDOW.blit(surfaceRecord     , recordText     )
    WINDOW.blit(surfaceRecordValue, recordValueText)

    pygame.display.update()

################
##### GAME #####
################

gameBoard, gameBoardAux, playerScore, gameRecord = InitializeGame()
DisplayGameOnCOnsole(gameBoard, playerScore)
newGameRecord = False
# MAIN GAME LOOP
while not EndOfGame(gameBoard):

    tilesMoved = False
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_UP:
            playerScore, tilesMoved = MoveAllTilesUp(gameBoard, gameBoardAux, playerScore, tilesMoved)
            UpdateGame(gameBoard, gameBoardAux, playerScore, tilesMoved)
        elif event.type == KEYDOWN and event.key == K_DOWN:
            playerScore, tilesMoved = MoveAllTilesDown(gameBoard, gameBoardAux, playerScore, tilesMoved)
            UpdateGame(gameBoard, gameBoardAux, playerScore, tilesMoved)
        elif event.type == KEYDOWN and event.key == K_RIGHT:
            playerScore, tilesMoved = MoveAllTilesRight(gameBoard, gameBoardAux, playerScore, tilesMoved)
            UpdateGame(gameBoard, gameBoardAux, playerScore, tilesMoved)
        elif event.type == KEYDOWN and event.key == K_LEFT:
            playerScore, tilesMoved = MoveAllTilesLeft(gameBoard, gameBoardAux, playerScore, tilesMoved)
            UpdateGame(gameBoard, gameBoardAux, playerScore, tilesMoved)
    gameRecord, newGameRecord = CompareScoreAndRecord(playerScore, gameRecord, newGameRecord)
    DrawBoard(gameBoard, playerScore, gameRecord)

CheckGameRecord(playerScore, gameRecord, newGameRecord)
DisplayScore(newGameRecord, playerScore, gameRecord)