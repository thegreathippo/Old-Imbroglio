D_ABILITIES = {
		'strength' : 10,
		'base_strength' : 10,
		'constitution' : 10,
		'base_constitution' : 10,
		'dexterity' : 10,
		'base_dexterity' : 10,
		'intelligence' : 10,
		'base_intelligence' : 10,
		'wisdom' : 10,
		'base_wisdom' : 10,
		'charisma' : 10,
		'base_charisma' : 10
		}

class Abilities(object):
	def __init__(self, owner, abilities = None):
		if abilities is None: abilities = {}
		self.owner = owner
		for key in D_ABILITIES:
			if key not in abilities: abilities[key] = D_ABILITIES[key]
		self.set_abilities(dict(abilities))
	def set_abilities(self, abilities):
		for key in abilities:
			setattr(self, key, abilities[key])

class Modifiers(object):
	def __init__(self, owner):
		self.owner = owner
	def calculate(self, value):
		return (int(value) / 2) - 5
	def __get_str_mod(self):
		return self.calculate(self.owner.ability.strength)
	def __get_base_str_mod(self):
		return self.calculate(self.owner.ability.base_strength)
	def __get_dex_mod(self):
		return self.calculate(self.owner.ability.dexterity)
	def __get_base_dex_mod(self):
		return self.calculate(self.owner.ability.base_dexterity)
	def __get_con_mod(self):
		return self.calculate(self.owner.ability.constitution)
	def __get_base_con_mod(self):
		return self.calculate(self.owner.ability.base_constitution)
	def __get_int_mod(self):
		return self.calculate(self.owner.ability.intelligence)
	def __get_base_int_mod(self):
		return self.calculate(self.owner.ability.base_intelligence)
	def __get_wis_mod(self):
		return self.calculate(self.owner.ability.wisdom)
	def __get_base_wis_mod(self):
		return self.calculate(self.owner.ability.base_wisdom)	
	def __get_cha_mod(self):
		return self.calculate(self.owner.ability.charisma)
	def __get_base_cha_mod(self):
		return self.calculate(self.owner.ability.base_charisma)		
	strength = property(__get_str_mod, None, None, "gets strength mod of EntityNode")
	base_strength = property(__get_base_str_mod, None, None, "gets base strength mod of EntityNode")
	dexterity = property(__get_dex_mod, None, None, "gets dexterity mod of EntityNode")
	base_dexterity = property(__get_base_dex_mod, None, None, "gets base dexterity mod of EntityNode")
	constitution = property(__get_con_mod, None, None, "gets constitution mod of EntityNode")
	base_constitution = property(__get_base_con_mod, "gets base constitution mod of EntityNode")
	intelligence = property(__get_int_mod, None, None, "gets intelligence mod of EntityNode")
	base_intelligence = property(__get_base_int_mod, None, None, "gets base intelligence mod of EntityNode")
	wisdom = property(__get_wis_mod, None, None, "gets wisdom mod of EntityNode")
	base_wisdom = property(__get_base_wis_mod, None, None, "gets base wisdom mod of EntityNode")
	charisma = property(__get_cha_mod, None, None, "gets charisma mod of EntityNode")	
	base_charisma = property(__get_base_cha_mod, None, None, "gets base charisma mod of EntityNode")

class Defenses(object):
	def __init__(self, owner):
		self.owner = owner
	def __get_fortitude(self):
		if self.owner.modifier.strength > self.owner.modifier.constitution:
			modifier = self.owner.modifier.strength
		else:
			modifier = self.owner.modifier.constitution
		return 10 + modifier
	def __get_reflex(self):
		if self.owner.modifier.intelligence > self.owner.modifier.dexterity:
			modifier = self.owner.modifier.intelligence
		else:
			modifier = self.owner.modifier.dexterity
		return 10 + modifier
	def __get_will(self):
		if self.owner.modifier.charisma > self.owner.modifier.wisdom:
			modifier = self.owner.modifier.charisma
		else:
			modifier = self.owner.modifier.wisdom
		return 10 + modifier	
	def __get_resilience(self):
		return self.fortitude
	fortitude = property(__get_fortitude, None, None, "gets fortitude defense of EntityNode")
	reflex = property(__get_reflex, None, None, "gets reflex defense of EntityNode")
	will = property(__get_will, None, None, "gets will defense of EntityNode")
	resilience = property(__get_resilience, None, None, "gets resilience defense of EntityNode")

class Attacks(object):
	def __init__(self, owner):
		self.owner = owner
	def __get_melee_to_hit(self):
		return self.owner.modifier.strength
	def __get_range_to_hit(self):
		return self.owner.modifier.dexterity
	def __get_melee_damage(self):
		return self.owner.modifier.strength
	def __get_range_damage(self):
		return self.owner.modifier.dexterity
	melee_to_hit = property(__get_melee_to_hit, None, None, "gets melee to hit modifier of EntityNode")
	range_to_hit = property(__get_range_to_hit, None, None, "gets range to hit modifier of EntityNode")
	melee_damage = property(__get_melee_damage, None, None, "gets melee damage modifier of EntityNode")
	range_damage = property(__get_range_damage, None, None, "gets range damage modifier of EntityNode")


