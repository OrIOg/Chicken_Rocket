import pygame
import os

# Gere un bouton
class Button(pygame.sprite.Sprite):

	def __init__(self, image, pos, callback):
		super(Button, self).__init__()
		# Set Image bouton & positon
		self.image = image
		self.rect = self.image.get_rect()
		self.pos = pos
		# Action du bouton
		self.callback = callback

	# Suis-je clique
	def isClicked(self, mouse_pos):
		x = mouse_pos[0] #position de la souris en x
		y = mouse_pos[1] #position de la souris en y

		# Est-ce que la souris est dans le bouton
		if self.pos[0] <= x <= self.pos[0] + self.rect.w and self.pos[1] <= y <= self.pos[1] + self.rect.h:
			# Alors je fais l'action
			self.callback()
			return True
		return False

	# Dessine le bouton
	def draw(self, screen):
		screen.blit(self.image, self.pos)
