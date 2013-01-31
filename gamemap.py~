from images import *
from widget import *


class GameMap(Widget):
	def init(self):
		self.children = set()
		self.terrain = {}
		self.features = {}
		self.entities = {}
		self.rect = pygame.Rect((0,0), self.parent.rect.size)
		self.image = get_surface(self.rect.size, self.bcolor)
		if 'focus' not in self:
			self.focus = self.parent.focus
		self.camera = (self.focus.x - 9) * self.parent.cell, (self.focus.y - 9) * self.parent.cell
		self.focus.set_fov(self.area.fov_mask)
		self.fov = self.focus.fov
		self.build_view()
		self.refresh()
	def build_view(self):
		old_terrain = set(self.terrain)
		new_terrain = self.area.terrain.get_nodes(self.fov)
		new_nodes = new_terrain.difference(old_terrain)
		dead_nodes = old_terrain.difference(new_terrain)
		for node in new_nodes:
			terrain = Terrain(self, pos = (node.x * self.parent.cell, node.y * self.parent.cell))
			self.terrain[node] = terrain
		for node in dead_nodes:
			del self.terrain[node]
		old_features = set(self.features)
		new_features = self.area.features.get_nodes(self.fov)
		new_nodes = new_features.difference(old_features)
		dead_nodes = old_features.difference(new_features)
		for node in new_nodes:
			feature = Feature(self, pos = (node.x * self.parent.cell, node.y * self.parent.cell))
			self.features[node] = feature
		for node in dead_nodes:
			del self.features[node]		
		old_entities = set(self.entities)
		new_entities = self.area.entities.get_nodes(self.fov)
		new_nodes = new_entities.difference(old_entities)
		dead_nodes = old_entities.difference(new_entities)
		for node in new_nodes:
			entity = Entity(self, pos = (node.x * self.parent.cell, node.y * self.parent.cell))
			self.entities[node] = entity
		for node in dead_nodes:
			del self.entities[node]
	def refresh(self):
		self.draw(self.parent.display)
		self.parent.dirty_rects.append(self.rect)
	def draw(self, screen):
		self.image.fill(self.bcolor)
		for child in self.terrain.values():
			xy = child.rect.left - self.camera[0], child.rect.top - self.camera[1]
			self.image.blit(child.image, xy)
		for child in self.features.values():
			xy = child.rect.left - self.camera[0], child.rect.top - self.camera[1]
			self.image.blit(child.image, xy)
		for child in self.entities.values():
			xy = child.rect.left - self.camera[0], child.rect.top - self.camera[1]
			self.image.blit(child.image, xy)
		for child in self.children:
			xy = child.rect.left - self.camera[0], child.rect.top - self.camera[1]
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
	def tick(self, focus):
		if self.focus != focus:
			self.data['focus'] = focus
			self.focus = focus
			self.init()
			return
		if focus.fov.points != self.fov.points:
			self.fov = focus.fov
			self.build_view()
			self.refresh()
			return
		sprite_move = False
		for sprite in self.entities.values():
			if sprite.path != []:
				sprite_move = True
				speed = (self.parent.cell / 3) + (len(sprite.path) * 3)
				step = get_step(sprite.path[0], sprite.rect.topleft, speed)
				sprite.rect.topleft = sprite.rect.left + step[0], sprite.rect.top + step[1]
				if sprite.rect.topleft == sprite.path[0]:
					sprite.path.pop(0)
		camera = (self.focus.x - 9) * self.parent.cell, (self.focus.y - 9) * self.parent.cell
		if self.camera != camera:
			step = get_step(camera, self.camera, self.parent.cell / 3)
			self.camera = self.camera[0] + step[0], self.camera[1] + step[1]
			self.refresh()
			return
		if sprite_move: self.refresh()
								






		

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
		self.path = []
		self.rect = pygame.Rect(self.pos, self.parent.parent.cell_size)
		self.image = pygame.transform.scale(load_image('hero.bmp', -1),self.rect.size)
	def move(self, pos):
		xy = pos[0] * self.parent.parent.cell, pos[1] * self.parent.parent.cell
		self.path.append(xy)


		
