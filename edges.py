from constructor import *
import random


CHASM_ZONE = 0
CAVERN_ZONE = 1
DUNGEON_ZONE = 2

class RegionGraph(object):
	def __init__(self, leaves, root = None):
		if root is None: 
			root = random.choice(list(leaves)).search_up()
		self.root = root
		self.leaves = leaves
		self.data = {leaf: set() for leaf in self.leaves}
		self.assign_adjacency()
		self.assign_siblings()
	def __iter__(self):
		return iter(self.data)
	def __getitem__(self, key):
		return self.data[key]
	def __contains__(self, key):
		return key in self.data
	def assign_adjacency(self):
		for node in self:
			adjacents = set()
			possible_neighbors = self.root.search_by_proximity(node)
			for neighbor in possible_neighbors:
				if neighbor == node: continue
				axis = neighbor.is_adjacent(node)
				if axis: adjacents.add(Adjacency(node, neighbor, axis))
			self.data[node].update(adjacents)
	def assign_siblings(self):
		for node in self:
			for edge in self.data[node].copy():
				if edge.sibling != False: continue
				if edge.target not in self.data: 
					edge.sibling = Adjacency(edge.target, edge.owner, (-edge.axis[0], -edge.axis[1]))
					edge.set_pos(edge.center)
					continue
				for opposite_edge in self.data[edge.target]:
					if opposite_edge.target == edge.owner:
						opposite_edge.sibling = edge
						edge.sibling = opposite_edge
						edge.set_pos(edge.center)
						break
	def assign_zones(self, max_size = 4, one_step = False):
		unzoned = self.leaves.copy()
		zones = set()
		while unzoned != set():
			region = random.choice(list(unzoned))
			network = set([region])
			edges = set()
			for i in range(0, random.randrange(0, max_size)):
				for node in network.copy():
					for edge in self.data[node]:
						if edge.weight < 1 or edge.target not in unzoned: continue
						network.add(edge.target)
						if one_step: break
			for region in network:
				for edge in self[region]:
					if edge.target not in network:
						edges.add(edge)
			zones.add(Zone(network, edges))
			unzoned = unzoned.difference(network)
		self.connect_zones(zones)
		return zones
	def assign_structures(self, zone, max_size = 1, one_step = True):
		unstructured = self.leaves.copy()
		structures = set()
		while unstructured != set():
			region = random.choice(list(unstructured))
			network = set([region])
			for i in range(0, random.randrange(0, max_size)):
				for node in network.copy():
					for edge in self.data[node]:
						if edge.weight < 1 or edge.target not in unstructured: continue
						network.add(edge.target)
						if one_step: break
			structures.add(Structure(network, zone))
			unstructured = unstructured.difference(network)
		return structures
	def connect_zones(self, zones):
		network = set([random.choice(list(zones))])
		while network != zones:
			for zone in network.copy():
				for edge in zone.edges:
					if edge.target.zone in network or edge in zone.connections or edge.weight < 0 : continue
					zone.connections.add(edge)
					edge.target.zone.connections.add(edge.sibling)
					network.add(edge.target.zone)

