from images import *
from widget import *


class GameMap(Widget):
	def init(self):
		self.children = set()
		self.terrain = set()
		self.features = set()
		self.entities = set()
		self.nodes = {}
		self.rect = pygame.Rect((0,0), self.parent.rect.size)
		self.image = get_surface(self.rect.size, self.bcolor)
		if 'focus' not in self:
			self.focus = self.parent.focus
		self.focus.set_fov(self.area.fov_mask)
		self.fov = self.focus.fov
		for node in self.area.get_nodes(self.fov):
			if node in self.area.terrain:
				terrain = Terrain(self, pos = (node.x * self.parent.cell, node.y * self.parent.cell))
				self.nodes[node] = terrain
				self.terrain.add(terrain)
			if node in self.area.features:
				feature = Feature(self, pos = (node.x * self.parent.cell, node.y * self.parent.cell))
				self.nodes[node] = feature
				self.features.add(feature)
			if node in self.area.entities:
				entity = Entity(self, pos = (node.x * self.parent.cell, node.y * self.parent.cell))
				self.nodes[node] = entity
				self.entities.add(entity)
		self.refresh()
	def refresh(self):
		self.draw(self.parent.display)
		self.parent.dirty_rects.append(self.rect)
	def draw(self, screen):
		offset = (self.focus.x - 9) * self.parent.cell, (self.focus.y - 9) * self.parent.cell
		self.image.fill(self.bcolor)
		for child in self.terrain:
			xy = child.rect.left - offset[0], child.rect.top - offset[1]
			self.image.blit(child.image, xy)
		for child in self.features:
			xy = child.rect.left - offset[0], child.rect.top - offset[1]
			self.image.blit(child.image, xy)
		for child in self.entities:
			xy = child.rect.left - offset[0], child.rect.top - offset[1]
			self.image.blit(child.image, xy)
		for child in self.children:
			xy = child.rect.left - offset[0], child.rect.top - offset[1]
			self.image.blit(child.image, xy)
		screen.blit(self.image, self.rect.topleft)	
	def key_press(self, key):
		if key == 1:
			self.handler.move_entity(self.focus,(0,-1))
		if key == 2:
			self.handler.move_entity(self.focus,(0,1))
		if key == 3:
			self.handler.move_entity(self.focus,(-1,0))
		if key == 4:
			self.handler.move_entity(self.focus,(1,0))
		self.init()
	def tick(self, focus):
		if self.focus != focus:
			self.data['focus'] = focus
			self.focus = focus
			self.init()
		if focus.fov.points != self.fov.points:
			nodes = self.area.get_nodes(focus.fov)
			if nodes != set(self.nodes):
				dead_nodes = set(self.nodes).difference(nodes)
				new_nodes = nodes.difference(set(self.nodes))



		

class Terrain(Widget):
	def init(self):
		self.rect = pygame.Rect(self.pos, self.parent.parent.cell_size)
		self.image = pygame.transform.scale(load_image('floor.bmp'),self.rect.size)
class Feature(Widget):
	def init(self):
		self.rect = pygame.Rect(self.pos, self.parent.parent.cell_size)
		self.image = pygame.transform.scale(load_image('wall.bmp'),self.rect.size)
class Entity(Widget):
	def init(self):
		self.rect = pygame.Rect(self.pos, self.parent.parent.cell_size)
		self.image = pygame.transform.scale(load_image('hero.bmp', -1),self.rect.size)
