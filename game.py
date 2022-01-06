from enum import Enum

import pygame.event
import colors
import window
from client import client
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, RPS


class Windows(Enum):
	main_menu = 0
	field = 1


class Game:
	def __init__(self):
		self.__is_running = False
		self.current_window = Windows.main_menu
		self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		pygame.display.set_caption("Wanderer - designed by Aeek True")
		self.clock = pygame.time.Clock()
		self.font = pygame.font.Font(None, 64)
		self.windows = {
			Windows.main_menu: window.MainMenu(self, None),
			Windows.field: window.Field(self, Windows.main_menu),
		}

	def run(self):
		self.__is_running = True
		frames_cnt = 0
		while self.is_running():
			for event in pygame.event.get():
				self.handle(event)

			if frames_cnt % (FPS // RPS) == 0:
				response = client.data_exchange()
				print("Response:", response)
				frames_cnt = 0
			self.update()

			self.draw()
			pygame.display.update()
			self.screen.fill(colors.BACKGROUND)
			self.clock.tick(FPS)
			frames_cnt += 1
		pygame.quit()

	def update(self):
		self.windows[self.current_window].update()

	def draw(self):
		self.windows[self.current_window].draw()
		fps = f"FPS {round(self.clock.get_fps())}"
		debug = self.font.render(fps, False, colors.BLUE)
		debug_rect = debug.get_rect()
		debug_rect.topright = self.screen.get_rect().topright
		self.screen.blit(debug, debug_rect)

	def handle(self, event: pygame.event.Event):
		if event.type == pygame.QUIT:
			self.close()
		else:
			self.windows[self.current_window].handle(event)

	def change_window(self, window_index: Windows):
		if window_index is None:
			self.close()
		else:
			self.current_window = window_index

	def close(self):
		self.__is_running = False

	def is_closed(self):
		return not self.__is_running

	def is_running(self):
		return self.__is_running