class Adjacency(object):
	def __init__(self, owner, target, axis):
		self.owner = owner
		self.target = target
		self.axis = axis
		self.weight = 0
		self.sibling = False
		self.pos = False
		self.bounds = self.get_edge_bounds()
		self.center = self.get_center_of_edge()
		self.points = self.get_edge_points()
		self.calculate_weight()
	def __iter__(self):
		return iter(self.points)
	def __contains__(self, point):
		if point in self.points: return True
	def set_pos(self, pos):
		self.pos = pos
		if self.sibling:
			self.sibling.pos = get_closest_point(pos, self.sibling.points)
	def get_center_of_edge(self):
		edge_vector = (self.bounds[0] - self.bounds[1]) / 2
		return (edge_vector + self.bounds[1]).xy
	def get_edge_points(self):
		line = set(build_line(self.bounds[0], self.bounds[1]))
		return line
	def get_edge_bounds(self):
		edge = set()
		if self.axis == (1,0):
			edge_bounds = self.calculate_width_edge(self.owner.topleft.xy, self.owner.bottomleft.xy)
		if self.axis == (-1,0):
			edge_bounds = self.calculate_width_edge(self.owner.topright.xy, self.owner.bottomright.xy)
		if self.axis == (0,1):
			edge_bounds = self.calculate_height_edge(self.owner.topleft.xy, self.owner.topright.xy)
		if self.axis == (0,-1):
			edge_bounds = self.calculate_height_edge(self.owner.bottomleft.xy, self.owner.bottomright.xy)
		return Vec2(edge_bounds[0]), Vec2(edge_bounds[1])
	def calculate_width_edge(self, xy1, xy2):
		for top_y in xrange(xy1[1], xy2[1] + 1):
			edges = [xy for xy in N_NEIGHBORS[(xy1[0], top_y)] if self.target.contains_point(xy)]
			if len(edges) > 0: break
		for bottom_y in xrange(xy2[1], xy1[1] - 1, -1):
			edges = [xy for xy in N_NEIGHBORS[(xy1[0], bottom_y)] if self.target.contains_point(xy)]
			if len(edges) > 0: break			
		return (xy1[0], top_y), (xy1[0], bottom_y)
	def calculate_height_edge(self, xy1, xy2):
		for left_x in xrange(xy1[0], xy2[0] + 1):
			edges = [xy for xy in N_NEIGHBORS[(left_x, xy1[1])] if self.target.contains_point(xy)]
			if len(edges) > 0: break
		for right_x in xrange(xy2[0], xy1[0] - 1, -1):
			edges = [xy for xy in N_NEIGHBORS[(right_x, xy1[1])] if self.target.contains_point(xy)]
			if len(edges) > 0: break			
		return (left_x, xy1[1]), (right_x, xy1[1])					
	def calculate_weight(self):
		#ADJACENCY WEIGHTS:
		# -1 : Corner Adjacency (worst allowable kind)
		# 0 : Arbitrary adjacency (most common kind)
		# 1 : Complete adjacency (owner's side is owned by target)
		# 2 : Mutual Complete Adjacency (both sides are owned by each other)
		if self.axis == (1,0) or self.axis == (-1,0): 
			target_side = self.target.height
			owner_side = self.owner.height
		else: 
			target_side = self.target.width
			owner_side = self.owner.width
		if owner_side == len(self.points): 
			self.weight = 1
			if target_side == owner_side:
				self.weight = 2
		if target_side / 2 > len(self.points) and owner_side / 2 > len(self.points):
			self.weight = -1


class Zone(object):
	def __init__(self, regions, edges):
		self.regions = regions
		self.edges = edges
		self.color = random_color()
		self.neighborhood = set()
		self.structures = set()
		self.connections = set()
		self.path = set()
		self.wall = set()
		self.kind = None
		for region in self.regions:
			region.zone = self
			region.color = self.color
			self.neighborhood.update(region.fill())
		self.area = self.neighborhood
		self.neighborhood = self.neighborhood.difference(get_outline(self.neighborhood))
		self.floor = set()
	def define(self):
		if len(self.regions) == 1:
			return LobbyZone(self.regions, self.edges, self.connections)
		zone_type = random.randrange(0, 2)
		if zone_type == 0:
			return CavernZone(self.regions, self.edges, self.connections)
		if zone_type == 1:
			return ChasmZone(self.regions, self.edges, self.connections)
		if zone_type == 2:
			return DungeonZone(self.regions, self.edges, self.connections)			
	def update_structures(self, region_graph):
		for structure in self.structures:
			structure.update_edges(region_graph)

class DefinedZone(Zone):
	def __init__(self, regions, edges, connections):
		self.regions = regions
		self.edges = edges
		self.connections = connections
		self.color = random_color()
		self.neighborhood = set()
		self.structures = set()
		self.path = set()
		self.wall = set()
		self.kind = None
		for region in self.regions:
			region.zone = self
			region.color = self.color
			self.neighborhood.update(region.fill())
		self.area = self.neighborhood
		self.neighborhood = self.neighborhood.difference(get_outline(self.neighborhood))
		self.floor = set()	

