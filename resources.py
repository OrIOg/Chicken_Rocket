import os
import random
from pygame import image, font, mixer
from spritestripanim import SpriteStripAnim

# Fonction qui decoupe une spritesheet en fonction de la taille
# du nombre d'images totales et par ligne ainsi qu'une position de départ.
def get_sheet(size, nb, max_per_line, offset, *path):
	sprite_sheet = []
	# Recupere la spritesheet
	sprite = image.load(get(*path)).convert_alpha()
	# Parcoure la spritesheet image par image et les ajoutes a la list
	for y in range(offset[1], nb//max_per_line):
		y_s = size[1] * y
		for x in range(offset[0], min((nb - len(sprite_sheet)), max_per_line)):
			x_s = size[0] * x
			sprite_sheet.append(sprite.subsurface((x_s, y_s, size[0]-1, size[1]-1)).convert_alpha())
	# Renvoie des images decoupees.
	return sprite_sheet

# Recupere le dossier du script
data_folder = os.path.join(os.getcwd(), 'data')

# Assemble les chemins pour avoir le chemin absolue
def get(*path):
	return os.path.join(data_folder, *path)

# Recupere un son et permet d'ajuster son volume
def get_sound(volume, *path):
	sound = mixer.Sound(get(*path))
	sound.set_volume(volume)
	return sound

def GetMap():
	nb = len(skys)
	rnd = random.randrange(0, nb)
	return (grounds[rnd].copy(), skys[rnd].copy())


grounds = []
skys = []

Textures = dict()
Fonts = dict()
Sounds = dict()

# Initialisation des ressources: images sons ...
def init_ressources():
	# Conversion des images pour l'usage de pygame

	# Decor / Ancien joueur & Ancinne balle
	
	global skys
	global grounds
	global data_folder
	for i in os.listdir(data_folder):
		if os.path.isfile(os.path.join(data_folder, i)) and 'sky' in i:
			skys.append(image.load(get(i)).convert_alpha())
	for i in os.listdir(data_folder):
		if os.path.isfile(os.path.join(data_folder, i)) and 'ground' in i:
			grounds.append(image.load(get(i)).convert_alpha())
	#skys = [filename for filename in os.listdir(data_folder) if filename.startswith("sky")]
	#grounds = [filename for filename in os.listdir(data_folder) if filename.startswith("ground")]

	Textures['player'] = image.load(get('player.png')).convert_alpha()
	Textures['bullet'] = image.load(get('bullet.png')).convert()
	Textures['bullet'].set_colorkey((255,255,255))
	Textures['select_icon'] = image.load(get('select_icon.png')).convert_alpha()
	Textures['powerbar_back'] = image.load(get('power_bar_back.png')).convert_alpha()
	Textures['powerbar'] = image.load(get('power_bar.png')).convert_alpha()

	# Menu
	Textures['menu'] = image.load(get('back.png')).convert()
	Textures['play'] = image.load(get('Play.png')).convert_alpha()
	Textures['replay'] = image.load(get('replay.png')).convert_alpha()
	Textures['exit'] = image.load(get('Exit.png')).convert_alpha()

	# Sprite/Animations Poule - Sovanarit
	poule = get("poule.png")
	Textures['poulet'] = [

	SpriteStripAnim(poule, (96,128,32,32), 1, (181,230,29), True) +
	SpriteStripAnim(poule, (128,128,32,32), 1, (181,230,29), True)+
        SpriteStripAnim(poule, (160,128,32,32), 1, (181,230,29), True),

        SpriteStripAnim(poule, (96,160,32,32), 1, (181,230,29), True) +
	SpriteStripAnim(poule, (128,160,32,32), 1, (181,230,29), True)+
        SpriteStripAnim(poule, (160,160,32,32), 1, (181,230,29), True),

        SpriteStripAnim(poule, (96,192,32,32), 1, (181,230,29), True)+
	SpriteStripAnim(poule, (128,192,32,32), 1, (181,230,29), True)+
        SpriteStripAnim(poule, (160,192,32,32), 1, (181,230,29), True),

        SpriteStripAnim(poule, (96,224,32,32), 1, (181,230,29), True) +
	SpriteStripAnim(poule, (128,224,32,32), 1, (181,230,29), True)+
        SpriteStripAnim(poule, (160,224,32,32), 1, (181,230,29), True),

        SpriteStripAnim(poule, (96,128,32,32), 1, (181,230,29), True),
        #animation k_up stop 4

        SpriteStripAnim(poule, (96,160,32,32), 1, (181,230,29), True),
        #5

        SpriteStripAnim(poule, (96,192,32,32), 1, (181,230,29), True),
        #6

        SpriteStripAnim(poule, (96,224,32,32), 1, (181,230,29), True),
	]

	# Sprite/Animations Missile - Sovanarit
	missile = get("LargeMissiles.png")
	Textures['missile'] = [

        SpriteStripAnim(missile, (0,0,78,40),7,(63,143,255), True)+
        SpriteStripAnim(missile, (0,49,78,40),6,(63,143,255), True),

	]

	# Sprite-sheets Explosion
	Textures['exp_sheet'] = get_sheet((64, 64), 16, 4, (0, 0), 'exp_sheet.png')

	# Sounds de tire ancien
	Sounds['bullet'] = get_sound(1.0, 'hi_hat.wav')


	# Fonts - police d'ecriture
	Fonts['default'] = font.SysFont('None', 16)
	Fonts['32'] = font.SysFont('None',64)
