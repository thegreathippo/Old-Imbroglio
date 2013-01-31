from regions import Region
from edges import RegionGraph
import random

class Block(object):
	def __init__(self, size):
		self.size = size
		self.path = set()
		self.zones = set()
	def build(self):
		self.root = Region((0,0), self.size)
		self.regions = self.root.split_to_size(1000)
		self.graph = RegionGraph(self.regions)
		self.zones = self.graph.assign_zones(3)
		self.build_structures()
		self.starter_zone = random.choice(list(self.zones))
	def build_structures(self):
		for zone in self.zones.copy():
			self.zones.remove(zone)
			self.zones.add(zone.define())
		for zone in self.zones:
			zone.construct()
		structure_graph = RegionGraph(self.root.search_down(), self.root)
		for zone in self.zones:
			zone.determine_interior_edges(self.graph)
			zone.update_structures(structure_graph)
		for zone in self.zones:
			for edge in zone.connections:
				edge.owner.edges.add(edge)	
		for zone in self.zones:
			zone.draw_path()	
		for zone in self.zones:
			for structure in zone.structures:
				structure.draw()
