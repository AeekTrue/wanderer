import pygame.event

import window
import utils


class EventHandler:
	way = [0, 0]
	# arrows = {
	# 	BTN_UP: False,
	# 	BTN_DOWN: False,
	# 	BTN_LEFT: False,
	# 	BTN_RIGHT: False
	# }

	def __init__(self, fd=window.Field):
		self.field = fd

	# def handle(self, event: pygame.event.Event):
	# 	if event.type == pygame.KEYDOWN:
	# 		self.arrows[event.key] = True
	# 		if event.key == BTN_UP:
	# 			self.way[1] = -1
	# 		elif event.key == BTN_DOWN:
	# 			self.way[1] = 1
	# 		elif event.key == BTN_LEFT:
	# 			self.way[0] = -1
	# 		elif event.key == BTN_RIGHT:
	# 			self.way[0] = 1
	#
	# 	elif event.type == pygame.KEYUP:
	# 		self.arrows[event.key] = False
	# 		if event.key == BTN_UP:
	# 			self.way[1] = 1 if self.arrows[BTN_DOWN] else 0
	# 		elif event.key == BTN_DOWN:
	# 			self.way[1] = -1 if self.arrows[BTN_UP] else 0
	# 		elif event.key == BTN_LEFT:
	# 			self.way[0] = 1 if self.arrows[BTN_RIGHT] else 0
	# 		elif event.key == BTN_RIGHT:
	# 			self.way[0] = -1 if self.arrows[BTN_LEFT] else 0

	def mouse_position_handler(self):
		pass
