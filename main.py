### Author: Max Zangs
### Description: Plays the game of life
### Category: Games
### License: MIT
### Appname: Game of Life
### Built-in: no

import pyb
import ugfx
import buttons
import dialogs

ugfx.init()
buttons.init()
buttons.disable_menu_reset()

w, h, s = 40, 30, 8
grid = [[False for x in range(w)] for y in range(h)]
grid_next = [[False for x in range(w)] for y in range(h)]

def get_color(is_on):
	"""Pass binary value for colur"""
	val = 0
	if is_on:
		val = 31
	return ((val & 0x1f) << 11) | ((val & 0x1f) << 6) | (val & 0x1f)

def draw_grid():
	"""Draws the grid on screen"""
	for x in range(w):
		for y in range(h):
			ugfx.area(x*s, y*s, s, s, get_color(grid[y][x]))

def clear_grid():
	for y in range(h):
		for x in range(w):
			grid[y][x] = False

def random_grid():
	"""Generates a new random grid"""
	for x in range(w):
		for y in range(h):
			grid[y][x] = int(pyb.rng() & 0x01) == 1

def put_blinker(x, y):
	"""Adds a blinker"""
	clear_grid()
	grid[y][x-1:x+2:] = [True, True, True]

def put_clock(x, y):
	"""Adds a clock"""
	clear_grid()
	grid[y-2][x-2:x+2] = [False, True,  False, False]
	grid[y-1][x-2:x+2] = [False, True,  False, True]
	grid[y][x-2:x+2]   = [True,  False, True,  False]
	grid[y+1][x-2:x+2] = [False, False, True,  False]

def put_bipole(x, y):
	"""Adds a bipole"""
	clear_grid()
	grid[y-2][x-2:x+2] = [False, True,  False, False]
	grid[y-1][x-2:x+2] = [False, True,  True,  False]
	grid[y][x-2:x+2]   = [False, True,  True,  False]
	grid[y+1][x-2:x+2] = [False, False, True,  False]

def put_tripole(x, y):
	"""Adds a tripole"""
	clear_grid()
	grid[y-2][x-2:x+3] = [True,  True,  False, False, False]
	grid[y-1][x-2:x+3] = [True,  False, True,  False, False]
	grid[y][x-2:x+3]   = [False, False, False, False, False]
	grid[y+1][x-2:x+3] = [False, False, True,  False, True]
	grid[y+2][x-2:x+3] = [False, False, False, True,  True]

def surrounding(x, y):
	"""Counts the number of surrounding blocks"""

	ans = 0
	ans += sum(grid[y-1][x-1:x+2])
	ans += sum(grid[y][x-1:x+2]) - int(grid[y][x])
	if y >= h-1:
		ans += sum(grid[0][x-1:x+2])
	else:
		ans += sum(grid[y+1][x-1:x+2])

	return ans

def update():
	for y in range(h):
		for x in range(w):
			count = surrounding(x, y)
			if grid[y][x]:
				grid_next[y][x] = count > 1 and count < 4
			else:
				grid_next[y][x] = count == 3
	for y in range(h):
		for x in range(w):
			grid[y][x] = grid_next[y][x]


## Running the main code

playing = dialogs.prompt_boolean("""
button A\t: next step
button B\t: run/pause
joystick\t: resets the game
menu\t: quits app
Shall we play a game professor Falken?
""", title='Conway\'s Game of Life', true_text="Play", false_text="Quit")

random_grid()
draw_grid()


running = False

while playing:
	while True:
		# pyb.wfi() # Some low power stuff
		if buttons.is_triggered('BTN_A'):
			update()
			draw_grid()

		if buttons.is_triggered('BTN_B'):
			running = not running

		if buttons.is_triggered('JOY_CENTER'):
			running = False
			random_grid()
			draw_grid()

		if running:
			update()
			draw_grid()
			ugfx.text(15, 15, 'Runnig...', ugfx.YELLOW)
		else:
			ugfx.text(15, 15, 'Paused...', ugfx.YELLOW)

		if buttons.is_triggered('BTN_MENU'):
			playing = False #pyb.hard_reset()
			break
