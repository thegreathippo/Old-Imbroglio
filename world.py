from nodes import GeoGraph, GeoNode
from generator import Block
import random

class World(object):
	def __init__(self):
		self.areas = {(0,0,0) : Area()}
		self.cur_area = (0,0,0)
	def __getitem__(self, key):
		if key == 0:
			key = self.cur_area
		return self.areas[key]

class Area(object):
	def __init__(self):
		self.terrain = GeoGraph()
		self.features = GeoGraph()
		self.entities = GeoGraph()
		self.constructor = Block((100,100))
		self.constructor.build()
		for zone in self.constructor.zones:
			for point in zone.floor:
				self.terrain[point] = GeoNode(point)
			for point in zone.wall:
				self.features[point] = GeoNode(point)
		possible_points = set(self.terrain.data).difference(set(self.features.data))
		for point in possible_points:
			if random.randrange(0,100) == 0:
				self.entities[point] = GeoNode(point)
		print str(len(self.entities.nodes))
		self.fov_mask = self.features.get_mask()
	def get_nodes(self, mask):
		result = set()
		result.update(self.terrain.get_nodes(mask))
		result.update(self.features.get_nodes(mask))
		result.update(self.entities.get_nodes(mask))
		return result
