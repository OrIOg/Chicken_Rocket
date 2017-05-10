import pygame

from player import Player
from terrain import Terrain
import math
import random
from resources import Textures, Fonts

debug = 1

class Scene:

	def __init__(self, director):
		self.dir = director

		self.group_explosions = pygame.sprite.Group()
		self.group_players = pygame.sprite.Group()
		self.group_platforms = pygame.sprite.Group()
		self.group_projectiles = pygame.sprite.Group()

		self.sky = Textures['sky']#random.choice((Textures['sky'], Textures['sky2']))
		self.sky_rect = self.sky.get_rect()
		self.terrain = Terrain(self, Textures['ground'])

		self.explosion_size = 0
		self.display_explosion_size = Fonts['default']

		Player(self, [100.0, 100.0])
		Player(self, [1820.0, 100.0])

		self.current_player = random.randint(0, len(self.group_players)-1)
		self.last_player = self.current_player

		self.events = None

	def freeze_player(self):
		self.current_player = -1

	def next_player(self):
		self.current_player = (self.last_player+1) % len(self.group_players)
		self.last_player = self.current_player

	def event(self):
		self.events = pygame.event.get()
		for event in self.events:
			if event.type == pygame.QUIT:
				self.dir.running = False
			if event.type == pygame.KEYDOWN and event.unicode == 'p':
				self.dir.running = False
			elif event.type == pygame.KEYDOWN and event.unicode == 'a' and debug:
				self.next_player()
			elif event.type == pygame.MOUSEBUTTONUP:
				if self.current_player != -1:
					if event.button == 1:
						self.group_players.sprites()[self.current_player].upaction()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if self.current_player != -1:
					if event.button == 1:
						self.group_players.sprites()[self.current_player].action()
					elif event.button == 4:
						self.explosion_size += 0.5
					elif event.button == 5:
						self.explosion_size -= 0.5
					self.explosion_size = float('%.3f' % self.explosion_size)
		if self.current_player != -1 and self.group_players.sprites()[self.current_player]:
			self.group_players.sprites()[self.current_player].event()

	def update(self, delta_time):
		self.group_projectiles.update(delta_time)
		self.group_players.update(delta_time)
		self.group_explosions.update()

	def draw(self):
		self.dir.screen.fill((0, 0, 0))
		self.dir.screen.blit(self.sky, self.sky_rect)
		#self.dir.screen.blit(self.terrain.image, self.terrain.rect)
		self.group_platforms.draw(self.dir.screen)
		self.group_players.draw(self.dir.screen)
		self.group_explosions.draw(self.dir.screen)
		self.group_projectiles.draw(self.dir.screen)

		for player in self.group_players.sprites():
			player.drawHealth()

		if self.current_player != -1 and self.group_players.sprites()[self.current_player]:
			self.group_players.sprites()[self.current_player].draw_powerbar()

		#text = self.display_explosion_size.render(str(self.explosion_size), False, (0, 0, 0, 255))
		#self.dir.screen.blit(text, (0, 50))

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
