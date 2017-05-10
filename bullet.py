import pygame
from resources import Sounds, Textures
from math import cos, sin
from explosion import Explosion
import math

class Bullet(pygame.sprite.Sprite):
	POWER = 1000

	def __init__(self, scene, pos, pow, ang, collisions_mask):
		super(Bullet, self).__init__()
		self.scene = scene
		self.animations = list(Textures['missile'])
		self.key = 0
		self.animations[self.key].iter()
		self.image = self.animations[self.key].next()
		self.rect = self.image.get_rect()
		self.position = [pos[0],pos[1]]
		self.rect.center = self.position
		self.acceleration = [Bullet.POWER*pow*cos(ang), -Bullet.POWER*pow*sin(ang)]
		self.angle = ang
		Sounds['bullet'].play()

		self.collisions_mask = collisions_mask
		scene.group_projectiles.add(self)

	def gravity(self, delta_time):
		self.acceleration[1] += 1000 * delta_time

	def update(self, delta_time):
		self.gravity(delta_time)
		self.position[0] += self.acceleration[0] * delta_time
		self.position[1] += self.acceleration[1] * delta_time

		self.rect.center = self.position

		for col_mask in self.collisions_mask:
			hits = pygame.sprite.spritecollide(self, col_mask, False, pygame.sprite.collide_mask)
			if len(hits) != 0:
				Explosion(self.scene, self.position, self.scene.terrain, self.scene.group_players.sprites(), 2.5)
				self.kill()

		if -64 > self.position[0] or self.position[0] > pygame.display.get_surface().get_width() + 64 or -256 > self.position[1] or self.position[1] > pygame.display.get_surface().get_height() + 64:
			self.kill()
			self.scene.next_player()

		self.animations[self.key].iter()
		if math.pi/2 < self.angle:
			self.image = pygame.transform.flip(self.animations[self.key].next(), True, True)
		else:
			self.image = self.animations[self.key].next()
#
# from math import cos, sin
#
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running=False
#         elif event.type == pygame.MOUSEBUTTONDOWN:
#             if cooldown <= 0:
#                 cooldown = 1.0
#                 pygame.mixer.music.play(0,0)
#                 mouseX, mouseY = pygame.mouse.get_pos()
#                 bullets_group.append(Bullet([mouseX, mouseY], [PUISSANCE*cos(45),-PUISSANCE*sin(45)]))
#
#     delta_time = clock.tick() * 0.001
#     if cooldown > 0:
#         cooldown -= delta_time
#
#     for bullet in bullets_group:
#         bullet.update(delta_time)
#
#     screen.fill(backgroundcolour)
#
#     for bullet in bullets_group:
#         bullet.draw(screen)
#
#     pygame.display.update()