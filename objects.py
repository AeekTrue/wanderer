import math
from typing import List

import pygame
import pygame.draw

import colors
import config
import images
import utils
import client
from config import BTN_LEFT, BTN_RIGHT, BTN_UP, BTN_DOWN

HUMAN_SIZE = (40, 40)
HUMAN_SPEED = 3
HUMAN_HEALTH = 100
GUN_DAMAGE = 30
BULLET_SPEED = 10
FIRING_RANGE = 400
BULLET_SIZE = (10, 10)

HERO_SPEED = HUMAN_SPEED
HERO_SPEED_FAST = 2 * HERO_SPEED
HERO_SIZE = (20, 20)


class Obj(pygame.sprite.Sprite):
	def __init__(self, position: utils.Point, parent_field, image=None, size=None):
		super(Obj, self).__init__()
		if image is None:
			self.image = pygame.Surface(size)
		else:
			self.image = image
		self.image.set_colorkey(colors.BLACK)
		self.rect = self.image.get_rect()
		self.pos = position
		self.field = parent_field

	def update(self):
		self.rect.center = self.field.calc_relative_position(self.pos).get()

	def get_position(self):
		return self.pos


class Tree(Obj):
	def __init__(self, position, fd):
		super(Tree, self).__init__(position, parent_field=fd, image=images.small_tree)

	def update(self):
		super(Tree, self).update()


class Bullet(Obj):
	def __init__(self, position, speed: utils.Vector, max_distance, damage, parent_field):
		radius = BULLET_SIZE[0] // 2
		super(Bullet, self).__init__(position, size=BULLET_SIZE, parent_field=parent_field)
		pygame.draw.circle(self.image, colors.BULLET, (radius, radius), radius)
		self.damage = damage
		self.speed = speed
		self.spawn_pos = position
		self.max_distance = max_distance

	def update(self):
		super(Bullet, self).update()
		self.move()
		current = self.get_position()
		difference = self.field.shortest_way(self.spawn_pos, current)
		if difference.get_length() > self.max_distance:
			self.kill()

	def move(self):
		self.pos += self.speed
		self.pos.x %= self.field.height
		self.pos.y %= self.field.width


class Human(Obj):
	def __init__(self, position, fd, image=None):
		radius = HUMAN_SIZE[0] // 2
		super(Human, self).__init__(position, size=HUMAN_SIZE, parent_field=fd, image=image)
		if image is None:
			pygame.draw.circle(self.image, colors.HUMAN, (radius, radius), radius)
		self.rotation = utils.Vector(0, 1)
		self.speed = HUMAN_SPEED
		self.gun = Gun(self)
		self.max_health = HUMAN_HEALTH
		self.health = self.max_health

	def set_rotation(self, new_rotation: utils.Vector):
		self.rotation = new_rotation

	def move(self, direction: utils.Vector):
		self.pos += direction.length(self.speed)
		self.pos.x %= self.field.width
		self.pos.y %= self.field.height

	def update(self):
		super(Human, self).update()

	def make_damage(self, bullet: Bullet):
		self.health -= bullet.damage
		if self.health <= 0:
			self.kill()

	def get_health(self):
		return self.health


class Hero(Human):
	def __init__(self, fd):
		super(Hero, self).__init__(utils.Point(fd.width // 2, fd.height // 2), fd, image=images.hero)
		self.rect.center = self.field.get_window_center().get()
		self.rotation = utils.Vector(0, 1)
		self.speed = HERO_SPEED

	def update(self):
		self.set_rotation()
		self.move()

	def set_rotation(self, *args):
		center = self.field.get_window_center()
		mouse_pos = utils.Point(*pygame.mouse.get_pos())
		self.rotation = mouse_pos - center

	def move(self, *args):
		key_state = pygame.key.get_pressed()
		key_mods = pygame.key.get_mods()
		direction = utils.Vector(0, 0)
		if key_state[BTN_LEFT]:
			direction.x += -1
		if key_state[BTN_RIGHT]:
			direction.x += 1
		if key_state[BTN_UP]:
			direction.y += -1
		if key_state[BTN_DOWN]:
			direction.y += 1

		if direction.get_length() > 0:
			self.speed = HERO_SPEED_FAST if key_mods & pygame.KMOD_SHIFT else HERO_SPEED

			client.client.write_data(direction, self.speed)

			direction.set_length(self.speed)
			next_pos = self.pos + direction
			next_pos.x %= self.field.height
			next_pos.y %= self.field.width

			is_inter = self.field.check_intersection(next_pos)
			if not is_inter:
				self.pos = next_pos

	def shot(self):
		self.gun.shot()


class Gun:
	def __init__(self, holder: Human):
		self.damage = GUN_DAMAGE
		self.holder = holder
		self.bullet_speed = BULLET_SPEED
		self.firing_range = FIRING_RANGE

	def shot(self):
		vector = self.holder.rotation.length(self.bullet_speed)
		bullet = Bullet(self.holder.pos, vector, self.firing_range, self.damage, self.holder.field)
		# client.client.write_data(vector, self.firing_range, se)
		self.holder.field.bullets.add(bullet)
		self.holder.field.sprites.add(bullet)


def relative_rect(actor, camera):
	return pygame.Rect(actor.rect.x - camera.rect.x, actor.rect.y - camera.rect.y, actor.rect.w, actor.rect.h)


class Camera:

	def __init__(self, hero: Hero):
		self.hero = hero
		self.rect = pygame.display.get_surface().get_rect()
		self.rect.center = hero.rect.center

	def update(self):
		self.rect.center = self.hero.rect.center

	def draw_sprites(self, surf, sprites: pygame.sprite.Group):
		for s in sprites:
			if s.rect.colliderect(self.rect):
				surf.blit(s.image, relative_rect(s, self))


class ProgressBar(pygame.sprite.Sprite):
	length = 100
	height = 10

	def __init__(self):
		super(ProgressBar, self).__init__()
		self.image = pygame.Surface((self.length, self.height))
		self.rect = self.image.get_rect()

	def update(self, percent):
		self.image.fill(colors.PROGRESS_BACK)
		pygame.draw.rect(self.image, colors.PROGRESS_FRONT, (0, 0, round(percent * self.length), self.height))


class HealthBar(ProgressBar):

	def __init__(self, human: Human):
		super(HealthBar, self).__init__()
		self.human = human

	def update(self, *args):
		percent = self.human.get_health() / self.human.max_health
		super(HealthBar, self).update(percent)
		self.rect.top = self.human.rect.bottom + 10
		self.rect.left = self.human.rect.centerx - 50
		if percent <= 0:
			self.kill()


class HeroHealthBar(ProgressBar):
	length = 250
	height = 30

	def __init__(self, hero: Hero, camera: Camera):
		super(HeroHealthBar, self).__init__()
		self.hero = hero
		self.rect.left = camera.rect.left + 10
		self.rect.bottom = camera.rect.bottom - 10

	def update(self, *args):
		percent = self.hero.get_health() / self.hero.max_health
		super(HeroHealthBar, self).update(percent)
