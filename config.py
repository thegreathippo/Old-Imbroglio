SCREEN_SIZE = (500, 500)
CELL = SCREEN_SIZE[0] / 20
CELL_SIZE = CELL, CELL
MAX_MAP_SIZE = (200, 200)

#basic key-code: 
#0 : None
#1 : NORTH
#2 : SOUTH
#3 : WEST
#4 : EAST
#5 : NW
#6 : NE
#7 : SW
#8 : SE
#9 : enter

NORTH = ( 0,-1)
SOUTH = ( 0, 1)
WEST = (-1, 0)
EAST = ( 1, 0)
NORTHWEST = (-1,-1)
NORTHEAST = ( 1,-1)
SOUTHWEST = (-1, 1)
SOUTHEAST = ( 1, 1)
ENTER = 1

DEFAULT_KEYS = {
	264 : 1,
	258 : 2,
	260 : 3,
	262 : 4,
	263 : 5,
	265 : 6,
	257 : 7,
	259 : 8,
	273 : 1,
	274 : 2,
	276 : 3,
	275 : 4,
	13 : 9,
	271 : 9,
	32 : 9
}

COMMANDS = { 
	1 : NORTH,
	2 : SOUTH,
	3 : WEST,
	4 : EAST,
	5 : NORTHWEST,
	6 : NORTHEAST,
	7 : SOUTHWEST,
	8 : SOUTHEAST,
	9 : ENTER
	}

