
from typing import List
import pygame

import colors
import objects
import utils
from objects import Obj

BLOCK_WIDTH = 800
BLOCK_HEIGHT = 800


class Block(obj.Obj):
	def __init__(self, position: utils.Point, size, parent_field):
		super().__init__(position, size, parent_field)
		self.surface = pygame.Surface((BLOCK_WIDTH, BLOCK_HEIGHT))

	def draw(self, sc: pygame.Surface, x, y):
		self.surface.fill(colors.GRASS)
		# pygame.draw.line(self.screen, color.WHITE, (0, 0), (0, BLOCK_HEIGHT - 1))
		# pygame.draw.line(self.screen, color.WHITE, (BLOCK_WIDTH - 1, 0), (BLOCK_WIDTH - 1, BLOCK_HEIGHT - 1))
		# pygame.draw.line(self.screen, color.WHITE, (0, 0), (BLOCK_WIDTH - 1, 0))
		# pygame.draw.line(self.screen, color.WHITE, (0, BLOCK_HEIGHT - 1), (BLOCK_WIDTH, BLOCK_HEIGHT - 1))
		sc.blit(self.surface, (x, y, BLOCK_WIDTH, BLOCK_HEIGHT))


# def gen_block():
# 	sprites = []
# 	for o in range(0, 10):
# 		sprites.append(gen_tree())
# 	return Block(sprites)
