import pygame
from AnimatedSprite import AnimatedSprite


class Explosion(object):

	EXPLOSION = AnimatedSprite(explode=[(64, 64), 16, 4, (0, 0), 'exp_sheet.png'])

	def __init__(self, scene, to_destroy, c_scale=-1):
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
		self.rect.center = pygame.mouse.get_pos()
		self.next_update = pygame.time.get_ticks() + self.interval

		to_destroy.explode(self.rect.center, self.rect.width // 5)
		scene.group_explosions.add(self)

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
