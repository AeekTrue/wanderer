import random

import pygame
import pygame.sprite

import colors
import game
import objects
import utils
from objects import Hero, Camera
from utils import min_abs


class Window:
	def __init__(self, program, parent_index):
		self.__program = program
		self.__parent = parent_index
		self.surface = program.screen
		self.rect = self.surface.get_rect()
		self.font = pygame.font.Font(None, 36)

	def update(self):
		pass

	def draw(self):
		pass

	def handle(self, event: pygame.event.Event):
		pass

	def close(self):
		self.__program.change_window(self.__parent)

	def open_window(self, window_index):
		self.__program.change_window(window_index)


class Field(Window):
	def __init__(self, program, parent):
		super(Field, self).__init__(program, parent)
		self.width = 2000
		self.height = 2000
		self.size = (self.width, self.height)
		self.sprites = pygame.sprite.Group()
		self.others = pygame.sprite.Group()
		self.humans = pygame.sprite.Group()
		self.bullets = pygame.sprite.Group()
		self.trees = pygame.sprite.Group()
		self.ui = pygame.sprite.Group()

		self.__hero = Hero(self)
		self.camera = Camera(self.__hero)
		self.spawn_hero(self.__hero)

		for i in range(10):
			tree = gen_tree(self)
			self.sprites.add(tree)
			self.others.add(tree)
			self.trees.add(tree)
		for i in range(10):
			x = random.randint(0, self.width)
			y = random.randint(0, self.height)
			human = objects.Human(utils.Point(x, y), self)
			self.spawn_human(human)

	def update(self):
		self.sprites.update()
		self.ui.update()
		self.camera.update()
		hits = pygame.sprite.groupcollide(self.humans, self.bullets, False, True)
		for human in hits:
			for bullet in hits[human]:
				human.make_damage(bullet)
		pygame.sprite.groupcollide(self.trees, self.bullets, False, True)

	def draw(self):
		self.surface.fill(colors.GRASS)
		# self.sprites.draw(self.screen)
		self.camera.draw_sprites(self.surface, self.sprites)
		self.ui.draw(self.surface)
		self.draw_debug_info()

	def get_window_center(self):
		window_size = self.surface.get_size()
		return utils.Point(window_size[0] // 2, window_size[1] // 2)

	def shortest_way(self, a: utils.Point, b: utils.Point):
		dx = min_abs(b.x + self.width - a.x, b.x - a.x, b.x - self.width - a.x)
		dy = min_abs(b.y + self.height - a.y, b.y - a.y, b.y - self.height - a.y)
		return utils.Vector(dx, dy)

	def calc_relative_position(self, point: utils.Point) -> utils.Point:
		center = self.get_window_center()
		hero_pos = self.__hero.get_position()
		rel_pos = self.shortest_way(hero_pos, point)
		return center + rel_pos

	def check_intersection(self, pos: utils.Point):
		possible_hero = objects.Human(pos, self)
		possible_hero.update()
		return len(pygame.sprite.spritecollide(possible_hero, self.others, False))

	def spawn_human(self, human: objects.Human):
		self.sprites.add(human)
		self.humans.add(human)
		self.others.add(human)
		health_bar = objects.HealthBar(human)
		self.ui.add(health_bar)

	def spawn_hero(self, hero: Hero):
		self.sprites.add(hero)
		health_bar = objects.HeroHealthBar(hero, self.camera)
		self.ui.add(health_bar)

	def handle(self, event: pygame.event.Event):
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == pygame.BUTTON_LEFT:
				self.__hero.shot()
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_ESCAPE:
				self.close()

	def draw_debug_info(self):
		debug_text = self.font.render(f"{self.__hero.pos.get()}", True, colors.WHITE)
		self.surface.blit(debug_text, (0, 0))


def gen_tree(fd: Field):
	x = random.randint(40, fd.width - 40)
	y = random.randint(40, fd.height - 40)
	return objects.Tree(utils.Point(x, y), fd)


class MainMenu(Window):
	def draw(self):
		self.surface.fill(colors.BACKGROUND)
		greeting = self.font.render("Hello! Press [S] to start!", True, colors.WHITE)
		greeting_rect = greeting.get_rect()
		greeting_rect.center = self.rect.center
		self.surface.blit(greeting, greeting_rect)

		creator = self.font.render("Designed by Aeek True. Powered by Pygame.", True, colors.GRAY100)
		creator_rect = creator.get_rect()
		creator_rect.bottomleft = self.rect.bottomleft
		self.surface.blit(creator, creator_rect)

	def handle(self, event: pygame.event.Event):
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_s:
				self.open_window(game.Windows.field)