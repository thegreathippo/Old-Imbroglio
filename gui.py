from widget import *



class GUI(Widget):
	def init(self):
		self.children = set()
		pos, size = (self.pos[0] * self.parent.cell, self.pos[1] * self.parent.cell), (self.size[0] * self.parent.cell, self.size[1] * self.parent.cell)
		self.rect = pygame.Rect(pos, size)
		self.image = get_surface(self.size, self.bcolor)
		self.refresh()
	def refresh(self):
		self.draw(self.parent.display)
		self.parent.dirty_rects.append(self.rect)
	def translate(self, pos):
		return pos
	def draw(self, screen):
		self.image.fill(self.bcolor)
		for child in self.children:
			self.image.blit(child.image, child.rect.topleft)
		screen.blit(self.image, self.rect.topleft)	
	def tick(self, focus):
		pass


class Cursor(GUI):
	def init(self):
		self.children = set()
		pos, size = pygame.mouse.get_pos(), self.parent.cell_size
		self.rect = pygame.Rect(pos, size)
		self.image = get_surface(self.rect.size)
	def mouse_move(self, pos, rel, buttons):
		self.rect.center = pos
		if buttons == (0,0,0):
			self.parent.accept_input('cursor_hover', self)
	def mouse_click(self, pos, button):
		if button == 1:
			self.parent.accept_input('cursor_lclick', self)
		elif button == 2:
			self.parent.accept_input('cursor_mclick', self)
		elif button == 3:
			self.parent.accept_input('cursor_rclick', self)
	def tick(self, focus):
		self.refresh()

class Status(GUI):
	def init(self):
		self.children = set()
		pos = self.pos[0] * self.parent.cell, self.pos[1] * self.parent.cell
		size = self.size[0] * self.parent.cell, self.size[1] * self.parent.cell
		self.rect = pygame.Rect(pos, size)
		self.image = get_surface(self.rect.size, self.bcolor)
		self.children.add(Label(self, pos = (0, self.parent.cell / 2), text = 'WOUNDS:', color = self.color))
		self.wounds = Label(self, pos = (0, self.parent.cell), text = str(self.parent.focus.damage), color = self.color)
		self.children.add(self.wounds)
	def refresh(self):
		self.wounds.update(text = str(self.parent.focus.damage))
		self.draw(self.parent.display)
		self.parent.dirty_rects.append(self.rect)

class TextScroll(GUI):
	def init(self):
		self.children = set()
		pos = self.pos[0] * self.parent.cell, self.pos[1] * self.parent.cell
		size = self.size[0] * self.parent.cell, self.size[1] * self.parent.cell
		self.rect = pygame.Rect(pos, size)
		self.image = get_surface(self.rect.size, self.bcolor)

class Inventory(GUI):
	def init(self):
		self.children = set()
		graph = self.parent.focus.inventory
		offset = graph.rect.width + 1, graph.rect.height + 1
		for slot in graph:
			xy = slot[0] * self.parent.cell + (slot[0] + 1), slot[1] * self.parent.cell + (slot[1] + 1)
			cell = Cell(self, pos = xy, node = self.parent.focus.inventory[slot])
			self.children.add(cell)
		size = graph.rect.width * self.parent.cell + offset[0], graph.rect.height * self.parent.cell + offset[1]
		pos = self.pos[0] * self.parent.cell, self.pos[1] * self.parent.cell
		self.rect = pygame.Rect(pos, size)
		self.image = get_surface(self.rect.size, self.bcolor)
		self.refresh()
	def cursor_lclick(self, cursor):
		if self.contains_point(cursor.rect.center) == False: return
		for child in self.children:
			if child.contains_point(cursor.rect.center): 
				if cursor.node != None and child.node == None:
					child['node'] = cursor.node
					cursor['node'] = None
					child.reset()
					cursor.reset()
					self.parent.refresh()
				elif cursor.node == None and child.node != None:
					cursor['node'] = child['node']
					child['node'] = None
					child.reset()
					cursor.reset()
					self.parent.refresh()
		return True
		
class Menu(GUI):
	def init(self):
		self.children = set()
		pos = self.pos[0] * self.parent.cell, self.pos[1] * self.parent.cell
		size = self.size[0] * self.parent.cell, self.size[1] * self.parent.cell
		self.rect = pygame.Rect(pos, size)
		self.image = get_surface(self.rect.size, self.bcolor)
		self.selected, self.choices, y = 0, [], self.parent.cell
		if 'title' in self:
			self.children.add(Label(self, pos = (0, self.parent.cell), text = self.title, color = self.color))
			y += self.parent.cell * 2	
		for choice in self['choices']:
			self.choices.append(Label(self, pos = (0, y), text = choice, color = self.color))
			y += self.parent.cell
		if 'descriptions' in self:
			self.description = TextBox(self, pos = (self.parent.cell, y + self.parent.cell), text = "", color = self.color)
			self.children.add(self.description)
		self.children.update(self.choices)
		self.refresh()
	def refresh(self):
		self.draw(self.parent.display)
		self.parent.dirty_rects.append(self.rect)
		hchoice = self.choices[self.selected]
		hchoice.overwrite(color = self.hcolor)
		if hasattr(self, 'description'):
			self.description.overwrite(text = self['descriptions'][self.selected])
		self.draw(self.parent.display)
	def key_press(self, key):
		if key==2 or key==4:
			self.choices[self.selected].reset()
			if self.selected == len(self.choices) - 1: self.selected = 0
			else: self.selected += 1
		elif key==1 or key==3:
			self.choices[self.selected].reset()
			if self.selected == 0: self.selected = len(self.choices) - 1
			else: self.selected -= 1
		elif key==9:
			return self.select()
		self.refresh()
		return True
	def cursor_hover(self, cursor):
		if self.contains_point(cursor.rect.center) == False: return
		if self.choices[self.selected].contains_point(cursor.rect.center): return
		for choice in self.choices:
			if choice.contains_point(cursor.rect.center):
				self.choices[self.selected].reset()
				self.selected = self.choices.index(choice)
				self.refresh()
				break
	def cursor_lclick(self, cursor):
		if self.contains_point(cursor.rect.center) == False: return
		if self.choices[self.selected].contains_point(cursor.rect.center) == False: return
		return self.select()
	def select(self):
		self.parent.remove(self)
		return True
