# Squirrels
#
# By Jose Acevedo
#
# © Copyright 2015.

import pygame
import random
import math
import sys
import time
from pygame.locals import *

# COLORS        R    G    B
WHITE       = (255, 255, 255)
BLACK       = (0  , 0  , 0  )
GREEN       = (0  , 85 , 0  )
BRIGHTGREEN = (0  , 130, 0  )
RED         = (255, 0  , 0  )

# GAME SETTINGS
MOVE_RATE                  = 9
BOUNCE_RATE                = 15
BOUNCE_HEIGHT              = 70
GRASS_SIZE                 = 50
SQUIRREL_START_SIZE        = 75
MAX_HEALTH                 = 3
SQUIRREL_MIN_SPEED         = 1
SQUIRREL_MAX_SPEED         = 11
AMOUNT_OF_GRASS            = 150
BOUNCE_RATE_MAX            = 18
BOUNCE_RATE_MIN            = 10
BOUNCE_HEIGHT_MAX          = 50
BOUNCE_HEIGHT_MIN          = 10
GRASS_AT_START             = 10
SQUIRRELS_AT_START         = 10
CHANGE_DIRECTION_FREQ      = 2
INVULNERABLE_MODE_DURATION = 2

# DISPLAY SETTINGS
FPS                    = 30
GAME_CENTER            = 0
WINDOW_WIDTH           = 1600
WINDOW_HEIGHT          = 1000
CAMERASLACK            = 100
HEALTHBAR_TOPLEFT_X    = 10
HEALTHBAR_TOPLEFT_Y    = 10
HEALTHBOX_WIDTH        = 50
HEALTHBOX_HEIGHT       = 30
SAFEHOUSE_SIZE         = 250
TITLE_WIDTH            = 500
TITLE_HEIGHT           = 100
WINDOW_WIDTH_HALF      = WINDOW_WIDTH  // 2
WINDOW_HEIGHT_HALF     = WINDOW_HEIGHT // 2
BACKGROUND_COLOR       = GREEN
PLAYER_SIZE_TEXT_COLOR = WHITE

# TEXT SETTINGS
CAPTION_TEXT    = "Squirrels"
BASICFONT_STYLE = "freesansbold.ttf"
BASICFONT_SIZE  = 15
LEFT            = "left"
RIGHT           = "right"
UP              = "up"
DOWN            = "down"

def main():
    gameSetup()
    while True:
        startScreen()
        runGame()

def runGame():
    playerSquirrel, grassObjs, amountOfGrass, squirrelObjs,         \
    amountOfSquirrels, camerax, cameray, moveUp, moveDown,          \
    moveRight, moveLeft, neededAmountOfSquirrels, invulnerableMode, \
    invulnerableModeLastTime, safeHouse, lost = initializeGame()
    # Main game loop
    while True:

        # 1: Handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    moveDown = False
                    moveUp   = True
                elif event.key == K_DOWN:
                    moveUp   = False
                    moveDown = True
                elif event.key == K_RIGHT:
                    moveLeft  = False
                    moveRight = True
                elif event.key == K_LEFT:
                    moveRight = False
                    moveLeft  = True

            elif event.type == KEYUP:
                if event.key == K_UP:
                    moveUp = False
                elif event.key == K_DOWN:
                    moveDown = False
                elif event.key == K_RIGHT:
                    moveRight = False
                elif event.key == K_LEFT:
                    moveLeft = False
                elif event.key == K_SPACE:
                    pauseGame()
                elif event.key == K_ESCAPE:
                    terminate()
                elif event.key == K_r:
                    return

        # 2: Update game status
        movePlayer(playerSquirrel, moveUp, moveDown, moveRight, moveLeft, camerax, cameray)
        moveSquirrels(squirrelObjs, camerax, cameray)
        camerax, cameray        = moveCamera(camerax, cameray, playerSquirrel["x"], playerSquirrel["y"])
        amountOfSquirrels       = eliminateFarAwayObjects(squirrelObjs, amountOfSquirrels, camerax, cameray)
        amountOfGrass           = eliminateFarAwayObjects(grassObjs   , amountOfGrass    , camerax, cameray)
        safeHouse               = eliminateFarAwaySafeHouse(safeHouse , camerax          , cameray)
        amountOfSquirrels       = createEnoughSquirrels(playerSquirrel, squirrelObjs, amountOfSquirrels, camerax, cameray, neededAmountOfSquirrels)
        amountOfGrass           = createEnoughGrass(grassObjs   , amountOfGrass, camerax, cameray)
        if not invulnerableMode:
            amountOfSquirrels, lostLife, invulnerableModeLastTime = checkCollisions(playerSquirrel, squirrelObjs,
                                                                    amountOfSquirrels, invulnerableModeLastTime)
        neededAmountOfSquirrels = checkAMountOfSquirrelsNeeded(playerSquirrel, neededAmountOfSquirrels)
        insideSafeHouse         = checkPlayerInsideSafeHouse(safeHouse, playerSquirrel)
        invulnerableMode        = checkInvulnerableMode(lostLife, invulnerableModeLastTime, insideSafeHouse)
        lost                    = checkHealth(playerSquirrel["health"])
        restart                 = checkGameOver(playerSquirrel, grassObjs, amountOfGrass, invulnerableMode,
                                                invulnerableModeLastTime, squirrelObjs, amountOfSquirrels,
                                                camerax, cameray , safeHouse, lost)
        if restart:
            return

        # 3: display game
        displayGame(playerSquirrel, grassObjs, amountOfGrass, invulnerableMode, invulnerableModeLastTime,
        squirrelObjs, amountOfSquirrels, camerax, cameray , safeHouse, lost)

