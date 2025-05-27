import pygame
from Vars import *
import math
import random

class Selector(pygame.sprite.Sprite):
	def __init__(self, game, x, y):

		self.game = game
		self._layer = SELECTOR_LAYER
		self.groups = self.game.all_sprites
		pygame.sprite.Sprite.__init__(self,self.groups)

		self.x = x * TILESIZE
		self.y = y *TILESIZE
		self.width = TILESIZE
		self.height = TILESIZE

		self.image = pygame.image.load('Selector.png')

		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.y = self.y



	def update(self):
		pass




class Lyn(pygame.sprite.Sprite):
	def __init__(self, game, x, y):

		self.game = game
		self._layer = LYN_LAYER
		self.groups = self.game.all_sprites
		pygame.sprite.Sprite.__init__(self,self.groups)

		self.x = x * TILESIZE
		self.y = y *TILESIZE
		self.width = TILESIZE
		self.height = TILESIZE

		self.image = pygame.image.load('Lyn.png')

		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.y = self.y

	def update(self):
		pass

class Brigand(pygame.sprite.Sprite):
	def __init__(self, game, x, y):

		self.game = game
		self._layer = LYN_LAYER
		self.groups = self.game.all_sprites
		pygame.sprite.Sprite.__init__(self,self.groups)

		self.x = x * TILESIZE
		self.y = y *TILESIZE
		self.width = TILESIZE
		self.height = TILESIZE

		self.image = pygame.image.load('Brigand.png')

		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.y = self.y
