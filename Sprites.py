import pygame
from config import *
import math
import random
from assets  import SpriteSheet, Animation



class Selector(pygame.sprite.Sprite):
    def __init__(self, game, x, y, image):
        self.game = game
        self._layer = SELECTOR_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        pass

class Lyn(pygame.sprite.Sprite):
    def __init__(self, game, x, y, image=None):  # `image` is no longer used
        self.game = game
        self._layer = LYN_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.tx = x  # tile x
        self.ty = y  # tile y
        self.width = TILESIZE
        self.height = TILESIZE

        # Load sprite sheet and animations
        self.sheet = SpriteSheet("Assets/Lyn.gif", 16, 16)
        self.animations = {
            "idle": Animation([self.sheet.get_frame(i, 0, 433 ,396) for i in range(4)], 200),
            "attack": Animation([self.sheet.get_frame(i, 0) for i in range(8)], 100),
            "crit": Animation([self.sheet.get_frame(i, 1) for i in range(8)], 100),
        }
        self.current_anim = self.animations["idle"]
        self.map_icon = self.sheet.get_frame(col=0, row=5)
        self.image = self.current_anim.get_current_frame()
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.tx * TILESIZE, self.ty * TILESIZE)

    def update(self):
            
        self.current_anim.update(self.game.clock.get_time())
        self.image = self.current_anim.get_current_frame()
        self.rect.topleft = (self.tx * TILESIZE, self.ty * TILESIZE)


    def set_tile_position(self, x, y):
        self.tx = x
        self.ty = y

    def play(self, animation_name):
        if animation_name in self.animations:
            self.current_anim = self.animations[animation_name]

class Brigand(pygame.sprite.Sprite):
    def __init__(self, game, x, y, image):
        self.game = game
        self._layer = LYN_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        pass
