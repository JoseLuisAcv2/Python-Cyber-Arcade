# Projectile Launch Simulator
#
# By Jose Acevedo

import pygame
import math
import time
import sys
from pygame.locals import *

pygame.init()

BLACK               = (  0,   0,   0)
WHITE               = (240, 240, 240)
LIGHTBLUE           = (128, 204, 189)
GRAY                = (97 , 129, 129)
FPS                 = 60
WINDOW_WIDTH        = 1500
WINDOW_HEIGHT       = 1000
PROJECTILE1_WIDTH   = 200
PROJECTILE1_HEIGHT  = 100
PROJECTILE2_WIDTH   = 30
PROJECTILE2_HEIGHT  = 30
projectileImage     = "tennisBall.png"

axisx               = 73
axisy               = 135
displacementxi      = 73
displacementyi      = 135
gravity             = -450
mass                = 0.7 # kg

def main(): 
	simulatorSetUp()
	projectileObjs = initializeSimulator()
	while True:

		# 1: Event handling loop
		for event in pygame.event.get():
	
			if event.type == QUIT:
				terminate()

			elif event.type == KEYUP:
				if event.key == K_SPACE:
					launchNewProjectile(projectileObjs)
					projectileObjs.append(makeProjectile())

				if event.key == K_ESCAPE:
					terminate()

		# 2: Update game
		moveProjectiles(projectileObjs)
		eliminateFarAwayProjectiles(projectileObjs)

		# 3: Display graphics
		displaySimulator(projectileObjs)

def makeProjectile():
	projectile = {}
	projectile["fired"]         = False
	projectile["displacementx"] = displacementxi
	projectile["displacementy"] = displacementyi
	projectile["velocityx"]     = 0
	projectile["velocityy"]     = 0	
	projectile["accelerationx"] = 0
	projectile["accelerationy"] = gravity
	projectile["angle"]         = getAngle(displacementxi, displacementyi - PROJECTILE2_HEIGHT)
	projectile["mass"]          = mass
	projectile["force"]         = getForce()
	projectile["impulse"]       = 0

	return projectile

def eliminateFarAwayProjectiles(projectileObjs: []):
	flightTime = None
	for i in range(len(projectileObjs))[::-1]:
		if projectileObjs[i]["displacementx"] >  WINDOW_WIDTH    or \
		   projectileObjs[i]["displacementx"] < -500             or \
		   projectileObjs[i]["displacementy"] < -500:
			if i == 0:
				del projectileObjs[i]

def launchNewProjectile(projectileObjs: []):
	for projectile in projectileObjs:
		if projectile["fired"] == False:
			projectile["fired"] = True
			projectile["impulse"]    = getImpulse(projectile["force"])
			projectile["velocityi"]  = getInitialVelocity(projectile["mass"], projectile["impulse"])
			projectile["velocityxi"] = getInitialVelocityComponents(projectile["angle"], projectile["velocityi"])[0]
			projectile["velocityyi"] = getInitialVelocityComponents(projectile["angle"], projectile["velocityi"])[1]
			projectile["velocityx"]  = projectile["velocityxi"]
			projectile["velocityy"]  = projectile["velocityyi"]
			projectile["startTime"]  = time.time()
			break	

