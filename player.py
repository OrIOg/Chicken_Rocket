import pygame
from operator import add, sub
from math import atan2
from explosion import Explosion
from bullet import Bullet
from math import sin

def addv(*vectors):
	return [sum(x) for x in zip(*vectors)] #list(map(add, vectors[0], vectors[1]))


def subv(vector1, vector2):
	return list(map(sub, vector1, vector2))


class Player(pygame.sprite.Sprite):

	MAX_LIFE = 500

	def __init__(self, scene, pos):
		# Variables de scene & d'images
		self.scene = scene
		from resources import Textures
		super(Player, self).__init__()
		self.animations = list(Textures['poulet'])
		self.key = 0
		self.animations[self.key].iter()
		self.image = self.animations[self.key].next()
		self.rect = self.image.get_rect()
		self.mask = pygame.mask.from_surface(self.image)

		# Variables de mouvements
		self.real_pos = pos#[400.0, 100.0]
		self.velocity = [0.0, 0.0]
		self.movements = [0.0, 0.0]
		self.rect.midbottom = self.real_pos
		self.grounded = False
		self.step_height = -4

		# Variables de GamePlay
		self.life = Player.MAX_LIFE

		self.getting_power = False
		self.X = 0
		self.mult = 0

		scene.group_players.add(self)

	def hit(self, damage):
		self.life -= damage
		if self.life <= 0:
			self.kill()

	def draw_powerbar(self):
		if self.getting_power:
			posx = pygame.display.get_surface().get_width()/2 - 100
			posy = pygame.display.get_surface().get_height() - 50
			pygame.draw.rect(self.scene.dir.screen, (0, 0, 255), (posx, posy, 200, 50))
			self.X += 0.01
			self.mult = abs(sin(self.X))
			pygame.draw.rect(self.scene.dir.screen, (255, 0, 0), (posx, posy, self.mult * 200, 50))

	def upaction(self):
		self.getting_power = False
		self.scene.freeze_player()
		mouse_pos = pygame.mouse.get_pos()

		vect = (mouse_pos[0] - self.rect.centerx, mouse_pos[1] - self.rect.centery)

		# soh cah toa
		angle = 0
		if vect[0] is not 0:
			angle = -atan2(vect[1], vect[0])

		Bullet(self.scene, [self.rect.midtop[0],self.rect.midtop[1]-32], 2*self.mult, angle, [self.scene.group_players, self.scene.group_platforms])
		self.X = 0
		self.mult = 0

	def action(self):
		self.getting_power = True

	def event(self):
		self.movements = [0, 0]
		if not self.getting_power:
			keys = pygame.key.get_pressed()
			if keys[pygame.K_a]:
				self.movements[0] -= 150
				self.key = 1
			elif keys[pygame.K_d]:
				self.movements[0] += 150
				self.key = 2
			elif keys[pygame.K_SPACE] and self.grounded:
				self.velocity[1] -= 5
			else:
				self.animations[self.key].iter()
			self.image = self.animations[self.key].next()

	def apply_gravity(self, delta_time):
		if self.grounded:
			pass#self.velocity[1] = 0
		else:
			self.velocity[1] += 25 * delta_time

	def check_ground(self, collisions):
		if len(collisions) is 0:
			self.grounded = False
		else:
			self.grounded = True
			self.real_pos = subv(self.real_pos, self.velocity)
			self.velocity[1] = 0

	def check_collisions(self, surfaces, offset=(0,0)):
		if len(surfaces) is 0:
			return True
		terrain = surfaces[0]

		#new_pos = addv(self.rect.topleft, (int(self.movements[0]), int(self.movements[1])))
		new_pos = addv(self.rect.topleft, (int(self.movements[0]), 0), offset)

		current = terrain.mask.overlap_area(self.mask, self.rect.topleft)
		new = terrain.mask.overlap_area(self.mask, new_pos)
		if new > current:
			return False
		return True

	def update(self, delta_time):
		self.apply_gravity(delta_time)
		self.real_pos = addv(self.real_pos, self.velocity)
		self.rect.midbottom = self.real_pos
		crashgroup = pygame.sprite.spritecollide(self, self.scene.group_platforms, False, pygame.sprite.collide_mask)
		self.check_ground(crashgroup)

		self.movements[0] *= delta_time
		self.movements[1] *= delta_time

		if self.grounded:
			self.real_pos[1] += self.movements[1]

		if self.check_collisions(crashgroup):
			self.real_pos[0] += self.movements[0]
		elif self.check_collisions(crashgroup, (int(self.movements[0]), self.step_height)):
			self.real_pos[0] += self.movements[0]
			self.real_pos[1] += self.step_height

		if self.rect.top > self.scene.dir.screen.get_rect().bottom:
			self.kill()

		self.rect.midbottom = self.real_pos

	def drawHealth(self):
		pygame.draw.rect(self.scene.dir.screen, (255, 0, 0), (self.rect.left, self.rect.top, self.rect.w, 4))
		pygame.draw.rect(self.scene.dir.screen, (0, 255, 0), (self.rect.left, self.rect.top, self.rect.w * (self.life/Player.MAX_LIFE), 4))
