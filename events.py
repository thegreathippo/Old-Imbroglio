class EventQueue(object):
	def __init__(self):
		self.game_events = []
		self.gui_events = []
	def apply(self):
		self.apply_gui_events()
		self.apply_game_events()
	def apply_gui_events(self):
		for event in list(self.gui_events):
			event.apply(self.owner)
			self.gui_events.remove(event)
		if self.gui_events != []:
			self.apply_gui_events()
	def apply_game_events(self):
		for event in list(self.game_events):
			event.apply(self.owner)
			self.game_events.remove(event)
		if self.game_events != []:
			self.apply_game_events()

event_queue = EventQueue()

class EventHandler(object):
	def move_entity(self, entity, rel):
		MoveEntity(entity, rel)
	

class Event(object):
	def __init__(self, *args):
		self.owner = event_queue
		self.owner.gui_events.append(self)
		self.args = args

class CalculateFov(Event):
	def apply(self, game):
		obj = self.args[0]
		obj.set_fov(game.session.world[0].fov_mask)

class MoveEntity(Event):
	def apply(self, game):
		entity, rel = self.args[0], self.args[1]
		pos = entity.x + rel[0], entity.y + rel[1]
		if pos not in game.session.world[0].terrain:
			return
		if pos in game.session.world[0].features:
			return
		if pos in game.session.world[0].entities:
			return
		game.session.world[0].entities[pos] = entity 
		CalculateFov(entity)


def init(game):
	event_queue.owner = game
	game.event_queue = event_queue	