def getAngle(centerx: int, centery: int):
	mousex, mousey = pygame.mouse.get_pos()
	mousey = WINDOW_HEIGHT - mousey
	distancex = mousex - centerx - (PROJECTILE2_WIDTH  // 2)
	distancey = mousey - centery - (PROJECTILE2_HEIGHT // 2)
	if distancex == 0:
		if mousey >= centery:
			angle = 90
		elif mousey < centery:
			angle = 270

	elif distancex > 0:
		if mousey >= centery:
			angle = math.degrees(math.atan(distancey / distancex))
		elif mousey < centery:
			angle = math.degrees(math.atan(distancey / distancex)) + 360
	elif distancex < 0:
		if mousey >= centery:
			angle = math.degrees(math.atan(distancey / distancex)) + 180
		elif mousey < centery:
			angle = math.degrees(math.atan(distancey / distancex)) + 180

	return angle

def getInitialVelocity(objMass: int, objImpulse: int):
	return objImpulse // objMass

def getForce():
	mousex, mousey = pygame.mouse.get_pos()
	mousey = WINDOW_HEIGHT - mousey
	distancex = mousex - axisx - (PROJECTILE2_WIDTH // 2)
	distancey = mousey - axisy + (PROJECTILE2_HEIGHT // 2)

	return math.sqrt(distancex**2 + distancey**2)*2

def getImpulse(force: int):
	return force * 0.5 # Collision time 0.5s

def getInitialVelocityComponents(angle: int, initialVelocity: int):
	initialVelocityx = int(initialVelocity * math.cos(math.radians(angle)))
	initialVelocityy = int(initialVelocity * math.sin(math.radians(angle)))

	return initialVelocityx, initialVelocityy

def moveProjectiles(projectileObjs: []):
	for i in range(len(projectileObjs) - 1):
		t = time.time() - projectileObjs[i]["startTime"]
		projectileObjs[i]["displacementx"] = displacementxi + (projectileObjs[i]["velocityx"]*t) + (0.5*projectileObjs[i]["accelerationx"]*t*t)
		projectileObjs[i]["displacementy"] = displacementyi + (projectileObjs[i]["velocityy"]*t) + (0.5*projectileObjs[i]["accelerationy"]*t*t)
		projectileObjs[i]["velocityx"]     = projectileObjs[i]["velocityxi"] + (projectileObjs[i]["accelerationx"]*t)
		projectileObjs[i]["velocityy"]     = projectileObjs[i]["velocityyi"] + (projectileObjs[i]["accelerationy"]*t)

	# Make projectile follow mouse cursor
	projectileObjs[len(projectileObjs) - 1]["angle"] = getAngle(displacementxi, displacementyi - PROJECTILE2_HEIGHT)
	# Calculate applicable force from given distance
	projectileObjs[len(projectileObjs) - 1]["force"] = getForce()

def simulatorSetUp():
	global FPSCLOCK, BASICFONT, BASICFONT2, PROJECTILE_IMAGE
	windowSetUp()
	loadBackground()
	loadCartesianPlane()
	FPSCLOCK   = pygame.time.Clock()
	BASICFONT  = pygame.font.Font("freesansbold.ttf", 20)
	BASICFONT2 = pygame.font.Font("freesansbold.ttf", 15)
	if projectileImage == "projectile.png":
		PROJECTILE_IMAGE = loadImage(projectileImage, PROJECTILE1_WIDTH ,PROJECTILE1_HEIGHT)
	elif projectileImage == "tennisBall.png":
		PROJECTILE_IMAGE = loadImage(projectileImage, PROJECTILE2_WIDTH ,PROJECTILE2_HEIGHT)

def initializeSimulator():
	projectileObjs = []
	projectileObjs.append(makeProjectile())

	return projectileObjs

def windowSetUp():
	global DISPLAYSURF
	DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
	pygame.display.set_caption("Projectile Simulator")	

def loadBackground():
	global BACKGROUND_IMAGE, backgroundImageWidth, backgroundImageHeight
	BACKGROUND_IMAGE      = pygame.image.load("background.jpg")
	backgroundImageWidth  = BACKGROUND_IMAGE.get_rect().width
	backgroundImageHeight = BACKGROUND_IMAGE.get_rect().height

def loadCartesianPlane():
	global AXIS_IMAGE, GRID_IMAGE
	AXIS_IMAGE = loadImage("axis.gif", WINDOW_WIDTH - 80, WINDOW_HEIGHT - 110)
	GRID_IMAGE = loadImage("grid.png", WINDOW_WIDTH - 140, WINDOW_HEIGHT - 140)

def displaySimulator(projectileObjs: []):
	DISPLAYSURF.fill(LIGHTBLUE)
	drawBackground()
	drawCartesianPlane()
	drawProjectiles(projectileObjs)
	drawProjectileInfo(projectileObjs)
	pygame.display.update()
	FPSCLOCK.tick(FPS)

def drawBackground():
	numberOfImagesNeeded = WINDOW_WIDTH // backgroundImageWidth + 1
	for i in range(numberOfImagesNeeded):
		DISPLAYSURF.blit(BACKGROUND_IMAGE, (i*backgroundImageWidth, WINDOW_HEIGHT - backgroundImageHeight))

def drawProjectiles(projectileObjs: []):
	for projectile in projectileObjs:
		projectileImageRotated = pygame.transform.rotate(PROJECTILE_IMAGE, projectile["angle"])
		DISPLAYSURF.blit(projectileImageRotated, (projectile["displacementx"], WINDOW_HEIGHT - projectile["displacementy"]))

def drawCartesianPlane():
	DISPLAYSURF.blit(AXIS_IMAGE, (30, 30))
	DISPLAYSURF.blit(GRID_IMAGE, (74, 40))

def drawProjectileInfo(projectileObjs: []):
	# Draw degrees of inclination
	angleSurf = BASICFONT.render("Degrees: " + str(round(projectileObjs[len(projectileObjs)-1]["angle"],2)) + "º", True, WHITE)
	angleRect = angleSurf.get_rect()
	angleRect.topleft = (120, WINDOW_HEIGHT - 55)
	DISPLAYSURF.blit(angleSurf, angleRect)

	# Draw impulse given to projectile
	impulseSurf = BASICFONT.render("Impulse: " + str(round(projectileObjs[0]["impulse"],2)) + "N*s", True, WHITE)
	impulseRect = impulseSurf.get_rect()
	impulseRect.topleft = (360, WINDOW_HEIGHT - 55)
	DISPLAYSURF.blit(impulseSurf, impulseRect)	

	# Draw height of projectile
	heightSurf = BASICFONT.render("Height: " + str(round(projectileObjs[0]["displacementy"]-axisy,2)) + "m", True, WHITE)
	heightRect = heightSurf.get_rect()
	heightRect.topleft = (600, WINDOW_HEIGHT - 55)
	DISPLAYSURF.blit(heightSurf, heightRect)

	# Draw range of projectile
	rangeSurf = BASICFONT.render("Range: " + str(round(projectileObjs[0]["displacementx"]- axisx,2)) + "m", True, WHITE)
	rangeRect = rangeSurf.get_rect()
	rangeRect.topleft = (800, WINDOW_HEIGHT - 55)
	DISPLAYSURF.blit(rangeSurf, rangeRect)

	# Draw speed of projectile
	speed = math.sqrt(projectileObjs[0]["velocityx"]**2 + projectileObjs[0]["velocityy"]**2)
	speedSurf = BASICFONT.render("Speed: " + str(round(speed ,2)) + "m/s", True, WHITE)
	speedRect = speedSurf.get_rect()
	speedRect.topleft = (1000, WINDOW_HEIGHT - 55)
	DISPLAYSURF.blit(speedSurf, speedRect)

	# Draw time elapsed since start of motion
	if projectileObjs[0]["fired"]:
		timeElapsed = time.time() - projectileObjs[0]["startTime"]
	else:
		timeElapsed = 0
	timeSurf = BASICFONT.render("Time Elapsed: " + str(round(timeElapsed,2)) + "s", True, WHITE)
	timeRect = timeSurf.get_rect()
	timeRect.topleft = (1230, WINDOW_HEIGHT - 55)
	DISPLAYSURF.blit(timeSurf, timeRect)

	# Draw line between projectile and mouse cursor
	pygame.draw.line(DISPLAYSURF, WHITE, (axisx + (PROJECTILE2_WIDTH // 2),
	WINDOW_HEIGHT - axisy + (PROJECTILE2_HEIGHT // 2)), (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]), 2)

	# Draw force aplication
	initialSpeed     = BASICFONT2.render("Force: " + str(round(projectileObjs[0]["force"],2)) + "N", True, WHITE)
	initialSpeedRect = initialSpeed.get_rect()
	initialSpeedRect.topleft = (pygame.mouse.get_pos()[0]+20, pygame.mouse.get_pos()[1])
	DISPLAYSURF.blit(initialSpeed, initialSpeedRect)	

def loadImage(imageFileName: str, imageWidth: int, imageHeight: int):
	image = pygame.image.load(imageFileName)
	return pygame.transform.scale(image, (imageWidth, imageHeight))

def terminate():
	pygame.quit()
	sys.exit()

if __name__ == "__main__":
	main()