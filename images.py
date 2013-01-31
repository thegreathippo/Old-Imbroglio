import pygame, os
from pygame.locals import *
from config import *

pygame.init()

FONT_SIZE = CELL - (CELL / 2)
WINDOW_FONT = pygame.font.Font('PressStart2P.ttf', FONT_SIZE)

def get_surface(size, color = (1,1,1)):
	image = pygame.Surface(size)
	image.fill(color)
	image.set_colorkey((1,1,1))
	return image

def get_text(text, color = (250,250,250)):
	image = get_surface(get_text_size(text))
	image.blit(WINDOW_FONT.render(text, 0, color, (1,1,1)),(0,0))
	return image

def load_image(name, colorkey=None):
	fullname = os.path.join('data', name)
	try:
		image = pygame.image.load(fullname)
	except pygame.error, message:
		print 'Cannot load image:', name
		raise SystemExit, message
	image = image.convert()
	if colorkey is not None:
		if colorkey is -1:
			colorkey = image.get_at((0,0))
		image.set_colorkey(colorkey, RLEACCEL)
	image = pygame.transform.scale(image, CELL_SIZE)
	return image

def blit_text(ftext, color = (250,250,250)):
	image = get_surface((500,500))
	y = 0
	for element in ftext:
		line = WINDOW_FONT.render(element, 0, color, (1,1,1))
		line.set_colorkey((1,1,1))
		image.blit(line, (0,y))
		y+=WINDOW_FONT.get_linesize()
	return image

def format_lines(text, size):
	line = ""
	ftext = list()
	for word in text.split():
		if WINDOW_FONT.size(line + word + " ")[0] > size[0]:
			ftext.append(line)
			line = word + " "
		else:
			line = line + word + " "
	ftext.append(line)
	return ftext

def get_text_center_offset(text, width):
	return (width - WINDOW_FONT.size(text)[0]) / 2

def get_text_size(text):
	return WINDOW_FONT.size(text)
