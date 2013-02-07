import random, math
from vec2 import Vec2

MOORE = [(-1,-1),(-1,0),(-1,1),(0,1),(0,-1),(1,0),(1,1),(1,-1)]
NEUMANN = [(1,0),(-1,0),(0,1),(0,-1)]

def get_m_networks(points):
	completed = set()
	networks = []
	for point in points:
		if point in completed: continue
		network = get_m_network(point, points)
		completed.update(network)
		networks.append(network)
	return networks

def get_m_network(point, points):
	network = set([point])
	explored = set()
	unexplored = [point]
	while True:
		if unexplored == []: break
		cur_point = unexplored[0]
		for edge in M_NEIGHBORS[cur_point]:
			if edge not in points or edge in network or edge in explored: continue
			network.add(edge)
			unexplored.append(edge)
		unexplored.remove(cur_point)
		explored.add(cur_point)
	return network	

def get_n_networks(points):
	completed = set()
	networks = []
	for point in points:
		if point in completed: continue
		network = get_n_network(point, points)
		completed.update(network)
		networks.append(network)
	return networks

def get_n_network(point, points):
	network = set([point])
	explored = set()
	unexplored = [point]
	while True:
		if unexplored == []: break
		cur_point = unexplored[0]
		for edge in N_NEIGHBORS[cur_point]:
			if edge not in points or edge in network or edge in explored: continue
			network.add(edge)
			unexplored.append(edge)
		unexplored.remove(cur_point)
		explored.add(cur_point)
	return network	

def random_color():
	return random.randrange(40,150),random.randrange(40,150),random.randrange(40,150)

def add_tuple(xy1, xy2):
	return xy1[0] + xy2[0], xy1[1] + xy2[1]

def subtract_tuple(xy1, xy2):
	return xy1[0] - xy2[0], xy1[1] - xy2[1]

def get_closest_point(pos, points):
	min_distance = 50000.0
	for point in points:
		vec = subtract_tuple(pos, point)
		distance = math.hypot(vec[0], vec[1])
		if distance < min_distance:
			min_distance = distance
			result = point
	return result			

def get_outline(points):
	result = set()
	for point in points:
		for edge in M_NEIGHBORS[point]:
			if edge not in points:
				result.add(point)
				break
	return result

def get_trim(points):
	outline = get_outline(points)
	return points.difference(outline)

def get_trace(points):
	result = set()
	for point in points:
		dead_edges = set([xy for xy in M_NEIGHBORS[point] if xy not in points])
		result.update(dead_edges)
	return result

def get_tunnel(line):
	tunnel = set()
	for point in line:
		variance = random.randrange(-1,2), random.randrange(-1,2)
		radius = random.randrange(1,3)
		xy = add_tuple(point, variance)
		tunnel.update(build_circle(xy, radius))
	return tunnel	

def get_straight_tunnel(line):
	tunnel = set()
	for point in line:
		radius = random.randrange(2,3)
		tunnel.update(build_circle(point, radius))
	return tunnel	

def randomize(neighborhood, p = 0.5):
	points = set()
	for point in neighborhood:
		if random.randrange(0,100) * 0.01 < p:
			points.add(point)
	return points

def automata(neighborhood, start, dead = 3, alive = 6, iterations = 1):
	end = set(start)
	for i in range(iterations):
		points = set()
		for pos in neighborhood:
			if pos in end:
				if len([xy for xy in M_NEIGHBORS[pos] if xy in end]) > dead:
					points.add(pos)
				continue
			if len([xy for xy in M_NEIGHBORS[pos] if xy in end]) >= alive: points.add(pos)
		end = set(points)
	return end

def build_cave(neighborhood, p = 0.64):
	points = randomize(neighborhood, p)
	return automata(neighborhood, points, iterations = 5)

def build_circle(offset = (0,0), size = 5):
	result = set()
	for x in range(-size, size):
		for y in range(-size, size):
			if math.hypot(x, y) < size:
				result.add(add_tuple((x,y),offset))
	return result

def build_box(offset = (0,0), size = (100,100)):
	result = set()
	for x in range(0, size[0]):
		for y in range(0, size[1]):
			result.add(add_tuple((x,y),offset))
	return result
	
def build_line(xy1, xy2):
	x1, y1, x2, y2 = xy1[0], xy1[1], xy2[0], xy2[1] 
	points = []
	issteep = abs(y2-y1) > abs(x2-x1)
	if issteep:
		x1, y1 = y1, x1
		x2, y2 = y2, x2
	rev = False
	if x1 > x2:
		x1, x2 = x2, x1
		y1, y2 = y2, y1
		rev = True
	deltax = x2 - x1
	deltay = abs(y2-y1)
	error = int(deltax / 2)
	y = y1
	ystep = None
	if y1 < y2:
		ystep = 1
	else:
		ystep = -1
	for x in range(x1, x2 + 1):
		if issteep:
			points.append((y, x))
		else:
			points.append((x, y))
		error -= deltay
		if error < 0:
			y += ystep
			error += deltax
    # Reverse the list if the coordinates were reversed
	if rev:
		points.reverse()
	return points


def bake_neighbors(neighborhood, relationship):
	result = {}
	for block in neighborhood:
		result[block] = set([add_tuple(block,vec) for vec in relationship if add_tuple(block,vec) in neighborhood])
	return result

NEIGHBORHOOD = build_box((-1,-1),(202,202))
M_NEIGHBORS = bake_neighbors(NEIGHBORHOOD, MOORE)
N_NEIGHBORS = bake_neighbors(NEIGHBORHOOD, NEUMANN)
