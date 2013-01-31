from events import event_queue
from images import *
import pygame

class GUIHandler(object):
	def draw_widget(self, widget):
		DrawWidget(widget)
	def send_cursor_input(self, command, cursor):
		SendCursorInput(command, cursor)
	def accept_command(self, state, command):
		AcceptCommand(state, command)

class GUIEvent(object):
	def __init__(self, *args):
		self.owner = event_queue
		self.owner.gui_events.append(self)
		self.args = args

		
class DrawWidget(GUIEvent):
	def apply(self, game):
		widget = self.args[0]
		widget.draw(game.stack.display)
		game.stack.dirty_rects.append(pygame.Rect(widget.topleft, widget.size))

class SendCursorInput(GUIEvent):
	def apply(self, game):
		command, cursor = self.args[0], self.args[1]
		game.stack.accept_input(command, cursor)

class AcceptCommand(GUIEvent):
	def apply(self, game):
		gui, command = self.args[0], self.args[1]
		if command == 'new_game':
			game.stack.remove(gui)
			game.stack.add_menu((0,0), game.screen.size, bcolor = (0,0,40), \
				choices = ['TUTORIAL', 'EASY', 'HARD'], title = 'DIFFICULTY',\
				commands = ['tutorial', 'easy', 'hard'], color = (160,160,160),\
				hcolor = (50,50,200), descriptions = ["For players who are new \
				to roguelikes, just want to fool around, or would like to \
				explore without serious risk (no PermaDeath)", "For players who \
				are somewhat familiar with roguelikes, but don't enjoy PermaDeath\
				(no PermaDeath)", "For average to veteran roguelike players \
				(PermaDeath)"])
		elif command == 'load_game':
			pass
		elif command == 'options':
			pass	
		elif command == 'tutorial':
			print 'tutorial!'
