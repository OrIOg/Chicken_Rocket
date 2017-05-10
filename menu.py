import pygame
from Button import Button
from scene import Scene


class Menu:

	def play(self):
		self.dir.scene = Scene(self.dir)

	def quitt(self):
		self.dir.running = False

	def __init__(self, director):
		from resources import Textures, Fonts
		self.dir = director

		self.play_button = Button(Textures["play"], (432, 465), self.play)
		self.exit_button = Button(Textures["exit"], (1488-315, 500), self.quitt)
		self.background = Textures["menu"]

	def event(self):
		pass

	def update(self, delta_time):
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONUP:
				mx = pygame.mouse.get_pos()
				self.play_button.isClicked(mx)
				self.exit_button.isClicked(mx)

	def draw(self):
		self.dir.screen.blit(self.background, (0,0))
		self.play_button.draw(self.dir.screen)
		self.exit_button.draw(self.dir.screen)
		pygame.display.update()
