import pygame

from player import Player
from terrain import Terrain
from Button import Button
import math
import random
from resources import Textures, Fonts, GetMap
from pygame.math import Vector2

debug = False


class Scene:

	def __init__(self, director):
		self.dir = director

		# Creer des groupes pour la gestions des objets
		self.group_explosions = pygame.sprite.Group()
		self.group_players = pygame.sprite.Group()
		self.group_platforms = pygame.sprite.Group() # Plateformes solides
		self.group_projectiles = pygame.sprite.Group()

		# Set le ciel & le sol |    Si utilise, utilise aleatoirement le jour ou la nuit
		map_graph = GetMap() #random.choice((Textures['sky'], Textures['sky2']))
		self.terrain = Terrain(self, map_graph[0])
		self.sky = map_graph[1]
		self.sky_rect = self.sky.get_rect()

		self.powerbar = Textures['powerbar'].copy()
		self.powerbar_back = Textures['powerbar_back'].copy()

		self.select_icon = Textures['select_icon'].copy()
		self.select_icon_rect = self.select_icon.get_rect()
		self.overtime = 0.0

		# Fin Variable
		self.is_over = False
		self.winner = None
		size = self.dir.screen.get_rect().size
		self.button_restart = Button(Textures['replay'].copy(), (size[0]*0.5, size[1]*0.3), self.restart)
		self.button_quit = Button(Textures['exit'].copy(), (size[0]*0.5, size[1]*0.45), self.quit_game)
		self.text_over = None

		# Creation des joueurs
		Player(self, [105.0, 500.0])
		Player(self, [1800.0, 560.0])

		# Quel joueur commence en premier ?
		self.current_player = random.randint(0, len(self.group_players)-1)
		self.last_player = self.current_player
		self.last_nb_joueurs = len(self.group_players)

		self.events = None
		self.is_shooting = False
		
	def restart(self):
		self.dir.load_scene(Scene(self.dir))
	
	def quit_game(self):
		self.dir.running = False

	# Bloque les actions des joueurs
	def freeze_player(self):
		self.current_player = -1

	# Qui est le prochain ?
	def next_player(self):
		if len(self.group_players) == 1:
			self.is_over = True
			self.winner = self.current_player
			self.text_over = Fonts['32'].render("Player {} WIN".format(1+self.current_player), True, (200, 200, 200))
			return
		self.current_player = (self.last_player+1) % len(self.group_players)
		self.last_player = self.current_player
		self.overtime = 0

	# Parcoure les evenements & agit en fonction
	def event(self):
		self.events = pygame.event.get()
		if self.is_over:
			for event in self.events:
				if event.type == pygame.MOUSEBUTTONUP:
					mx = pygame.mouse.get_pos()
					self.button_restart.isClicked(mx)
					self.button_quit.isClicked(mx)
			return

		for event in self.events:
			if event.type == pygame.QUIT:
				self.dir.running = False
			if event.type == pygame.KEYDOWN and event.unicode == 'p':
				self.dir.running = False # Quitte le jeu
			elif event.type == pygame.KEYDOWN and event.unicode == 'a' and debug:
				self.next_player() # Prochain joueur
			elif event.type == pygame.MOUSEBUTTONUP:
				if self.current_player != -1 and self.is_shooting:
					if event.button == 1:
						self.group_players.sprites()[self.current_player].upaction() # Tire
						self.is_shooting = False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if self.current_player != -1:
					if event.button == 1:
						self.is_shooting = True
						self.group_players.sprites()[self.current_player].action() # Barre de puissance

		# Gere les evenements de joueur actuel
		if self.current_player != -1 and self.group_players.sprites()[self.current_player]:
			self.group_players.sprites()[self.current_player].event()

	# Gere les mises a jours de chaque frame des groupes
	def update(self, delta_time):
		if self.is_over:
			return
		self.group_projectiles.update(delta_time)
		self.group_players.update(delta_time)
		self.group_explosions.update()
		self.overtime += delta_time

		if (self.current_player == -1 or self.last_nb_joueurs != len(self.group_players.sprites())) and len(self.group_explosions) == 0 and len(self.group_projectiles) == 0:
			self.next_player()
			self.last_nb_joueurs = len(self.group_players.sprites())

	def draw_menu(self):
		self.dir.screen.fill((200, 200, 200, 255), None, pygame.BLEND_RGBA_MULT)
		size = self.dir.screen.get_rect().size

		message = pygame.transform.rotozoom(self.text_over, math.cos(self.overtime * 2) * 1, 1 + 0.2 * (math.sin(self.overtime * 2)+1))

		self.button_restart.draw(self.dir.screen)
		self.button_quit.draw(self.dir.screen)

		size = self.dir.screen.get_rect().size
		x = size[0] * 0.5 - message.get_rect().centerx
		y = size[1] * 0.125
		self.dir.screen.blit(message, (x, y))

	# Dessine les objets de la scene
	def draw(self):
		if self.is_over:
			self.draw_menu()
			return

		# Dessine le decore & groupes
		self.dir.screen.fill((0, 0, 0))
		self.dir.screen.blit(self.sky, self.sky_rect)
		self.group_platforms.draw(self.dir.screen)
		self.group_players.draw(self.dir.screen)
		self.group_explosions.draw(self.dir.screen)
		self.group_projectiles.draw(self.dir.screen)

		# Dessine les barres de vies
		for i, player in enumerate(self.group_players.sprites()):
			player.drawHealth()
			if i == self.current_player:
				x = player.rect.centerx - self.select_icon_rect.centerx
				y = player.rect.top - self.select_icon_rect.bottom - 16 - 16*math.sin(self.overtime)
				self.dir.screen.blit(self.select_icon, (x, y))


		# Dessine la barre de puissance si active
		if self.current_player != -1 and self.group_players.sprites()[self.current_player]:
			self.group_players.sprites()[self.current_player].draw_powerbar()

		if self.is_shooting:
			mouse_pos = pygame.mouse.get_pos()
			player_center = self.group_players.sprites()[self.current_player].rect.center

			vect = (mouse_pos[0] - player_center[0], mouse_pos[1] - player_center[1])

			angle = 0
			if vect[0] is not 0:
				angle = math.degrees(-math.atan2(vect[1], vect[0]))


			back = pygame.transform.rotate(self.powerbar_back, angle)
			pos_back = back.get_rect()

			pos = Vector2(player_center)# - pos_back.midright).rotate(angle)

			rotated_offset = Vector2(64, 0).rotate(-angle)
			new_pos= Vector2(player_center) + rotated_offset
			back = pygame.transform.rotate(self.powerbar_back, angle)
			rect = back.get_rect(center=new_pos)

			self.dir.screen.blit(back, rect)

			# FRONT POWERBAR
			x = self.group_players.sprites()[self.current_player].mult * 128
			cut_rect = (0, 0, x, 64)
			front = self.powerbar.subsurface(cut_rect)
			fr_rect = front.get_rect()
			rotated_offset = Vector2(fr_rect.width//2, 0).rotate(-angle)
			new_pos = Vector2(player_center) + rotated_offset
			back = pygame.transform.rotate(front, angle)
			rect = back.get_rect(center=new_pos)

			self.dir.screen.blit(pygame.transform.rotate(front, angle), rect)

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
			ang_text = Fonts['default'].render(str(math.degrees(angle)), False, (0, 0, 0, 255))
			self.dir.screen.blit(ang_text, player_center)
		#pygame.draw.aaline(self.dir.screen, (255, 0, 0), player_center, mouse_pos)
