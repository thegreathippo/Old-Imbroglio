import sys, pygame
from pygame.locals import *
from gui import *
from gamemap import GameMap

class GUIStack(object):
	def __init__(self, owner):
		self.owner = owner
		self.rect = pygame.Rect((0,0), SCREEN_SIZE)
		self.display = pygame.display.set_mode(self.rect.size)
		self.dirty_rects = []
		self.display.fill((0,0,0))
		self.cell = self.rect.size[0] / 20
		self.cell_size = self.cell, self.cell
		self.init_images()		
 		pygame.display.flip()
		self.stack = []
		self.stack.append(GameMap(self, area = self.owner.session.world[0], bcolor = (0,0,0), focus = self.owner.session.player))
		self.stack.append(Cursor(self, node = None))
		self.focus = self.owner.session.player
#		self.add(Menu(self, bcolor = (75,75,40), pos = (10,5), size = (10,10),\
#				choices = ['NEW GAME', 'LOAD GAME', 'OPTIONS'], \
#				title = 'IMBROGLIO', commands = ['new_game', 'load_game', 'options'], \
#				color = (160,160,160), hcolor = (50,50,200), descriptions = ['Start a\
#				new game', 'Load a previous game', 'Option menu for game']))
	def __iter__(self):
		return iter(reversed(self.stack))
	def __getitem__(self, index):
		return self.stack[index]
	def __call__(self, input_events):
		for event in input_events:
			if event.type == QUIT:
				sys.exit()
			if event.type == MOUSEBUTTONDOWN:
				pos, button = event.dict['pos'], event.dict['button']
				self.accept_input('mouse_click', pos, button)
			if event.type == MOUSEBUTTONUP:
				pos, button = event.dict['pos'], event.dict['button']
				self.accept_input('mouse_release', pos, button)
			if event.type == MOUSEMOTION:
				pos, rel, buttons = event.dict['pos'], event.dict['rel'], event.dict['buttons']
				self.accept_input('mouse_move', pos, rel, buttons)
			if event.type == KEYDOWN:
				if event.dict['key'] == 303 or event.dict['key'] == 304:
					self.accept_input('shift_press')
				if event.dict['key'] == 306 or event.dict['key'] == 305:
					self.accept_input('ctrl_press')
				if event.dict['key'] in DEFAULT_KEYS:
					key = event.dict['key']
					self.accept_input('key_press', DEFAULT_KEYS[key])
			if event.type == KEYUP:
				if event.dict['key'] == 303 or event.dict['key'] == 304:
					self.accept_input('shift_release')
				if event.dict['key'] == 306 or event.dict['key'] == 305:
					self.accept_input('ctrl_release')
				if event.dict['key'] in DEFAULT_KEYS:
					key = event.dict['key']
					self.accept_input('key_release', DEFAULT_KEYS[key])
			if event.type == USEREVENT:
				self.accept_input('tick', self.focus)
	def init(self, size):
		self.rect = pygame.Rect((0,0), size)
		self.display = pygame.display.set_mode(self.rect.size)
		self.dirty_rects = []
		self.display.fill((0,0,0))
		self.cell = self.rect.size[0] / 20
		self.cell_size = self.cell, self.cell
		self.init_images()		
		pygame.display.flip()
		for gui in self.stack:
			gui.init()
		self.refresh()
	def init_images(self):
		self.images = {
			'floor' : pygame.transform.scale(load_image('floor.bmp'), self.cell_size),
			'wall' : pygame.transform.scale(load_image('wall.bmp'), self.cell_size),
			'hero' : pygame.transform.scale(load_image('hero.bmp', -1), self.cell_size),
			'monster' : pygame.transform.scale(load_image('monster.bmp', -1), self.cell_size),
			'potion' : pygame.transform.scale(load_image('potion.bmp', -1), self.cell_size),
			'chasm' : pygame.transform.scale(load_image('chasm.bmp'), self.cell_size)
				}
	def refresh(self):
		for gui in self.stack:
			gui.refresh()
	def add(self, gui):
		self.stack.insert(len(self.stack)-1, gui)
		self.refresh()
	def remove(self, gui):
		self.stack.remove(gui)
		self.refresh()
	def accept_input(self, func_name, *args):
		if func_name == 'tick':
			for state in self.stack:
				state.tick(args[0])
			return
		for state in self:
			if hasattr(state, func_name):
				func = getattr(state, func_name)
				if len(args) == 0: fired = func()
				if len(args) == 1: fired = func(args[0])
				if len(args) == 2: fired = func(args[0], args[1])
				if len(args) == 3: fired = func(args[0], args[1], args[2])
				if fired == True: break
			if state.locked == True: break	
	def draw(self):
		pygame.display.update(self.dirty_rects)
	def tick(self):
		self.draw()
		self.dirty_rects = []

class HUD(object):
	def __init__(self, owner):
		self.owner = owner
		self.owner.stack.add(Status(self.owner.stack, bcolor = (75,75,40), pos = (15,1), size = (4, 3)))
		self.owner.stack.add(TextScroll(self.owner.stack, bcolor = (75,75,40), pos = (2,17), size = (16, 2)))
#		self.owner.stack.add(Inventory(self.owner.stack, bcolor = (75,75,40), pos = (14,5), size = (5,5)))

