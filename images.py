import pygame
import os
from config import game_folder

img_folder = os.path.join(game_folder, 'img')

small_tree = pygame.image.load(os.path.join(img_folder, 'small-tree.png'))
small_tree = pygame.transform.scale(small_tree, (64, 128))

hero = pygame.image.load(os.path.join(img_folder, 'snowman1.png'))
hero = pygame.transform.scale(hero, (64, 64))
