import pygame


class Explosion(pygame.sprite.Sprite):

	def __init__(self, scene, pos, world, players, c_scale=-1):
		super(Explosion, self).__init__()
		self.interval = 33
		self.phase = 0
		import random
		from resources import Textures
		self.angle = random.randint(0, 359)
		self.scale = random.uniform(1, 5) if c_scale <= 0 else c_scale
		self.image = pygame.transform.rotozoom(Textures['exp_sheet'][self.phase], self.angle, self.scale)
		del random
		self.rect = self.image.get_rect()
		self.rect.center = pos
		self.next_update = pygame.time.get_ticks() + self.interval

		world.explode(self.rect.center, self.rect.width // 2)

		for player in players:
			length = ((player.real_pos[0]-self.rect.center[0])**2 + (player.real_pos[1]-self.rect.center[1])**2) ** 0.5
			damage = (100-(length/2))
			print(length)
			if damage > 0:
				player.hit(damage)
		scene.group_explosions.add(self)
		scene.next_player()

	def update_phase(self):
		if pygame.time.get_ticks() >= self.next_update:
			from resources import Textures
			if self.phase >= len(Textures['exp_sheet']):
				return True

			center = self.rect.center
			self.image = pygame.transform.rotozoom(Textures['exp_sheet'][self.phase], self.angle, self.scale)
			self.rect = self.image.get_rect()
			self.rect.center = center
			self.phase += 1
			self.next_update = pygame.time.get_ticks() + self.interval

		return False

	def update(self):
		if self.update_phase():
			# gr.blit(Explosion.explosion_del, self.rect, None, pygame.BLEND_RGBA_MIN)
			self.kill()
