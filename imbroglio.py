import pygame, events
from pygame.locals import *
from stack import GUIStack
from session import Session

class Game(object):
	def __init__(self):
		events.init(self)
		self.clock = pygame.time.Clock()
		self.session = Session()
		self.stack = GUIStack(self)
	def tick(self, input_events):
		self.stack(input_events)
		self.turn_queue.apply()
		self.event_queue.apply()
		self.stack.tick()

game = Game()
while True:
	pygame.event.post(pygame.event.Event(USEREVENT, {}))
	game.tick(pygame.event.get())
	pygame.event.pump()
	game.clock.tick(30)				

