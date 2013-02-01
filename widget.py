from images import *
import pygame, events

DEFAULT_PROPERTIES = {
	'color' : (250,250,250),
	'bcolor' : (1,1,1),
	'locked' : False

		}


class Widget(object):
	def __init__(self, parent, **kwargs):
		self.handler = events.EventHandler()
		self.parent = parent
		self.data = kwargs
		for key in DEFAULT_PROPERTIES:
			if key not in self.data:
				self.data[key] = DEFAULT_PROPERTIES[key]
		self.reset()
	def __iter__(self):
		return iter(self.data)
	def __setitem__(self, key, value):
		self.data[key] = value
	def __getitem__(self, key):
		return self.data[key]
	def __contains__(self, key):
		return key in self.data
	def reset(self):
		for key in self:
			setattr(self, key, self[key])
		self.init()
	def overwrite(self, **kwargs):
		for key in kwargs:
			setattr(self, key, kwargs[key])
		self.init()
	def update(self, **kwargs):
		for key in kwargs:
			self[key] = kwargs[key]
		self.reset()	
	def init(self):
		self.owner = self.parent.parent
		self.rect = pygame.Rect(self.pos, self.size)
		self.image = get_surface(self.rect.size, self.bcolor)
	def draw(self, screen):
		xy = self.rect.left + self.parent.rect.left, self.rect.top + self.parent.rect.top
		screen.blit(self.image, xy)
	def translate(self, pos):
		return pos[0] - self.parent.rect.left, pos[1] - self.parent.rect.top
	def contains_point(self, pos):
		return self.rect.collidepoint(self.translate(pos))

class Label(Widget):
	def init(self):
		self.owner = self.parent.parent
		x = get_text_center_offset(self.text, self.parent.rect.width)
		self.rect = pygame.Rect((x, self.pos[1]), get_text_size(self.text))
		self.image = get_text(self.text, self.color)

class TextBox(Widget):
	def init(self):
		self.owner = self.parent.parent
		width, height = self.parent.rect.width - (self.owner.cell), self.owner.cell * 5
		self.rect = pygame.Rect(self.pos, (width, height))
		self.image = blit_text(format_lines(self.text, self.rect.size), self.color)

class Cell(Widget):
	def init(self):
		self.owner = self.parent.parent
		width, height = self.owner.cell, self.owner.cell
		self.rect = pygame.Rect(self.pos, (width, height))
		self.image = get_surface(self.rect.size, (30,30,30))
		if self.node != None:
			self.image.blit(load_image('potion.bmp', -1),(0,0))

		 		

