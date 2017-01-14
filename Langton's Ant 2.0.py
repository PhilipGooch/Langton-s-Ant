import pygame
import os
import time
pygame.init()
instructions = [[0, 1, "left"], [1, 0, "right"]]
width = 1224
height = 1024
grid_width = 1024
grid_height = 1024
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (400, 70)
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Langton's Ant")
ant_icon = pygame.image.load("ant_icon.png")
pygame.display.set_icon(ant_icon)
clock = pygame.time.Clock()
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
color_squares = [pygame.image.load("white.png"), pygame.image.load("red.png"), pygame.image.load("green.png"), pygame.image.load("blue.png")]
arrows = pygame.image.load("white_left.png", "white_right.png")
window.fill(white)
pygame.display.update()
zoom = 5
exit_app = False
grid = []
for i in range(grid_width):
	grid.append([])
	for j in range(grid_height):
		grid[i].append(0)
ant = {"x": int(grid_width / 2), "y": int(grid_height / 2 + 1), "direction": "right"}
ant_x = int((ant["x"] - 298) * 100) + 50
ant_y = int((ant["y"] - 298) * 100) + 50
ant_grid = []
for i in range(6):
	ant_grid.append([])
	for j in range(6):
		ant_grid[i].append(0)


def ant_AI(zoom):
	detect_edge = False
	direction = ant["direction"]
	if direction == "right":
		ant["x"] += 1
	elif direction == "left":
		ant["x"] -= 1
	elif direction == "up":
		ant["y"] -= 1
	elif direction == "down":
		ant["y"] += 1
	for instruction in instructions:
		if grid[ant["x"]][ant["y"]] == instruction[0]:
			if instruction[2] == "left":
				if direction == "right":
					ant["direction"] = "up"
				elif direction == "left":
					ant["direction"] = "down"
				elif direction == "up":
					ant["direction"] = "left"
				elif direction == "down":
					ant["direction"] = "right"
			elif instruction[2] == "right":
				if direction == "right":
					ant["direction"] = "down"
				elif direction == "left":
					ant["direction"] = "up"
				elif direction == "up":
					ant["direction"] = "right"
				elif direction == "down":
					ant["direction"] = "left"
			if zoom == 5:
				if grid_width / 2 - square_size[zoom - 3] <= ant["x"] <= grid_width / 2 + square_size[zoom - 3] and \
				   grid_width / 2 - square_size[zoom - 3] <= ant["y"] <= grid_width / 2 + square_size[zoom - 3]:
					grid[ant["x"]][ant["y"]] = instruction[1]
					ant_grid[ant["x"] - 512][ant["y"] - 512] = instruction[1]
				else:
					grid[ant["x"]][ant["y"]] = instruction[1]
					detect_edge = True
			elif zoom >= 0:
				if grid_width / 2 - square_size[zoom + 1] <= ant["x"] <= grid_width / 2 + square_size[zoom + 1] and \
				   grid_width / 2 - square_size[zoom + 1] <= ant["y"] <= grid_width / 2 + square_size[zoom + 1]:
					grid[ant["x"]][ant["y"]] = instruction[1]
				else:
					grid[ant["x"]][ant["y"]] = instruction[1]
					detect_edge = True 
			break
	return detect_edge		

def display_ant(move, direction):
	if direction == "right":
		pygame.draw.circle(window, black, (ant_x + move, ant_y), 10)
	elif direction == "left":
		pygame.draw.circle(window, black, (ant_x - move, ant_y), 10)
	elif direction == "up":
		pygame.draw.circle(window, black, (ant_x, ant_y - move), 10)
	elif direction == "down":
		pygame.draw.circle(window, black, (ant_x, ant_y + move), 10)	

def resize_color_squares(color_squares, zoom):
	size = square_size[zoom - 1]
	for i in range(len(color_squares)):
		color_squares[i] = pygame.transform.smoothscale(color_squares[i], (size, size))

square_size = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]

def display(zoom, update):
	window.fill(black, (600, 0, 201, height))
	if zoom == 5:
		for i in range(0, grid_width + 1, 100):
			pygame.draw.line(window, black, (i, 0), (i, grid_height))
			pygame.draw.line(window, black, (0, i), (grid_width, i))
		for i in range(6):
			for j in range(6):
				if ant_grid[i][j] == 1:
					pygame.draw.rect(window, red, (i * 100 + 1, j * 100 + 1, 99, 99), 0)
				elif ant_grid[i][j] == 2:
					pygame.draw.rect(window, blue, (i * 100 + 1, j * 100 + 1, 99, 99), 0)
				elif ant_grid[i][j] == 3:
					pygame.draw.rect(window, green, (i * 100 + 1, j * 100 + 1, 99, 99), 0)

	elif zoom >= 0:
		if update:
			for i in range(square_size[9 - zoom + 1]):
				for j in range(square_size[9 - zoom + 1]):
					print(grid[i + square_size[9] + square_size[8 - zoom] + 1][j + square_size[9] + square_size[8 - zoom] + 1])
					window.blit(color_squares[grid[i + square_size[9] - square_size[8 - zoom] + 1][j + square_size[9] - square_size[8 - zoom] + 1]], (i * square_size[zoom] + 1, j * square_size[zoom] + 1))
		# window.blit(color_squares[grid[ant["x"]][ant["y"]]], ((ant["x"] - (square_size[10 - zoom] + square_size[9 - zoom])) * 2 + 1, ((ant["y"] - (square_size[10 - zoom] + square_size[9 - zoom])) * 2 + 1)))


start = False
move = 1
fps = 10000
resize_color_squares(color_squares, zoom)
update = True
while not exit_app:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit_app = True
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				start = True
	if zoom == 5:
		window.fill(white)
		# if start:
		move += 1
		ant_x = int((ant["x"] - 298) * 100) + 50
		ant_y = int((ant["y"] - 298) * 100) + 50
		if move < 100:
			display(zoom, update)
			display_ant(move, ant["direction"])
			pygame.display.update()
		elif move == 100:
			if ant_AI(zoom) == True:
				resize_color_squares(color_squares, zoom)
				zoom -= 1
				start = False
				fps = 10000
			move = 0
	else:
		display(zoom, update)
		if update:
			update = False
		pygame.display.update()
		if ant_AI(zoom) == True:
			window.fill(white)
			resize_color_squares(color_squares, zoom)
			zoom -= 1
			start = False
			update = True
			fps = 10000
	clock.tick(fps)
for i in range(1024):
		for j in range(1024):
			if grid[i][j] == 1:
				print("%s %s" % (i, j))
pygame.quit()
quit()







