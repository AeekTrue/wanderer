import pygame
pygame.init()


#variables

WIDTH = pygame.display.Info().current_w
HEIGHT = pygame.display.Info().current_h
#WIDTH, HEIGHT=800,600
FPS = 60


#init/create objs

sc = pygame.display.set_mode((WIDTH,HEIGHT),pygame.FULLSCREEN)
#sc = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()


#display objs
pygame.draw.circle(sc, 20, (100, 100), 255)
pygame.display.update()


#main loop

while 1:
	for event in pygame.event.get():
		if event.type == 2 and event.key==27:
			exit()

	#edit objs and other
	

	#UPD display

	pygame.display.update()
	

	#pause

	clock.tick(FPS)


