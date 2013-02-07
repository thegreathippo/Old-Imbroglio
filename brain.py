from pathfinder import PathFinder
from constructor import M_NEIGHBORS, build_line

class Brain(object):
	def __init__(self, owner):
		self.owner = owner
		self.walls = set()
		self.floors = set()
		self.path = []
		self.pathfinder = PathFinder(self.get_adjacents, self.get_cost, self.get_heuristic)
	def observe(self):
		self.area = self.owner.owner.owner		
		for point in self.owner.fov:
			if point in self.area.terrain and self.area.terrain[point]['chasm'] == False:
				self.floors.add(point)
			else:
				self.floors.discard(point)
			if point in self.area.features:
				self.walls.add(point)
			else:
				self.walls.discard(point)
			if point in self.area.entities:
				entity = self.area.entities[point]
				if 'player' in entity and 'player' not in self.owner: 
					self.path = list(self.pathfinder.compute_path(self.owner.pos, entity.pos))
					self.path.pop(0)
	def get_adjacents(self, point):
		return set([pos for pos in M_NEIGHBORS[point] if pos in self.floors])
	def get_cost(self, start, end):
		return 1
	def get_heuristic(self, start, end):
		return len(build_line(start, end))
					
