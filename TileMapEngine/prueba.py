import pygame
import collisionEngine
from pygame.locals import *

FPS                        = 30
WINDOW_WIDTH               = 1500
WINDOW_HEIGHT              = 700
WINDOW_WIDTH_HALF          = WINDOW_WIDTH  // 2
WINDOW_HEIGHT_HALF         = WINDOW_HEIGHT // 2
MOVERATE = 10
 
DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

rect1x         = 280
rect1y         = 200
rect1radius    = 50
rect2x         = 500
rect2y         = 300
rect2radius     = 100
rect1color     = (255,0,0)
rect2color     = (0,0,255)

while True:

	for event in pygame.event.get():
		if event.type == KEYDOWN:
			if event.key == K_RIGHT:
				rect1x += MOVERATE
			elif event.key == K_LEFT:
				rect1x -= MOVERATE
			elif event.key == K_UP:
				rect1y -= MOVERATE
			elif event.key == K_DOWN:
				rect1y += MOVERATE

	if collisionEngine.detectCircleCollision(rect1x, rect1y, rect1radius, rect2x, rect2y, rect2radius):
		rect1color = (0,255,0)
	else:
		rect1color = (255,0,0)

	DISPLAYSURF.fill((0,0,0))
	pygame.draw.circle(DISPLAYSURF,rect1color,(rect1x, rect1y),rect1radius)
	pygame.draw.circle(DISPLAYSURF,rect2color,(rect2x, rect2y), rect2radius)
	pygame.display.update()