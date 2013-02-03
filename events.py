import random

NEUMANN = [(1,0), (-1,0), (0,1), (0,-1)]

class EventQueue(object):
	def __init__(self):
		self.game_events = []
	def apply(self):
		self.apply_game_events()
	def apply_game_events(self):
		for event in list(self.game_events):
			event.apply(self.owner)
			self.game_events.remove(event)
		if self.game_events != []:
			self.apply_game_events()

class TurnQueue(object):
	def __init__(self):
		self.order = []
		self.global_time = 0
	def __iter__(self):
		return iter(self.order)
	def sort(self):
		self.order = list(self.owner.session.world[0].entities.nodes)
		random.shuffle(self.order)
		self.order.sort(key=lambda entity: entity.time, reverse = True)
		if self.order[0].time < 0:
			self.return_time(-1 * self.order[0].time)
			self.sort()
	def return_time(self, time):
		self.global_time += time
		for entity in self.order:
			entity.time += time
	def apply(self):
		if self.order == []: self.sort()
		if self.order[0] != self.owner.stack.focus:
			while self.order[0] != self.owner.stack.focus:
				EntityTurn(self.order[0])
				self.owner.event_queue.apply()
		elif self.owner.stack[0].commands != []:
			while self.order[0] == self.owner.stack[0].focus and self.owner.stack[0].commands != []:
				self.owner.stack[0].apply_command()
				self.owner.event_queue.apply()



event_queue = EventQueue()
turn_queue = TurnQueue()

class EventHandler(object):
	def move_entity(self, entity, rel):
		MoveEntity(entity, rel)


class Event(object):
	def __init__(self, *args):
		self.owner = event_queue
		self.owner.game_events.append(self)
		self.args = args

class SpendTime(Event):
	def apply(self, game):
		entity, time = self.args[0], self.args[1]
		entity.time += -time
		game.turn_queue.sort()


class EntityTurn(Event):
	def apply(self, game):
		entity, rel = self.args[0], random.choice(NEUMANN)
		MoveEntity(entity, rel)


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
		if entity in game.stack[0].entities:
			game.stack[0].entities[entity].add_to_path(pos)
		if game.stack.focus == entity:
			SpendTime(entity, 5)
		else:
			SpendTime(entity, 4)



def init(game):
	event_queue.owner = game
	game.event_queue = event_queue
	turn_queue.owner = game
	game.turn_queue = turn_queue
	
