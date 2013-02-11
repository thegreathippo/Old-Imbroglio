from pathfinder import PathFinder
from constructor import M_NEIGHBORS, N_NEIGHBORS, build_line

class Brain(object):
	def __init__(self, owner):
		self.owner = owner
		self.walls = set()
		self.floors = set()
		self.entities = set()
		self.path = []
		self.pathfinder = PathFinder(self.get_adjacents, self.get_cost, self.get_heuristic)
	def observe(self):
		self.area = self.owner.owner.owner
		self.entities = set()
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
				self.entities.add(point)
		entities = self.area.entities.get_nodes(self.owner.fov)
		for node in entities:
			if 'player' in node and 'player' not in self.owner:
				self.entities.discard(node.pos)
				self.path = []
				path = self.pathfinder.compute_path(self.owner.pos, node.pos)
				for point in path:
					if point == self.owner.pos: continue
					self.path.append(point)
	def get_adjacents(self, point):
		return [pos for pos in M_NEIGHBORS[point] if pos in self.floors and pos not in self.walls and pos not in self.entities]
	def get_cost(self, start, end):
		return 1
	def get_heuristic(self, start, end):
		return len(build_line(start, end)) - 1
