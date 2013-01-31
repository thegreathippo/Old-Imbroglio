import math, pygame, random
from fov import fov



class Node(object):
	def __init__(self, properties = None):
		if properties is None: properties = {}
		self.properties = dict(properties)
		self.init()
	def __getitem__(self, key):
		return self.properties[key]
	def __setitem__(self, key, value):
		self.properties[key] = value
	def init(self):
		pass

class GeoNode(Node):
	def __init__(self, pos, properties = None):
		if properties is None: properties = {}
		self.properties = dict(properties)
		self._pos = pos
		self.fov = Mask()
		self.init()
	def set_fov(self, mask, max_radius = 10):
		points = set()
		def visit(x, y):
			if (x, y) in mask:
				points.add((x,y))
				return True
			return points.add((x,y))
		fov(self.x, self.y, max_radius, visit)
		self.fov = Mask(points)
	def get_pos(self):
		return self._pos
	def get_x(self):
		return self._pos[0]
	def get_y(self):
		return self._pos[1]
	def __setpos(self, xy):
		self._pos = xy
	def __setx(self, x):
		self._pos = x, self._pos[1]
	def __sety(self, y):
		self._pos = self._pos[0], y
	pos = property(get_pos, __setpos, None, "gets or sets the coordinate of a GeoNode")
	x = property(get_x, __setx, None, "gets or sets the x value of a GeoNode")
	y = property(get_y, __sety, None, "gets or sets the y value of a GeoNode")

 
class RectNode(pygame.Rect, Node):
	def __init__(self, pos, size, properties = None):
		Node.__init__(self, properties)
		pygame.Rect.__init__(self, pos, size)

class GeoGraph(object):
	def __init__(self, nodes = None):
		if nodes is None: nodes = set()
		self.nodes = set(nodes)
		self.data = {}
		for node in self.nodes:
			self.data[node.pos] = node
	def __iter__(self):
		return iter(self.nodes)
	def __contains__(self, pos_or_node):
		if pos_or_node in self.data: return True
		if pos_or_node in self.nodes: return True
		return False
	def __delitem__(self, key):
		del self.data[key]
	def __getitem__(self, pos):
		return self.data[pos]
	def __setitem__(self, pos, node):
		if node in self.nodes:
			self.data[pos] = self.data.pop(node.pos)
			node.pos = pos
		else:
			self.nodes.add(node)
			self.data[pos] = node
			node.pos = pos
	def get_mask(self):
		return Mask(self.data.keys())

class RectGraph(pygame.Rect):
	def __init__(self, size = (1,1)):
		pygame.Rect.__init__(self, (0,0), size)
		self.nodes = set()
		self.data = {}
		for x in range(0,self.width):
			for y in range(0,self.height):
				if random.randrange(0, 2) == 0:
					self.data[(x,y)] = None
				else:
					self.data[(x,y)] = GeoNode((x,y),D_ITEM)
	def __iter__(self):
		return iter(self.data)
	def __contains__(self, pos):
		return pos in self.data
	def __len__(self):
		return len(self.data)
	def __getitem__(self, xy):
		return self.data[xy]
	def __setitem__(self, pos, node):
		if pos not in self:
			raise KeyError(str(pos) + " not in RectGraph")
		elif node is None:
			self.nodes.discard(self.data[pos])
			self.data[pos] = None
		elif node in self.nodes and self[pos] is None:
			self.data[node.pos] = None
			self.data[pos] = node
			node.pos = pos
		elif node in self.nodes:
			old_node = self.data.pop(pos)
			self.data[pos] = node
			node.pos = pos
			return old_node
		else:
			self.nodes.add(node)
			self.data[pos] = node
			node.pos = pos
	def set_random(self, node):
		for pos in self:
			if self[pos] == None: 
				self[pos] = node
				break
	def remaining_space(self):
		space = 0
		for pos in self:
			if self[pos] == None: space+=1
		return space	

class Mask(object):
	def __init__(self, points = None):
		if points is None: points = set()
		self.points = set(points)
		self.data = {point:0 for point in self.points}
	def __iter__(self):
		return iter(self.points)
	def __contains__(self, point):
		return point in self.points

