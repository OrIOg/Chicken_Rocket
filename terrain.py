import pygame

# Le terrain destructible
class Terrain(pygame.sprite.Sprite):
	# Pourrait etre utilise pour n'importe quel objet destructible
	def __init__(self, scene, image):
		super(Terrain, self).__init__()
		# On ajoute au groupe de la scene
		scene.group_platforms.add(self)
		# On set l'image
		self.image = image
		self.rect = self.image.get_rect()
		self.mask = pygame.mask.from_surface(self.image)

	# On explose en dessinant un cercle vie :) kek
	def explode(self, pos, size):
		pygame.draw.circle(self.image, (255, 0, 255, 0), pos, size)
		self.mask = pygame.mask.from_surface(self.image)
