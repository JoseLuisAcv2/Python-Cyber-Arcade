# Collision Engine
#
# By Jose Acevedo

import math

def AABBCollision(rect1x: int, rect1y: int, rect1Width: int, rect1Height: int,
			            rect2x: int, rect2y: int, rect2Width: int, rect2Height: int):

	if rect1x + rect1Width  > rect2x and \
	   rect2x + rect2Width  > rect1x and \
	   rect1y + rect1Height > rect2y and \
	   rect2y + rect2Height > rect1y:
	   return True
	else:
		return False

def circleCollision(circle1x: int, circle1y: int, circle1Radius: int,
						  circle2x: int, circle2y: int, circle2Radius: int):

	dx = abs(circle1x - circle2x)
	dy = abs(circle1y - circle2y)
	distance = math.sqrt(dx*dx + dy*dy)

	if distance < circle1Radius + circle2Radius:
		return True
	else:
		return False