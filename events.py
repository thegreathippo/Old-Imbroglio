import random

MOORE = [(1,0), (-1,0), (0,1), (0,-1), (1,1), (-1,1), (-1,-1), (1,-1)]

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
	def wait_entity(self, entity):
		WaitEntity(entity)


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
		entity, rel = self.args[0], random.choice(MOORE)
		entity.brain.observe()		
		if entity.brain.path != []:
			step = entity.brain.path[0]
			new_rel = step[0] - entity.x, step[1] - entity.y
			entity.brain.path.pop(0)
			MoveEntity(entity, new_rel)
		else:
			MoveEntity(entity, rel)

class WaitEntity(Event):
	def apply(self, game):
		entity = self.args[0]
		SpendTime(entity, 5)

class MoveEntity(Event):
	def apply(self, game):
		entity, rel = self.args[0], self.args[1]
		pos = entity.x + rel[0], entity.y + rel[1]
		if pos not in game.session.world[0].terrain:
			return
		if game.session.world[0].terrain[pos]['chasm']:
			return
		if pos in game.session.world[0].features:
			return
		if pos in game.session.world[0].entities:
			BumpEntity(entity, game.session.world[0].entities[pos])
			return
		if pos in game.stack.focus.fov and entity not in game.stack[0].entities:
			game.stack[0].add_entity_sprite(entity)
		game.session.world[0].entities[pos] = entity
		if entity in game.stack[0].entities:
			game.stack[0].entities[entity].add_to_path(pos)
			if pos not in game.stack.focus.fov:
				game.stack[0].entities[entity].add_to_path(False)
		SpendTime(entity, 5)

class BumpEntity(Event):
	def apply(self, game):
		bumper, target = self.args[0], self.args[1]
		MeleeAttack(bumper, target)

class MeleeAttack(Event):
	def apply(self, game):
		attacker, target = self.args[0], self.args[1]
		attack_roll = roll(attacker.attack.melee_to_hit)
		if attack_roll == True:
			MeleeDamage(attacker, target)
		elif attack_roll == False:
			FloatText('MISS', target, (250,250,250))
		elif attack_roll >= target.defense.reflex:
			MeleeDamage(attacker, target)
		else: 
			FloatText('MISS', target, (250,250,250))
		SpendTime(attacker, 5)

class MeleeDamage(Event):
	def apply(self, game):
		attacker, target = self.args[0], self.args[1]
		damage_roll = roll(attacker.attack.melee_damage)
		if damage_roll == True:
			target.damage += 20
			FloatText('CRITICAL!', target, (250,0,0))
		elif damage_roll == False:
			FloatText(0, target, (250,250,250))			
		elif damage_roll > target.defense.resilience:
			damage = damage_roll - target.defense.resilience
			target.damage += damage
			FloatText(-damage, target, (250,0,0))
		else:
			FloatText(0, target, (250,250,250))
		if target != game.stack.focus:
			CheckForDeath(target)

class CheckForDeath(Event):
	def apply(self, game):
		entity = self.args[0]
		if entity.damage >= entity.defense.fortitude:
			FloatText('DEAD!', entity, (250,250,0))
			EntityDeath(entity)

class EntityDeath(Event):
	def apply(self, game):
		entity = self.args[0]
		if entity in game.stack[0].entities:
			del game.stack[0].entities[entity]
		entity.die()
		game.turn_queue.sort()		

class FloatText(Event):
	def apply(self, game):
		text, entity, color = str(self.args[0]), self.args[1], self.args[2]
		if entity in game.stack[0].entities:
			game.stack[0].entities[entity].float_text(text, color)		

def roll(modifier = 0):
	result = random.randrange(1, 21)
	if result == 20: return True
	if result == 1: return False
	return result + modifier



def init(game):
	event_queue.owner = game
	game.event_queue = event_queue
	turn_queue.owner = game
	game.turn_queue = turn_queue
	