class StructuredZone(DefinedZone):
	def prep_structures(self):
		edges = set()
		for structure in self.structures:
			for edge in structure.edges:
				if edge.weight > 0 and edge.target.zone == self: 
					edges.add(edge)
					edges.add(edge.sibling)
			structure.edges = set()
		for edge in edges:
			edge.owner.structure.edges.add(edge)
		for edge in self.connections:
			if edge.owner.structure in self.structures:
				edge.owner.structure.connections.add(edge)
				edge.owner.structure.lobby = True		
	def draw_path(self):
		self.prep_structures()
		halls, rooms = set(), set()
		for structure in self.structures:
			if structure in rooms: continue
			sides = {(-1,0) : set(), (1,0) : set(), (0,-1) : set(), (0,1) : set()}
			for edge in structure.edges:
				if edge.target.structure in rooms or edge.target.structure in halls: continue
				other_edges = [other_edge for other_edge in sides[edge.axis] if other_edge.target.structure == edge.target.structure]
				if other_edges != []: continue
				sides[edge.axis].add(edge)
			for axis in sides:
				if len(sides[axis]) > 2:
					halls.add(structure)
					structure.hall = True
					for edge in sides[axis]:
						structure.connections.add(edge)
						edge.target.structure.connections.add(edge.sibling)
						rooms.add(edge.target.structure)
						edge.target.structure.room = True
						structure.rooms.add(edge.target.structure)
		for hall in halls:
			for edge in hall.edges:
				if edge.target.structure in halls:
					hall.connections.add(edge)
					edge.target.structure.connections.add(edge.sibling)
					break
		network = set([random.choice(list(self.structures))])
		while network != self.structures:
			for structure in network.copy():
				for edge in structure.connections:
					if edge.target.zone == structure.zone and edge.target.structure not in network:
						network.add(edge.target.structure) 
				for edge in structure.edges:
					if edge.target.zone != structure.zone or edge in structure.connections or edge.target.structure in network: continue
					if edge.target.structure.room and random.randrange(0, 5) > 0: continue
					structure.connections.add(edge)
					edge.target.structure.connections.add(edge.sibling)
					network.add(edge.target.structure)
					break
		self.cull_structures(3, 5)
		for structure in self.structures:
			self.path.update(set([edge.pos for edge in structure.connections]))
			self.wall.update(structure.build_walls().difference(self.path))
		self.path = set()
	def cull_structures(self, iterations = 1, min_size = 10):
		for i in range(0, iterations):
			if len(self.structures) > min_size:
				for structure in self.structures.copy():
					if len(structure.connections) == 1 and structure.lobby == False and structure.room == False:
						self.structures.remove(structure)
						for edge in structure.connections:
							edge.target.structure.connections.remove(edge.sibling)		
	def determine_interior_edges(self, adjacency_graph):
		pass

class OpenZone(DefinedZone):
	def draw_path(self):
		access_points = set()
		for edge in self.connections:
			pos = get_closest_point(edge.pos, self.floor)
			tunnel = get_straight_tunnel(build_line(pos, edge.pos)).intersection(self.area)
			self.floor.update(tunnel)
			access_points.add(edge.pos)
		self.wall.update(get_trace(self.floor).intersection(self.area))
	def determine_interior_edges(self, adjacency_graph):
		for region in self.regions:
			for edge in adjacency_graph[region]:
				if edge.target.zone != region.zone: continue
				area = self.floor.intersection(region.fill().union(edge.target.fill()))
				if len(get_m_networks(area)) == 1:
					region.edges.add(edge)
	def connect_all_points_in_region(self, region):
		neighborhood = region.fill().intersection(self.neighborhood)
		networks = get_n_networks(self.floor.intersection(neighborhood))
		if len(networks) > 1:
			networks.sort(key = lambda network: len(network), reverse = True)
			main_network = networks[0]
			pathway = self.pathway(networks[1], main_network).intersection(neighborhood)
			self.floor.update(pathway)
			self.connect_all_points_in_region(region)
	def pathway(self, points, network):
		pos1 = random.choice(list(points))
		pos2 = get_closest_point(pos1, network)
		line = build_line(pos1, pos2)
		pathway = get_tunnel(line)
		return pathway

class CavernZone(OpenZone):
	def construct(self):
		self.color = (120,120,120)
		self.floor = build_cave(self.neighborhood).intersection(self.neighborhood)
		for region in self.regions:
			self.floor.add(region.center.xy)
			self.connect_all_points_in_region(region)

