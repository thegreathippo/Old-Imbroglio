from world import World
from nodes import *
import random

class Session(object):
	def __init__(self):
		self.world = World()
		points = set([node.pos for node in self.world[0].terrain.nodes if node['chasm'] == False])
		points.difference_update(set(self.world[0].features.data))
		self.player = EntityNode((random.choice(list(points))), {'player' : True})	
		self.world[0].entities[self.player.pos] = self.player