def loadImages():
    global GAME_ICON, LEFT_SQUIRREL_IMAGE, RIGHT_SQUIRREL_IMAGE, \
           GRASS_IMAGES, SAFEHOUSE_IMAGE, EXPLOSION_IMAGE, GAMEOVER_IMAGE, TITLE_IMAGE
    GAME_ICON            = pygame.image.load("SquirrelsImages/gameicon.png")
    TITLE_IMAGE          = pygame.image.load("SquirrelsImages/title.png")
    TITLE_IMAGE          = pygame.transform.scale(TITLE_IMAGE, (TITLE_WIDTH, TITLE_HEIGHT))
    EXPLOSION_IMAGE      = pygame.image.load("SquirrelsImages/explosion.png")
    SAFEHOUSE_IMAGE      = pygame.image.load("SquirrelsImages/safeHouse.png")
    SAFEHOUSE_IMAGE      = pygame.transform.scale(SAFEHOUSE_IMAGE, (SAFEHOUSE_SIZE, SAFEHOUSE_SIZE))
    LEFT_SQUIRREL_IMAGE  = pygame.image.load("SquirrelsImages/squirrel.png")
    RIGHT_SQUIRREL_IMAGE = pygame.transform.flip(LEFT_SQUIRREL_IMAGE, True, False)
    GAMEOVER_IMAGE       = pygame.image.load("SquirrelsImages/gameover.png")
    GRASS_IMAGES = []
    for i in range(1, 5):
        GRASS_IMAGES.append(pygame.image.load("SquirrelsImages/grass%s.png" % i))

def windowSetUp():
    global DISPLAYSURF
    DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption(CAPTION_TEXT)
    pygame.display.set_icon(GAME_ICON)

def textSetUp():
    global BASICFONT
    BASICFONT = pygame.font.Font(BASICFONT_STYLE, BASICFONT_SIZE)

def soundSetUp():
    global BOUNCE_SOUND, BITE_SOUND, EXPLOSION_SOUND, PUNCH_SOUND
    BOUNCE_SOUND    = pygame.mixer.Sound("SquirrelsSounds/bounce.wav")
    BITE_SOUND      = pygame.mixer.Sound("SquirrelsSounds/bite.wav")
    EXPLOSION_SOUND = pygame.mixer.Sound("SquirrelsSounds/explosion.wav")
    PUNCH_SOUND     = pygame.mixer.Sound("SquirrelsSounds/punch.wav")
    pygame.mixer.music.load("SquirrelsSounds/theme.mp3")

