# Sonic
#
# By Jose Acevedo

import pygame
import sys
from pygame.locals import *

WINDOW_WIDTH  = 1000
WINDOW_HEIGHT = 500

def main():
	sonic = initializeGame()
	while True: # Main game loop

		# 1: Event handling loop
		for event in pygame.event.get():

			if event.type == QUIT:
				terminate()

			elif event.type == KEYDOWN:
				if event.key == K_RIGHT:
					sonic["standing"]  = False
					sonic["moveLeft"]  = False
					sonic["moveRight"] = True
				elif event.key == K_LEFT:
					sonic["standing"]  = False
					sonic["moveRight"] = False
					sonic["moveLeft"]  = True

			elif event.type == KEYUP:
				if event.key == K_RIGHT:
					sonic["moveRight"] = False
					sonic["standing"]  = True
				elif event.key == K_LEFT:
					sonic["moveLeft"] = False
					sonic["standing"]  = True

		# 2: Update game
		sonic = moveSonic(sonic)

		# 3: Display game
		displayGame(sonic)

def makeSonic():
	sonic = {"facing": "right",
			 "standing":True,
			 "moveRight": False,
			 "moveLeft": False,
			 "runRight": False,
			 "runLeft": False,
			 "jump": False,
			 "x":100,
			 "y":300,
			 "moveRate":5,
			 "runRate":10}

	return sonic

def moveSonic(sonic: {}):
	if sonic["moveRight"]:
		sonic["x"] += sonic["moveRate"]
	elif sonic["moveLeft"]:
		sonic["x"] -= sonic["moveRate"]

	return sonic

def windowSetUp():
	global DISPLAYSURF
	DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
	pygame.display.set_caption("Sonic")

def loadImages():
	global SPRITESHEET, BACKGROUND_IMAGE
	SPRITESHEET = pygame.image.load("sonicSpriteSheet.png")
	BACKGROUND_IMAGE = pygame.image.load("background.jpg")

def initializeGame():
	pygame.init()
	windowSetUp()
	loadImages()
	sonic = makeSonic()

	return sonic

def terminate():
	pygame.quit()
	sys.exit()

def displayGame(sonic: {}):
	# Draw background
	DISPLAYSURF.blit(BACKGROUND_IMAGE, (0, 0))
	
	# Draw sonic
	if sonic["standing"]:
		DISPLAYSURF.blit(SPRITESHEET, (sonic["x"], sonic["y"]), (0,0,90,120))

	pygame.display.update()

if __name__ == "__main__":
	main()