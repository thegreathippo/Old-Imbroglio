from nodes import GeoGraph, GeoNode
from generator import Block

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
		self.fov_mask = self.features.get_mask()
	def get_nodes(self, mask):
		result = set()
		for point in mask:
			if point in self.terrain:
				result.add(self.terrain[point])
			if point in self.features:
				result.add(self.features[point])
			if point in self.entities:
				result.add(self.entities[point])
		return result
