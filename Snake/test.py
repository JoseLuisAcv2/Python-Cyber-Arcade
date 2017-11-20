import pygame
pygame.init()
pygame.display.set_mode((750,750))
pygame.mixer.music.load("/home/jose/Documents/GAMES/Snake/SnakeSounds/BackgroundMusic.mp3")
pygame.mixer.music.play(-1, 0.0)
while True:
	pygame.display.update()
