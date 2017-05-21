import pygame
from scene import Scene
from menu import Menu
from resources import Textures, Fonts, init_ressources

class Directeur(object):

	def __init__(self):
		# Creer une fenetre en 1920x1080 en plein ecran
		self.screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
		# Definit le nom du programme
		pygame.display.set_caption("Chicken Rocket")

		# Creer l'horloge du jeu
		self.clock = pygame.time.Clock()
		# Charge les ressources
		init_ressources()

		# Est-ce que le jeu continue
		self.running = True
		# Creer le menu et le met comme menu
		self.scene = Menu(self)
		self.display_fps = Fonts['default']
		self.game_loop()

	def game_loop(self):
		while self.running:
			# Temps entre deux updates
			delta_time = self.clock.tick() * 0.001
			# Appelle les fonctions principales d'une scene
			self.scene.event()
			self.scene.update(delta_time)
			self.scene.draw()
			text = self.display_fps.render(str(self.clock.get_fps()), False, (0, 0, 0, 255))
			# Affiche la nouvelle frame
			pygame.display.update()


# Affiche la nouvelle frame
def main():
	pygame.init()
	pygame.display.init()
	dir = Directeur()

if __name__ == "__main__":
	main()
	exit()


