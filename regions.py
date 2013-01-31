import math, random
from constructor import build_circle, Vec2

ADJACENCY = [(1,0),(-1,0),(0,1),(0,-1)]

class Region(object):
	def __init__(self, pos, size):
		self.pos = Vec2(pos)
		self.size = Vec2(size)
		self.initialize()
	def __len__(self):
		return self.size.x * self.size.y
	def __contains__(self, point):
		if self.left > point[0] or self.right - 1 < point[0]: return False
		if self.top > point[1] or self.bottom - 1 < point[1]: return False
		return True
	def initialize(self):
		self.width = self.size.x
		self.height = self.size.y
		self.left = self.pos.x
		self.right = self.pos.x + self.size.x
		self.top = self.pos.y
		self.bottom = self.pos.y + self.size.y
		self.topleft, self.topright = Vec2(self.left, self.top), Vec2(self.right - 1, self.top)
		self.bottomleft, self.bottomright = Vec2(self.left, self.bottom - 1), Vec2(self.right - 1, self.bottom - 1)
		self.corners = set([self.topleft.xy, self.topright.xy, self.bottomleft.xy, self.bottomright.xy])
		offset = self.size / 2
		self.center = self.pos + offset
		if self.width < self.height:
			self.short, self.tall = self.width, self.height
		else:
			self.short, self.tall = self.height, self.width
		self.children = set()
		self.parent = False
		self.zone = None
		self.structure = None
		self.edges = set()
		self.connections = set()
	def fill(self):
		result = set()
		for x in range(0, self.size.x):
			for y in range(0, self.size.y):
				point = Vec2(x, y)
				result.add((point + self.pos).xy)
		return result
	def search_up(self):
		if self.parent == False: return self
		return self.parent.search_up()
	def search_down(self):
		result = set()
		if self.children == set(): return set([self])
		for child in self.children:
			result.update(child.search_down())
		return result
	def search_by_proximity(self, region, value = 1):
		new_region = region.expand(value)
		return self.search_by_overlap(new_region)
	def search_by_overlap(self, region):
		result = set()
		if self.children == set(): return set([self])
		for child in self.children:
			if child.overlaps(region):
				result.update(child.search_by_overlap(region))
		return result	
	def contains_point(self, point):
		return point in self
	def overlaps(self, region):
		if self.left > region.right - 1: return False
		if self.right - 1 < region.left: return False
		if self.top > region.bottom - 1: return False
		if self.bottom - 1 < region.top: return False
		return True
	def move(self, vec):
		return Region(self.pos + Vec2(vec), self.size)
	def expand(self, value = 1):
		return Region(self.pos + Vec2(-value, -value), self.size + Vec2(value * 2,value * 2))
	def is_adjacent(self, region):
		test_regions = []
		for vec in ADJACENCY: test_regions.append(self.move(vec))
		for test_region in test_regions: 
			if test_region.overlaps(region): return ADJACENCY[test_regions.index(test_region)]
	def get_random_point(self):
		if self.short < 6: 
			return False
		return random.choice(list(build_circle(self.center, self.short / 4)))
	def pick_axis(self):
		if self.width > self.height * 1.25: return True
		if self.height > self.width * 1.25: return False
		return random.choice([True, False])		
	def slice_axis(self):
		axis = self.pick_axis()
		xy = self.get_random_point()
		if xy:
			if axis:
				width1, width2 = xy[0] - self.left, self.right - xy[0]				
				region1 = Region(self.pos, (width1, self.height))
				region2 = Region((xy[0], self.top), (width2, self.height))
			else:
				height1, height2 = xy[1] - self.top, self.bottom - xy[1]
				region1 = Region(self.pos, (self.width, height1))
				region2 = Region((self.left, xy[1]),(self.width, height2))
			self.children.update(set([region1, region2]))
			region1.parent, region2.parent = self, self
			return set([region1, region2])		
	def split_to_size(self, max_size = 750):
		regions_to_split = set([self])
		completed = set()
		while True:
			if regions_to_split == set(): break
			for region in regions_to_split.copy():
				new_regions = region.slice_axis()
				if len(region) < max_size or new_regions == None:
					regions_to_split.discard(region)
					completed.add(region)
					region.children = set()
					continue
				regions_to_split.remove(region)
				regions_to_split.update(new_regions)
		return completed

