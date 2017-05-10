import os
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


data_folder = os.path.join(os.getcwd(), 'data')

def get(*path):
	return os.path.join(data_folder, *path)


def get_sound(volume, *path):
	sound = mixer.Sound(get(*path))
	sound.set_volume(volume)
	return sound



Textures = dict()
Fonts = dict()
Sounds = dict()


def init_ressources():
	# Chargement des images, et conversion pour l'usage de pygame
	Textures['sky'] = image.load(get('sky.png')).convert()
	Textures['sky2'] = image.load(get('sky_2.png')).convert()
	Textures['ground'] = image.load(get('ground.png')).convert_alpha()
#	Textures['explosion'] = image.load(get('explosion.png')).convert_alpha()
	Textures['player'] = image.load(get('player.png')).convert_alpha()
	Textures['bullet'] = image.load(get('bullet.png')).convert()
	Textures['bullet'].set_colorkey((255,255,255))

	Textures['menu'] = image.load(get('back.png')).convert()
	Textures['play'] = image.load(get('Play.png')).convert_alpha()
	Textures['exit'] = image.load(get('Exit.png')).convert_alpha()

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

	missile = get("LargeMissiles.png")
	Textures['missile'] = [

        SpriteStripAnim(missile, (0,0,78,40),7,(63,143,255), True)+
        SpriteStripAnim(missile, (0,49,78,40),6,(63,143,255), True),

	]

	# Sprite-sheets
	Textures['exp_sheet'] = get_sheet((64, 64), 16, 4, (0, 0), 'exp_sheet.png')

	# Sounds
	Sounds['bullet'] = get_sound(1.0, 'hi_hat.wav')


	# Fonts
	Fonts['default'] = font.SysFont('None', 16)

