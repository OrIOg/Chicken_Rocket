import pygame
from operator import add, sub
from math import atan2
from explosion import Explosion
from bullet import Bullet
from math import sin

# Additioner des tableaux/vecteur
def addv(*vectors):
	return [sum(x) for x in zip(*vectors)]

# Soustraction de tableaux/vecteur
def subv(vector1, vector2):
	return list(map(sub, vector1, vector2))

# Permet de gerer un joueur
class Player(pygame.sprite.Sprite):

	MAX_LIFE = 500

	def __init__(self, scene, pos):
		# Variables de scene & d'images
		self.scene = scene
		from resources import Textures
		super(Player, self).__init__()
		# Set les animations
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
		# Variable pour monter automatiquement un nb de pixels
		self.step_height = -4

		# Variables de GamePlay
		self.life = Player.MAX_LIFE

		# Variable Barre de puissance
		self.getting_power = False
		self.X = 0
		self.mult = 0

		scene.group_players.add(self)

	# Touché !
	def hit(self, damage):
		self.life -= damage
		if self.life <= 0:
			self.kill()

	# Gere la barre de puissance & l'affiche
	def draw_powerbar(self):
		if self.getting_power:
			posx = pygame.display.get_surface().get_width()/2 - 100
			posy = pygame.display.get_surface().get_height() - 50
			pygame.draw.rect(self.scene.dir.screen, (0, 0, 255), (posx, posy, 200, 50))
			self.X += 0.01
			self.mult = abs(sin(self.X))
			pygame.draw.rect(self.scene.dir.screen, (255, 0, 0), (posx, posy, self.mult * 200, 50))

	# Action lorsque l'on lache le clique. Stop les joueurs. Creer une balle
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

	# Action lorsque l'on maintient la souris
	def action(self):
		self.getting_power = True

	# Gestions des mouvements & animations grace aux events
	def event(self):
		self.movements = [0, 0]
		# Si on ne tire pas...
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

	# Gravite - Screw Gravity
	def apply_gravity(self, delta_time):
		if self.grounded:
			pass#self.velocity[1] = 0
		else:
			self.velocity[1] += 25 * delta_time

	# Detection du sol
	def check_ground(self, collisions):
		if len(collisions) is 0:
			self.grounded = False
		else:
			self.grounded = True
			self.real_pos = subv(self.real_pos, self.velocity)
			self.velocity[1] = 0

	# Est-ce que je peux encore moins bouger avec cette position la ?
	def check_collisions(self, surfaces, offset=(0,0)):
		# Est-ce que au moins je touche quelque chose ?
		if len(surfaces) is 0:
			return True
		terrain = surfaces[0]

		#new_pos = addv(self.rect.topleft, (int(self.movements[0]), int(self.movements[1])))
		# Nouvelle position simule
		new_pos = addv(self.rect.topleft, (int(self.movements[0]), 0), offset)

		# Recuperation du nombre de pixels en collision avec le joueur
		current = terrain.mask.overlap_area(self.mask, self.rect.topleft)
		new = terrain.mask.overlap_area(self.mask, new_pos)
		# Si il y en a plus, on annule tout, le navire coule, ABORT
		if new > current:
			return False
		return True

	# Gestions de tout les mouvements, et autres
	def update(self, delta_time):
		# J'applique la gravite
		self.apply_gravity(delta_time)
		self.real_pos = addv(self.real_pos, self.velocity)
		self.rect.midbottom = self.real_pos

		# Est-ce que je suis dans le sol ? si oui j'annule l'application de la gravite
		crashgroup = pygame.sprite.spritecollide(self, self.scene.group_platforms, False, pygame.sprite.collide_mask)
		self.check_ground(crashgroup)

		# On multie les mouvements par le delta time pourrait etre fait dans event :|
		self.movements[0] *= delta_time
		self.movements[1] *= delta_time

		# Si je suis au sol, application du saut, s'il y en a un :)
		if self.grounded:
			self.real_pos[1] += self.movements[1]

		# Est-ce que je rentre dans le terrain si je fais ca ?
		if self.check_collisions(crashgroup):
			self.real_pos[0] += self.movements[0]
		# Sinon est-ce que si je monte ca marche ?
		elif self.check_collisions(crashgroup, (int(self.movements[0]), self.step_height)):
			self.real_pos[0] += self.movements[0]
			self.real_pos[1] += self.step_height

		# Si je suis hors map, je meurs *squick*
		if self.rect.top > self.scene.dir.screen.get_rect().bottom:
			self.kill()

		# Mise a jour de la position
		self.rect.midbottom = self.real_pos

	# Dessine la vie avec Mickey
	def drawHealth(self):
		pygame.draw.rect(self.scene.dir.screen, (255, 0, 0), (self.rect.left, self.rect.top, self.rect.w, 4))
		pygame.draw.rect(self.scene.dir.screen, (0, 255, 0), (self.rect.left, self.rect.top, self.rect.w * (self.life/Player.MAX_LIFE), 4))
