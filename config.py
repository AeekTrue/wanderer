import os

import pygame

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')

tree_img = pygame.image.load(os.path.join(img_folder, 'small-tree.png'))
tree_img = pygame.transform.scale(tree_img, (64, 128))

hero_img = pygame.image.load(os.path.join(img_folder, 'snowman1.png'))
hero_img = pygame.transform.scale(hero_img, (64, 64))

BTN_UP = pygame.K_w
BTN_DOWN = pygame.K_s
BTN_RIGHT = pygame.K_d
BTN_LEFT = pygame.K_a
ROOT_OF_2 = 1.41421356237

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
FPS = 120
RPS = 5   # network requests per second
