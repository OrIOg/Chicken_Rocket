import pygame


class Terrain(pygame.sprite.Sprite):

	def __init__(self, scene, image):
		super(Terrain, self).__init__()
		self.image = image
		scene.group_platforms.add(self)
		self.rect = self.image.get_rect()
		self.mask = pygame.mask.from_surface(self.image)

	def explode(self, pos, size):
		pygame.draw.circle(self.image, (255, 0, 255, 0), pos, size)
		self.mask = pygame.mask.from_surface(self.image)
