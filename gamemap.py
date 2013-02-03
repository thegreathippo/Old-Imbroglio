from images import *
from widget import *


class GameMap(Widget):
	def init(self):
		self.commands = []
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
		self.fov = self.focus.fov.copy()
		self.build_view()
		self.refresh()
	def build_view(self):
		rects = []
		old_terrain = set(self.terrain)
		new_terrain = self.area.terrain.get_nodes(self.fov)
		new_nodes = new_terrain.difference(old_terrain)
		dead_nodes = old_terrain.difference(new_terrain)
		for node in new_nodes:
			terrain = Terrain(self, pos = (node.x * self.parent.cell, node.y * self.parent.cell), owner = node)
			self.terrain[node] = terrain
			rects.append(terrain.rect)
		for node in dead_nodes:
			rects.append(self.terrain[node].rect)
			del self.terrain[node]
		old_features = set(self.features)
		new_features = self.area.features.get_nodes(self.fov)
		new_nodes = new_features.difference(old_features)
		dead_nodes = old_features.difference(new_features)
		for node in new_nodes:
			feature = Feature(self, pos = (node.x * self.parent.cell, node.y * self.parent.cell), owner = node)
			self.features[node] = feature
			rects.append(feature.rect)
		for node in dead_nodes:
			rects.append(self.features[node].rect)
			del self.features[node]		
		old_entities = set(self.entities)
		new_entities = self.area.entities.get_nodes(self.fov)
		new_nodes = new_entities.difference(old_entities)
		dead_nodes = old_entities.difference(new_entities)
		for node in new_nodes:
			entity = Entity(self, pos = (node.x * self.parent.cell, node.y * self.parent.cell), owner = node)
			self.entities[node] = entity
			rects.append(entity.rect)
		for node in dead_nodes:
			rects.append(self.entities[node].rect)
			del self.entities[node]
		return rects	
	def refresh(self, rects = None):
		if rects is None: rects = [self.rect]
		self.draw(self.parent.display)
		self.parent.dirty_rects += rects
		for gui in self.parent.stack:
			if gui == self: continue
			if gui.rect.collidelist(rects) != -1:
				gui.refresh()
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
	def apply_command(self):
		if self.commands != []:
			if self.commands[0] == 1:
				self.handler.move_entity(self.focus,(0,-1))
			if self.commands[0] == 2:
				self.handler.move_entity(self.focus,(0,1))
			if self.commands[0] == 3:
				self.handler.move_entity(self.focus,(-1,0))
			if self.commands[0] == 4:
				self.handler.move_entity(self.focus,(1,0))
			self.commands.pop(0)
	def key_press(self, key):
		self.commands.append(key)
	def cursor_lclick(self, cursor):
		for sprite in self.terrain.values():
			if sprite.contains_point(cursor.rect.center):
				print str(sprite.owner)
	def tick(self, focus):
		camera = (self.focus.x - 9) * self.parent.cell, (self.focus.y - 9) * self.parent.cell
		refresh = False
		if self.focus != focus:
			self.data['focus'] = focus
			self.focus = focus
			self.init()
			return
		if focus.fov.points != self.fov.points:
			self.fov = focus.fov.copy()
			dirty_rects = self.build_view()
		for sprite in self.entities.values():
			if sprite.moving: refresh = True
			if sprite.follow_path() == True: refresh = True
		if self.camera != camera:
			step = get_step(camera, self.camera, self.parent.cell / 3)
			self.camera = self.camera[0] + step[0], self.camera[1] + step[1]
			refresh = True
		if self.parent.owner.turn_queue.order != []:
			while self.parent.owner.turn_queue.order[0] == self.focus and self.commands != []:
				refresh = True
				self.apply_command()
		if refresh: self.refresh()





class Terrain(Widget):
	def init(self):
		self.rect = pygame.Rect(self.pos, self.parent.parent.cell_size)
		self.image = self.parent.parent.images['floor']
	def translate(self, pos):
		return pos[0] + self.parent.camera[0], pos[1] + self.parent.camera[1]

class Feature(Widget):
	def init(self):
		self.rect = pygame.Rect(self.pos, self.parent.parent.cell_size)
		self.image = self.parent.parent.images['wall']
class Entity(Widget):
	def init(self):
		self.path = []
		self.moving = False
		self.rect = pygame.Rect(self.pos, self.parent.parent.cell_size)
		self.image = self.parent.parent.images['hero']
	def add_to_path(self, pos):
		xy = pos[0] * self.parent.parent.cell, pos[1] * self.parent.parent.cell
		self.path.append(xy)
	def follow_path(self):
		self.moving = False
		if self.path != []:
			self.moving = True
			speed = self.parent.parent.cell / 2 + len(self.path)
			step = get_step(self.path[0], self.rect.topleft, speed)
			self.rect.topleft = self.rect.left + step[0], self.rect.top + step[1]
			if self.rect.topleft == self.path[0]:
				self.path.pop(0)
			return True	


		
