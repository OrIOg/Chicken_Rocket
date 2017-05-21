import pygame

from player import Player
from terrain import Terrain
import math
import random
from resources import Textures, Fonts

debug = 0


class Scene:

	def __init__(self, director):
		self.dir = director

		# Creer des groupes pour la gestions des objets
		self.group_explosions = pygame.sprite.Group()
		self.group_players = pygame.sprite.Group()
		self.group_platforms = pygame.sprite.Group() # Plateformes solides
		self.group_projectiles = pygame.sprite.Group()

		# Set le ciel & le sol |    Si utilise, utilise aleatoirement le jour ou la nuit
		self.sky = Textures['sky'] #random.choice((Textures['sky'], Textures['sky2']))
		self.sky_rect = self.sky.get_rect()
		self.terrain = Terrain(self, Textures['ground'])

		# Creation des joueurs
		Player(self, [100.0, 100.0])
		Player(self, [1820.0, 100.0])

		# Quel joueur commence en premier ?
		self.current_player = random.randint(0, len(self.group_players)-1)
		self.last_player = self.current_player

		self.events = None

	# Bloque les actions des joueurs
	def freeze_player(self):
		self.current_player = -1

	# Qui est le prochain ?
	def next_player(self):
		self.current_player = (self.last_player+1) % len(self.group_players)
		self.last_player = self.current_player

	# Parcoure les evenements & agit en fonction
	def event(self):
		self.events = pygame.event.get()
		for event in self.events:
			if event.type == pygame.QUIT:
				self.dir.running = False
			if event.type == pygame.KEYDOWN and event.unicode == 'p':
				self.dir.running = False # Quitte le jeu
			elif event.type == pygame.KEYDOWN and event.unicode == 'a' and debug:
				self.next_player() # Prochain joueur
			elif event.type == pygame.MOUSEBUTTONUP:
				if self.current_player != -1:
					if event.button == 1:
						self.group_players.sprites()[self.current_player].upaction() # Tire
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if self.current_player != -1:
					if event.button == 1:
						self.group_players.sprites()[self.current_player].action() # Barre de puissance

		# Gere les evenements de joueur actuel
		if self.current_player != -1 and self.group_players.sprites()[self.current_player]:
			self.group_players.sprites()[self.current_player].event()

	# Gere les mises a jours de chaque frame des groupes
	def update(self, delta_time):
		self.group_projectiles.update(delta_time)
		self.group_players.update(delta_time)
		self.group_explosions.update()

	# Dessine les objets de la scene
	def draw(self):
		# Dessine le decore & groupes
		self.dir.screen.fill((0, 0, 0))
		self.dir.screen.blit(self.sky, self.sky_rect)
		self.group_platforms.draw(self.dir.screen)
		self.group_players.draw(self.dir.screen)
		self.group_explosions.draw(self.dir.screen)
		self.group_projectiles.draw(self.dir.screen)

		# Dessine les barres de vies
		for player in self.group_players.sprites():
			player.drawHealth()

		# Dessine la barre de puissance si active
		if self.current_player != -1 and self.group_players.sprites()[self.current_player]:
			self.group_players.sprites()[self.current_player].draw_powerbar()

		# Debug
		if self.current_player != -1 and debug == 1:
			mouse_pos = pygame.mouse.get_pos()
			player_center = self.group_players.sprites()[self.current_player].rect.center

			vect = (mouse_pos[0] - player_center[0], mouse_pos[1] - player_center[1])

			#soh cah toa
			angle = 0
			if vect[0] is not 0:
				angle = -math.atan2(vect[1], vect[0])

			pygame.draw.aaline(self.dir.screen, (255, 0, 0), player_center, mouse_pos)
			pygame.draw.aaline(self.dir.screen, (0, 255, 0), player_center, (player_center[0] + vect[0], player_center[1]))
			pygame.draw.aaline(self.dir.screen, (0, 0, 255), (player_center[0] + vect[0], player_center[1]),
								(player_center[0] + vect[0], player_center[1] + vect[1]))
			pygame.draw.arc(self.dir.screen, (255, 0, 255), (player_center[0]-32, player_center[1]-32, 64, 64), 0, angle)
			ang_text = self.display_explosion_size.render(str(math.degrees(angle)), False, (0, 0, 0, 255))
			self.dir.screen.blit(ang_text, player_center)
		#pygame.draw.aaline(self.dir.screen, (255, 0, 0), player_center, mouse_pos)
