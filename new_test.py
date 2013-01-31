import pygame, sys, random
from pygame.locals import *
from generator import Block


SCREEN_SIZE = (800, 640)

class Session(object):
	def __init__(self):
		pygame.init()
		self.clock = pygame.time.Clock()
		self.screen = pygame.display.set_mode(SCREEN_SIZE)
		self.dungeon = Block((125,125))
		self.dungeon.build()
	def tick(self, input_events):
		self.screen.fill((0,0,0))
		for event in input_events:
			if event.type == QUIT:
				sys.exit()
		for zone in self.dungeon.zones:
			for point in zone.floor:
				xy = point[0] * 3, point[1] * 3
				pygame.draw.rect(self.screen, zone.color, (xy,(2,2)))
			for point in zone.wall:
				xy = point[0] * 3, point[1] * 3
				pygame.draw.rect(self.screen, (230,230,230), (xy,(2,2)))
			for point in zone.path:
				xy = point[0] * 3, point[1] * 3
				pygame.draw.rect(self.screen, (120,120,120), (xy,(2,2)))


game = Session()

while True:
	game.tick(pygame.event.get())
	pygame.event.pump()
	pygame.display.flip()
	game.clock.tick(30)
