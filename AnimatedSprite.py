import pygame
from resources import get_sheet

# Ce fichier n'est pas utilisé dans le jeu

class AnimatedSprite(pygame.sprite.Sprite):
	"""Extended sprite class to animate more easily"""

	def __init__(self, **keyargs):
		super(AnimatedSprite, self).__init__()
		self.animations = dict()
		for key, value in keyargs.items():
			self.animations[key] = get_sheet(*value)

		print(self.animations.keys())
		self.key = list(self.animations.keys())[0]
		self.frame = 0

		self.image = self.animations[self.key][self.frame]
		self.rect = self.image.get_rect()

	def set_key(self, key):
		if key in self.animations.keys():
			self.key = key
		return

	def next(self, loop=True):
		if (self.frame+1) >= len(self.animations[self.key]):
			if loop:
				self.frame = 0
				self.update_sprite()
			return True
		else:
			self.frame += 1
			self.update_sprite()
		return False

	def update_sprite(self):
		center = self.rect.center
		self.image = self.animations[self.key][self.frame]
		self.rect = self.image.get_rect()
		self.rect.center = center