def initializeGame():
    camerax                  = GAME_CENTER - WINDOW_WIDTH_HALF
    cameray                  = GAME_CENTER - WINDOW_HEIGHT_HALF
    moveUp                   = False
    moveDown                 = False
    moveRight                = False
    moveLeft                 = False
    lost                     = False
    invulnerableMode         = False
    invulnerableModeLastTime = 0
    neededAmountOfSquirrels  = 80
    grassObjs                = []
    squirrelObjs             = []
    safeHouse                = makeNewSafeHouse(camerax, cameray)
    amountOfGrass            = GRASS_AT_START
    amountOfSquirrels        = SQUIRRELS_AT_START
    playerSquirrel           = { "image" : pygame.transform.scale(LEFT_SQUIRREL_IMAGE, (SQUIRREL_START_SIZE, SQUIRREL_START_SIZE)),
                                 "width" : SQUIRREL_START_SIZE,
                                 "height": SQUIRREL_START_SIZE,
                                 "health": MAX_HEALTH,
                                 "bounce": 0,
                                 "facing": LEFT,
                                 "x": GAME_CENTER - (SQUIRREL_START_SIZE // 2),
                                 "y": GAME_CENTER - (SQUIRREL_START_SIZE // 2)}
    playerSquirrel["rect"] = playerSquirrel["image"].get_rect()
    playerSquirrel["rect"].topleft = (playerSquirrel["x"] - camerax, playerSquirrel["y"] - cameray -
                                      getBounceAmount(playerSquirrel["bounce"], BOUNCE_HEIGHT, BOUNCE_RATE))

    # Amount of grass at start of game
    for i in range(GRASS_AT_START):
        grassObjs.append(makeNewGrass(camerax, cameray))
        # Overwrite cooordinates to appear on the screen
        grassObjs[i]["x"] = random.randint(camerax, camerax + WINDOW_WIDTH )
        grassObjs[i]["y"] = random.randint(cameray, cameray + WINDOW_HEIGHT)

    # Amount of squirrels at start of game
    for i in range(SQUIRRELS_AT_START):
        squirrelObjs.append(makeNewSquirrel(camerax, cameray, playerSquirrel))      
        squirrelObjs[i]["x"] = random.randint(camerax, camerax + WINDOW_WIDTH )
        squirrelObjs[i]["y"] = random.randint(cameray, cameray + WINDOW_HEIGHT)

    return playerSquirrel, grassObjs, amountOfGrass, squirrelObjs,         \
           amountOfSquirrels, camerax, cameray, moveUp, moveDown,          \
           moveRight, moveLeft, neededAmountOfSquirrels, invulnerableMode, \
           invulnerableModeLastTime, safeHouse, lost

def makeNewSquirrel(camerax: int, cameray: int, playerSquirrel: {}):
    squirrel  = {}
    minWidth  = playerSquirrel["width"] // 2
    maxWidth  = (playerSquirrel["width"]  * 3) // 2
    minHeight = playerSquirrel["height"] // 2
    maxHeight = (playerSquirrel["height"] * 3) // 2
    squirrel["bounce"]           = 0    
    squirrel["width"]            = random.randint(minWidth, maxWidth)
    squirrel["height"]           = random.randint(minHeight, maxHeight)
    squirrel["bounceRate"]       = random.randint(BOUNCE_RATE_MIN  , BOUNCE_RATE_MAX  )
    squirrel["bounceHeight"]     = random.randint(BOUNCE_HEIGHT_MIN, BOUNCE_HEIGHT_MAX)
    squirrel["movex"]            = getRandomVelocity()
    squirrel["movey"]            = getRandomVelocity()
    squirrel["x"], squirrel["y"] = getRandomOffCameraPosition(camerax, cameray,
                                   squirrel["width"], squirrel["height"])
    
    if squirrel["movex"] > 0:
        squirrel["image"] = pygame.transform.scale(RIGHT_SQUIRREL_IMAGE,
                            (squirrel["width"], squirrel["height"]))
    else:
        squirrel["image"] = pygame.transform.scale(LEFT_SQUIRREL_IMAGE,
                            (squirrel["width"], squirrel["height"]))

    squirrel["rect"] = squirrel["image"].get_rect()
    squirrel["rect"].topleft = (squirrel["x"] - camerax,
                                squirrel["y"] - cameray -
                                # Add bounce
                                getBounceAmount(squirrel["bounce"],
                                squirrel["bounceHeight"], squirrel["bounceRate"]))
    return squirrel

def makeNewGrass(camerax: int, cameray: int):
    grass = {}
    grass["image"]  = random.randint(1, len(GRASS_IMAGES) - 1)
    grass["width"]  = GRASS_IMAGES[grass["image"]].get_width()
    grass["height"] = GRASS_IMAGES[grass["image"]].get_height()
    grass["x"], grass["y"] = getRandomOffCameraPosition(camerax, cameray,
                             grass["width"], grass["height"])

    return grass

def makeNewSafeHouse(camerax: int, cameray: int):
    safeHouse = {}
    safeHouse["x"] ,safeHouse["y"] = getRandomOffCameraPosition(camerax, cameray, SAFEHOUSE_SIZE, SAFEHOUSE_SIZE)
    safeHouse["rect"] = SAFEHOUSE_IMAGE.get_rect()
    safeHouse["rect"].topleft = (safeHouse["x"] - camerax, safeHouse["y"] - cameray)

    return safeHouse

def movePlayer(playerSquirrel: {}, moveUp: bool, moveDown: bool,
               moveRight: bool, moveLeft: bool, camerax: int, cameray: int):

    if moveUp:
        playerSquirrel["y"] -= MOVE_RATE
    elif moveDown:
        playerSquirrel["y"] += MOVE_RATE
    if moveRight:
        playerSquirrel["x"] += MOVE_RATE
        playerSquirrel["image"] = pygame.transform.scale(RIGHT_SQUIRREL_IMAGE, (playerSquirrel["width"], playerSquirrel["height"]))
    elif moveLeft:
        playerSquirrel["x"] -= MOVE_RATE
        playerSquirrel["image"] = pygame.transform.scale(LEFT_SQUIRREL_IMAGE , (playerSquirrel["width"], playerSquirrel["height"]))

    # Bounce movement
    if (moveUp or moveDown or moveRight or moveLeft) or playerSquirrel["bounce"] != 0:
        playerSquirrel["bounce"] += 1

        if playerSquirrel["bounce"] > BOUNCE_RATE:
            playerSquirrel["bounce"] = 0

        # Add bounce sound
        if playerSquirrel["bounce"] == 0:
            BOUNCE_SOUND.play()

    playerSquirrel["rect"].topleft = (playerSquirrel["x"] - camerax, playerSquirrel["y"] - cameray -
                                      getBounceAmount(playerSquirrel["bounce"], BOUNCE_HEIGHT, BOUNCE_RATE))        

def moveSquirrels(squirrelObjs: [{}], camerax: int, cameray: int):

    for squirrel in squirrelObjs:
        squirrel["x"] += squirrel["movex"]
        squirrel["y"] += squirrel["movey"]
        squirrel["bounce"] += 1

        if squirrel["bounce"] > squirrel["bounceRate"]:
            squirrel["bounce"] = 0

        squirrel["rect"].topleft = (squirrel["x"] - camerax,
                                    squirrel["y"] - cameray -
                                    # Add bounce
                                    getBounceAmount(squirrel["bounce"],
                                    squirrel["bounceHeight"], squirrel["bounceRate"]))

        possibleChangeOfVelocity(squirrel)

def moveCamera(camerax: int, cameray: int, playerx: int, playery: int):

    if (camerax + WINDOW_WIDTH_HALF) - playerx > CAMERASLACK:
        camerax = playerx - WINDOW_WIDTH_HALF + CAMERASLACK
    elif playerx - (camerax + WINDOW_WIDTH_HALF) > CAMERASLACK:
        camerax = playerx - WINDOW_WIDTH_HALF - CAMERASLACK
    if (cameray + WINDOW_HEIGHT_HALF) - playery > CAMERASLACK:
        cameray = playery - WINDOW_HEIGHT_HALF + CAMERASLACK
    elif playery - (cameray + WINDOW_HEIGHT_HALF) > CAMERASLACK:
        cameray = playery - WINDOW_HEIGHT_HALF - CAMERASLACK

    return camerax, cameray

def eliminateFarAwayObjects(objects: [{}], amountOfObjects: int,
                            camerax: int, cameray: int):

    for i in range(amountOfObjects)[::-1]:
        if IsOutsideActiveArea(camerax, cameray, objects[i]["x"], objects[i]["y"],
                               objects[i]["width"], objects[i]["height"]):
            del objects[i]
            amountOfObjects -= 1

    return amountOfObjects

def eliminateFarAwaySafeHouse(safeHouse: {}, camerax: int, cameray: int):
    if IsOutsideActiveArea(camerax, cameray, safeHouse["x"], safeHouse["y"], SAFEHOUSE_SIZE, SAFEHOUSE_SIZE):
        safeHouse = makeNewSafeHouse(camerax, cameray)

    return safeHouse

def createEnoughSquirrels(playerSquirrel: {}, squirrelObjs: [{}], amountOfSquirrels: int,
                          camerax: int, cameray: int, neededAmountOfSquirrels: int):

    while amountOfSquirrels < neededAmountOfSquirrels:
        squirrelObjs.append(makeNewSquirrel(camerax, cameray, playerSquirrel))
        amountOfSquirrels += 1

    return amountOfSquirrels

def createEnoughGrass(grassObjs: [{}], amountOfGrass: int,
                      camerax: int, cameray: int):

    while amountOfGrass < AMOUNT_OF_GRASS:
        grassObjs.append(makeNewGrass(camerax, cameray))
        amountOfGrass += 1

    return amountOfGrass

def checkCollisions(playerSquirrel: {}, squirrelObjs: [{}], amountOfSquirrels: int,
                    invulnerableModeLastTime: int):
    lostLife = False
    playerx, playery = playerSquirrel["rect"].topleft
    for i in range(amountOfSquirrels)[::-1]:
        squirrelx, squirrely = squirrelObjs[i]["rect"].topleft
        if squirrelObjs[i]["width"] * squirrelObjs[i]["height"] > playerSquirrel["width"] * playerSquirrel["height"] and \
           squirrelObjs[i]["rect"].collidepoint(playerx + (playerSquirrel["width"]  // 2),
                                                playery + (playerSquirrel["height"] // 2)):
            playerSquirrel["health"] -= 1
            lostLife = True
            invulnerableModeLastTime = time.time()
            PUNCH_SOUND.play()

        elif playerSquirrel["width"] * playerSquirrel["height"] > squirrelObjs[i]["width"] * squirrelObjs[i]["height"] and \
             playerSquirrel["rect"].collidepoint(squirrelx + (squirrelObjs[i]["width"]  // 2),
                                                 squirrely + (squirrelObjs[i]["height"] // 2)):

            growSquirrel(playerSquirrel, squirrelObjs[i]["width"] * squirrelObjs[i]["height"])
            del squirrelObjs[i]
            amountOfSquirrels -= 1
            BITE_SOUND.play()


    return amountOfSquirrels, lostLife, invulnerableModeLastTime

def growSquirrel(playerSquirrel: {}, mass: int):
    playerSquirrel["width"]  += 5
    playerSquirrel["height"] += 5

def checkAMountOfSquirrelsNeeded(playerSquirrel: {}, neededAmountOfSquirrels: int):
    if playerSquirrel["width"] > 250:
        neededAmountOfSquirrels = 20
    elif playerSquirrel["width"] > 200:
        neededAmountOfSquirrels = 40
    elif playerSquirrel["width"] > 150:
        neededAmountOfSquirrels = 60
    elif playerSquirrel["width"] > 100:
        neededAmountOfSquirrels = 70

    return neededAmountOfSquirrels

def checkInvulnerableMode(lostLife: int, invulnerableModeLastTime: int, insideSafeHouse: bool):
    if lostLife and time.time() - invulnerableModeLastTime <= INVULNERABLE_MODE_DURATION:
        invulnerableMode = True
    if insideSafeHouse:
        invulnerableMode = True
    if not lostLife or time.time() - invulnerableModeLastTime >  INVULNERABLE_MODE_DURATION:
        invulnerableMode = False

    return invulnerableMode

def checkHealth(health: int):
    if health <= 0:
        lost = True
        EXPLOSION_SOUND.play()
    else:
        lost = False

    return lost

def checkPlayerInsideSafeHouse(safeHouse: {}, playerSquirrel: {}):
    if safeHouse["rect"].contains(playerSquirrel["rect"]):
        insideSafeHouse = True
    else:
        insideSafeHouse = False

    return insideSafeHouse

def getRandomVelocity():
    speed = random.randint(SQUIRREL_MIN_SPEED, SQUIRREL_MAX_SPEED)
    # Fifty fifty chance to go either direction
    if random.choice((0, 1)) == 0:
        return  speed
    else:
        return -speed

def possibleChangeOfVelocity(squirrel: {}):
    # 2% chance squirrel changes velocity
    if random.randint(0, 99) < CHANGE_DIRECTION_FREQ:
        squirrel["movex"] = getRandomVelocity()
        squirrel["movey"] = getRandomVelocity()

        # Update squirrel image
        if squirrel["movex"] > 0:
            squirrel["image"] = pygame.transform.scale(RIGHT_SQUIRREL_IMAGE,
                               (squirrel["width"], squirrel["height"]))
        else:
            squirrel["image"] = pygame.transform.scale(LEFT_SQUIRREL_IMAGE,
                               (squirrel["width"], squirrel["height"]))

def getRandomOffCameraPosition(camerax: int, cameray: int, objWidth: int, objHeight: int):
    valid = False
    cameraRect = pygame.Rect(camerax, cameray, WINDOW_WIDTH, WINDOW_HEIGHT)
    while not valid:
        x = random.randint(camerax - WINDOW_WIDTH , camerax + (WINDOW_WIDTH  * 2))
        y = random.randint(cameray - WINDOW_HEIGHT, cameray + (WINDOW_HEIGHT * 2))
        objRect = pygame.Rect(x, y, objWidth, objHeight)
        if not cameraRect.colliderect(objRect):
            valid = True

    return x, y

def IsOutsideActiveArea(camerax: int, cameray: int, objx: int, objy: int,
                        objWidth: int, objHeight: int):

    if camerax + (2 * WINDOW_WIDTH) < objx           or \
       cameray + (2 * WINDOW_HEIGHT) < objy          or \
       objx + objWidth < camerax - WINDOW_WIDTH      or \
       objy + objHeight < cameray - WINDOW_HEIGHT:

        return True

    else:
        return False

def getBounceAmount(bounceStep:int, bounceHeight: int, bounceRate: int, ):
    return math.sin( (math.pi / bounceRate) * bounceStep ) * bounceHeight

def getExplosionSize(playerSquirrel: {}):
    global EXPLOSION_IMAGE
    explosionSize   = playerSquirrel["width"] * 6
    EXPLOSION_IMAGE = pygame.transform.scale(EXPLOSION_IMAGE, (explosionSize, explosionSize))
    return explosionSize

def gameSetup():
    global FPSCLOCK
    pygame.init()
    loadImages()
    windowSetUp()
    soundSetUp()
    textSetUp()
    FPSCLOCK = pygame.time.Clock()

def terminate():
    pygame.quit()
    sys.exit()

def checkGameOver(playerSquirrel: {}, grassObjs: [{}], amountOfGrass: int, invulnerableMode: bool, invulnerableModeLastTime: int,
                  squirrelObjs: [{}], amountOfSquirrels: int, camerax: int, cameray: int, safeHouse: {}, lost: bool):
    
    restart = False
    if lost:
        while True:

            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()

                elif event.type == KEYUP:
                    if event.key == K_r:
                        restart = True
                    elif event.key == K_ESCAPE:
                        terminate()

            displayGame(playerSquirrel, grassObjs, amountOfGrass, invulnerableMode,
            invulnerableModeLastTime, squirrelObjs, amountOfSquirrels, camerax, cameray , safeHouse, lost)
            if restart:
                break

    return restart

def startScreen():
    EXPLOSION_SOUND.stop()
    pygame.mixer.music.play(-1, 0.0)
    while True:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()
                else:
                    return

        displayStartScreen()

def pauseGame():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()
                else:
                    return

        displayPause()

####################
##### GRAPHICS #####
####################

def displayGame(playerSquirrel: {}, grassObjs: [{}], amountOfGrass: int, invulnerableMode: bool, invulnerableModeLastTime: int,
                squirrelObjs: [{}], amountOfSquirrels: int, camerax: int, cameray: int, safeHouse: {}, lost: bool):

    DISPLAYSURF.fill(BACKGROUND_COLOR)
    # Draw grass
    for i in range(amountOfGrass):
        DISPLAYSURF.blit(GRASS_IMAGES[grassObjs[i]["image"]],
                        (grassObjs[i]["x"] - camerax,
                         grassObjs[i]["y"] - cameray))

    # Draw squirrels
    for i in range(amountOfSquirrels):
        DISPLAYSURF.blit(squirrelObjs[i]["image"],
                         squirrelObjs[i]["rect"])

    # Draw player squirrel
    if not invulnerableMode:
        DISPLAYSURF.blit(playerSquirrel["image"],
                         playerSquirrel["rect"])
    else:
        # Make player squirrel flash
        if round(time.time(), 1) * 10 % 2 == 1:
            DISPLAYSURF.blit(playerSquirrel["image"],
                             playerSquirrel["rect"])

    # Draw safe house
    DISPLAYSURF.blit(SAFEHOUSE_IMAGE, safeHouse["rect"])

    # Draw health bar
    healthBoxTopleftx = HEALTHBAR_TOPLEFT_X
    healthBoxToplefty = HEALTHBAR_TOPLEFT_Y
    for i in range(playerSquirrel["health"]):
        pygame.draw.rect(DISPLAYSURF, RED  , (healthBoxTopleftx, healthBoxToplefty, HEALTHBOX_WIDTH, HEALTHBOX_HEIGHT))
        healthBoxTopleftx += HEALTHBOX_WIDTH

    healthBoxTopleftx = HEALTHBAR_TOPLEFT_X
    for i in range(MAX_HEALTH):
        pygame.draw.rect(DISPLAYSURF, WHITE, (healthBoxTopleftx, healthBoxToplefty, HEALTHBOX_WIDTH, HEALTHBOX_HEIGHT), 2)
        healthBoxTopleftx += HEALTHBOX_WIDTH

    # Draw player size
    playerSizeSurf = BASICFONT.render(str(playerSquirrel["width"]), True, PLAYER_SIZE_TEXT_COLOR)
    playerSizeRect = playerSizeSurf.get_rect()
    playerSizeRect.center = (playerSquirrel["x"] - camerax + (playerSquirrel["width"]  // 2),
                             playerSquirrel["y"] - cameray + (playerSquirrel["height"] // 2) -
                             getBounceAmount(playerSquirrel["bounce"], BOUNCE_HEIGHT, BOUNCE_RATE))
    DISPLAYSURF.blit(playerSizeSurf, playerSizeRect)

    # Game over display
    if lost:
        explosionSize = getExplosionSize(playerSquirrel)
        gameoverRect  = GAMEOVER_IMAGE.get_rect()
        DISPLAYSURF.blit(EXPLOSION_IMAGE, (playerSquirrel["rect"].center[0] - (explosionSize // 2), 
                                           playerSquirrel["rect"].center[1] - (explosionSize // 2)))
        DISPLAYSURF.blit(GAMEOVER_IMAGE , (WINDOW_WIDTH_HALF   - gameoverRect.center[0], 100))

    pygame.display.update()
    FPSCLOCK.tick(FPS)

def displayStartScreen():

    pauseTextFont        = pygame.font.Font(BASICFONT_STYLE, 15)
    pauseTextSurf        = pauseTextFont.render("Press any key to continue.", True, WHITE)
    pauseTextRect        = pauseTextSurf.get_rect()
    pauseTextRect.center = (WINDOW_WIDTH_HALF, WINDOW_HEIGHT_HALF + 150)

    objectiveFont        = pygame.font.Font(BASICFONT_STYLE, 20)
    objectiveSurf        = objectiveFont.render("Reach Omega Squirrel!", True, WHITE)
    objectiveRect        = objectiveSurf.get_rect()
    objectiveRect.center = (WINDOW_WIDTH_HALF, WINDOW_HEIGHT_HALF + 100)

    creditsFont          = pygame.font.Font(BASICFONT_STYLE, 13)
    creditsSurf          = creditsFont.render("© Jose Acevedo", True, BLACK)
    creditsRect          = creditsSurf.get_rect()
    creditsRect.center   = (WINDOW_WIDTH_HALF + 190, WINDOW_HEIGHT_HALF + 55)

    DISPLAYSURF.fill(BRIGHTGREEN)
    DISPLAYSURF.blit(pauseTextSurf, pauseTextRect)
    DISPLAYSURF.blit(objectiveSurf, objectiveRect)
    DISPLAYSURF.blit(creditsSurf  , creditsRect)
    DISPLAYSURF.blit(TITLE_IMAGE  , (WINDOW_WIDTH_HALF  - (TITLE_WIDTH  // 2),
                                     WINDOW_HEIGHT_HALF - (TITLE_HEIGHT // 2)))

    titleGrass     = pygame.transform.scale(GRASS_IMAGES[3]    , (100, 100) )
    titleSquirrel1 = pygame.transform.scale(LEFT_SQUIRREL_IMAGE, (150, 150) )
    titleSquirrel2 = pygame.transform.flip(titleSquirrel1      , True, False)
    titleSquirrel3 = pygame.transform.scale(titleSquirrel1     , (300, 300) )

    DISPLAYSURF.blit(titleSquirrel1, (WINDOW_WIDTH_HALF // 3, WINDOW_HEIGHT_HALF // 3))
    DISPLAYSURF.blit(titleSquirrel2, (WINDOW_WIDTH_HALF, WINDOW_HEIGHT_HALF + WINDOW_HEIGHT_HALF // 2))
    DISPLAYSURF.blit(titleSquirrel3, (WINDOW_WIDTH_HALF + WINDOW_WIDTH_HALF // 2, WINDOW_HEIGHT_HALF // 4))
    DISPLAYSURF.blit(titleGrass    , (WINDOW_WIDTH_HALF, WINDOW_HEIGHT_HALF // 2))
    DISPLAYSURF.blit(titleGrass    , (WINDOW_WIDTH_HALF // 4, WINDOW_HEIGHT_HALF + 120))
    DISPLAYSURF.blit(titleGrass    , (WINDOW_WIDTH_HALF // 2, WINDOW_HEIGHT_HALF + 200))
    DISPLAYSURF.blit(titleGrass    , (WINDOW_WIDTH_HALF + 500, WINDOW_HEIGHT_HALF + 250))

    pygame.display.update()

def displayPause():
    pauseTextFont        = pygame.font.Font(BASICFONT_STYLE, 25)
    pauseTextSurf        = pauseTextFont.render("Press any key to continue.", True, WHITE)
    pauseTextRect        = pauseTextSurf.get_rect()
    pauseTextRect.center = (WINDOW_WIDTH_HALF, WINDOW_HEIGHT_HALF - 100)

    pauseFont            = pygame.font.Font(BASICFONT_STYLE, 60)
    pauseSurf            = pauseFont.render("PAUSED GAME", True, WHITE)
    pauseRect            = pauseSurf.get_rect()
    pauseRect.center     = (WINDOW_WIDTH_HALF, WINDOW_HEIGHT_HALF - 200)

    DISPLAYSURF.blit(pauseTextSurf, pauseTextRect)
    DISPLAYSURF.blit(pauseSurf    , pauseRect    )

    pygame.display.update()

if __name__ == "__main__":
    main()