class ChasmZone(OpenZone):
	def construct(self):
		self.color = (40,40,40)
		self.floor = build_cave(self.neighborhood, .70).intersection(self.neighborhood)
		for region in self.regions:
			self.floor.add(region.center.xy)
			self.connect_all_points_in_region(region)		
	def draw_path(self):
		unexplored = [random.choice(list(self.regions))]
		visited = set()
		explored = set()
		while unexplored != []:
			cur_region = unexplored[0]
			for edge in cur_region.edges:
				if edge.target in explored: continue
				if edge.target in visited and random.randrange(0,5) > 0: continue
				cur_region.connections.add(edge)
				edge.target.connections.add(edge.sibling)
				self.path.update(get_straight_tunnel(build_line(cur_region.center.xy, edge.pos)))
				self.path.update(build_circle(cur_region.center.xy, random.randrange(2,4)))
				if edge.target.zone == cur_region.zone:
					self.path.update(get_straight_tunnel(build_line(edge.sibling.pos, edge.target.center.xy)))
					unexplored.append(edge.target)
				visited.add(edge.target)
			unexplored.remove(cur_region)
			explored.add(cur_region)
		for region in self.regions:
			if len(region.connections) == 1:
				self.path.update(build_circle(region.center.xy, 5))
		self.path = self.path.intersection(self.area)
		self.floor.update(self.path)
		self.wall.update(get_trace(self.floor).intersection(self.area))			

class LobbyZone(StructuredZone):
	def construct(self):
		self.floor = set()
		rooms = set()
		for region in self.regions:
			rooms.update(region.split_to_size(0))
		for room in rooms:
			room.zone = self
		graph = RegionGraph(rooms)
		self.structures = graph.assign_structures(self, 4, True)	
	def draw_path(self):
		self.prep_structures()
		halls, rooms = set(), set()
		for structure in self.structures:
			if structure in rooms: continue
			sides = {(-1,0) : set(), (1,0) : set(), (0,-1) : set(), (0,1) : set()}
			for edge in structure.edges:
				if edge.target.structure in rooms or edge.target.structure in halls: continue
				other_edges = [other_edge for other_edge in sides[edge.axis] if other_edge.target.structure == edge.target.structure]
				if other_edges != []: continue
				sides[edge.axis].add(edge)
			for axis in sides:
				if len(sides[axis]) > 2:
					halls.add(structure)
					structure.hall = True
					for edge in sides[axis]:
						structure.connections.add(edge)
						edge.target.structure.connections.add(edge.sibling)
						rooms.add(edge.target.structure)
						edge.target.structure.room = True
						structure.rooms.add(edge.target.structure)
		for hall in halls:
			for edge in hall.edges:
				if edge.target.structure in halls:
					hall.connections.add(edge)
					edge.target.structure.connections.add(edge.sibling)
					break
		network = set([random.choice(list(self.structures))])
		while network != self.structures:
			for structure in network.copy():
				for edge in structure.connections:
					if edge.target.zone == structure.zone and edge.target.structure not in network:
						network.add(edge.target.structure) 
				for edge in structure.edges:
					if edge.target.zone != structure.zone or edge in structure.connections or edge.target.structure in network: continue
					if edge.target.structure.room and random.randrange(0, 5) > 0: continue
					structure.connections.add(edge)
					edge.target.structure.connections.add(edge.sibling)
					network.add(edge.target.structure)
					break
		for structure in self.structures:
			self.path.update(set([edge.pos for edge in structure.connections]))
			self.wall.update(structure.build_walls().difference(self.path))
		self.path = set()

class DungeonZone(StructuredZone):
	def construct(self):
		self.floor = set()
		rooms = set()
		for region in self.regions:
			rooms.update(region.split_to_size(0))
		for room in rooms:
			room.zone = self
		graph = RegionGraph(rooms)
		self.structures = graph.assign_structures(self, 3, False)		

class Structure(object):
	def __init__(self, regions, zone):
		self.regions = regions
		self.zone = zone
		self.edges = set()
		self.connections = set()
		self.neighborhood = set()
		self.hall = False
		self.room = False
		self.lobby = False
		self.rooms = set()
		for region in self.regions:
			region.structure = self
			self.neighborhood.update(region.fill())
		self.floor = self.neighborhood
	def draw(self):
		self.zone.floor.update(self.floor)
	def build_walls(self):
		walls = get_outline(self.floor)
		return walls
	def update_edges(self, region_graph):
		for region in self.regions:
			for edge in region_graph[region]:
				if edge.target.structure != self:
					self.edges.add(edge)
		for connection in self.zone.connections.copy():
			for edge in self.edges:
				if edge.target.zone != connection.target.zone: continue
				if edge.pos in edge.owner.corners or edge.sibling.pos in edge.target.corners: continue
				self.zone.connections.remove(connection)
				connection.target.zone.connections.remove(connection.sibling)
				self.zone.connections.add(edge)
				edge.target.zone.connections.add(edge.sibling)
				break		