class Brain(object):
	def __init__(self, owner):
		self.owner = owner
		self.walls = set()
		self.floors = set()
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
				
