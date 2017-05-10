import pygame
import os

class Button(pygame.sprite.Sprite):

	def __init__(self, image, pos, callback):
		super(Button, self).__init__()
		self.image = image
		self.rect = self.image.get_rect()
		self.pos = pos
		self.callback = callback

	def isClicked(self, mouse_pos):
		x = mouse_pos[0] #position de la souris en x
		y = mouse_pos[1] #position de la souris en y

		if self.pos[0] <= x <= self.pos[0] + self.rect.w and self.pos[1] <= y <= self.pos[1] + self.rect.h:
			self.callback()
			return True
		return False

	def draw(self, screen):
		screen.blit(self.image, self.pos)
