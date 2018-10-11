import pygame

# Gere les explosions
class Explosion(pygame.sprite.Sprite):

	def __init__(self, scene, pos, world, players, c_scale=-1):
		super(Explosion, self).__init__()
		# Interval entre animation
		self.interval = 33
		self.phase = 0
		import random
		from resources import Textures
		# Aleatoire dans les explosions en tournant l'image
		self.angle = random.randint(0, 359)
		self.scale = random.uniform(1, 5) if c_scale <= 0 else c_scale
		self.image = pygame.transform.rotozoom(Textures['exp_sheet'][self.phase], self.angle, self.scale)
		del random
		self.rect = self.image.get_rect()
		self.rect.center = pos
		# Quand est-ce qu'on anime la prochaine fois
		self.next_update = pygame.time.get_ticks() + self.interval

		# on explose le monde
		world.explode(self.rect.center, self.rect.width // 2)

		# Pour chaque joueur on recupere la distance
		for player in players:
			length = ((player.real_pos[0]-self.rect.center[0])**2 + (player.real_pos[1]-self.rect.center[1])**2) ** 0.5
			# Si elle est plus de 200 alors on applique les dommages au joueur

			dmg = self.rect.width - length
			if dmg > 0:
				player.hit(300-(length * 0.5))
		# Ajout au groupe de la scene
		scene.group_explosions.add(self)

	# Mise a jour de l'animation
	def update_phase(self):
		# Si on doit faire la prochaine animation
		if pygame.time.get_ticks() >= self.next_update:
			from resources import Textures
			if self.phase >= len(Textures['exp_sheet']):
				return True

			# On retaille bien l'image et la mais centre DEPRECATED
			center = self.rect.center
			self.image = pygame.transform.rotozoom(Textures['exp_sheet'][self.phase], self.angle, self.scale)
			self.rect = self.image.get_rect()
			self.rect.center = center
			self.phase += 1
			# La prochaine animation sera ?
			self.next_update = pygame.time.get_ticks() + self.interval

		return False

	# Est-ce que je dois mourrir ?
	def update(self):
		if self.update_phase():
			self.kill()
