from world import World
from nodes import *
import random

class Session(object):
	def __init__(self):
		self.world = World()
		points = self.world[0].constructor.starter_zone.floor.difference(self.world[0].constructor.starter_zone.wall)
		self.player = EntityNode((random.choice(list(points))))	
		self.world[0].entities[self.player.pos] = self.player

