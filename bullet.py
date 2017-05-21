import pygame
from resources import Sounds, Textures
from math import cos, sin
from explosion import Explosion
import math

# Gere le missle magique :)

class Bullet(pygame.sprite.Sprite):
	POWER = 1000

	def __init__(self, scene, pos, pow, ang, collisions_mask):
		super(Bullet, self).__init__()
		self.scene = scene
		# Set animation & image du missile
		self.animations = list(Textures['missile'])
		self.key = 0
		self.animations[self.key].iter()
		self.image = self.animations[self.key].next()
		self.rect = self.image.get_rect()
		self.position = [pos[0],pos[1]]
		self.rect.center = self.position
		# Calcule de l'acceleration, cosinus, sinus. Merci la SI
		self.acceleration = [Bullet.POWER*pow*cos(ang), -Bullet.POWER*pow*sin(ang)]
		self.angle = ang
		# Joue le son du missile
		Sounds['bullet'].play()

		self.collisions_mask = collisions_mask
		# Ajout au groupe de la scene
		scene.group_projectiles.add(self)

	# Hello gravity
	def gravity(self, delta_time):
		self.acceleration[1] += 1000 * delta_time

	# Mise a jour - avast :[
	def update(self, delta_time):
		# Applique la gravite & acceleration
		self.gravity(delta_time)
		self.position[0] += self.acceleration[0] * delta_time
		self.position[1] += self.acceleration[1] * delta_time

		# Mise a jour de la position
		self.rect.center = self.position

		# Est-ce que je touche quelque chose dans ce que j'ai le droit de toucher
		for col_mask in self.collisions_mask:
			hits = pygame.sprite.spritecollide(self, col_mask, False, pygame.sprite.collide_mask)
			if len(hits) != 0:
				# Touché  BOOM !
				Explosion(self.scene, self.position, self.scene.terrain, self.scene.group_players.sprites(), 2.5)
				self.kill()

		# Si je sors de l'ecran je meurs aussi :(
		if -64 > self.position[0] or self.position[0] > pygame.display.get_surface().get_width() + 64 or -256 > self.position[1] or self.position[1] > pygame.display.get_surface().get_height() + 64:
			self.kill()
			self.scene.next_player()

		# NEXT ! animation
		self.animations[self.key].iter()
		# change la direction du missile selon l'angle #IDK fait au feeling :s
		if math.pi/2 < self.angle:
			self.image = pygame.transform.flip(self.animations[self.key].next(), True, True)
		else:
			self.image = self.animations[self.key].next()