import spritesheet

# Gere les animations de sprites
class SpriteStripAnim(object):
    
    def __init__(self, filename, rect, count, colorkey=False, loop=False, frames=1):
        
        self.filename = filename
        # On recupere les images grace a spritesheet
        ss = spritesheet.spritesheet(filename)
        self.images = ss.load_strip(rect, count, colorkey)
        # On initialise & applique les parametres
        self.i = 0
        self.loop = loop
        self.frames = frames
        self.f = frames

    # Reinitialise
    def iter(self):
        self.i = 0
        self.f = self.frames
        return self

    # Recupere la prochaine image
    def next(self):
        # Si on depasse la derniere image
        if self.i >= len(self.images):
            if not self.loop:
                # On arrete
                raise StopIteration
            else:
                # On recommence
                self.i = 0
        # Set l'image de retour
        image = self.images[self.i]
        self.f -= 1
        # Si on ecoule le nb de frame, alors prochaine image, re-init le compteur
        if self.f == 0:
            self.i += 1
            self.f = self.frames
        return image

    # Permet d'utiliser '+' pour ajouter des images sur d'autres lignes
    def __add__(self, ss):
        self.images.extend(ss.images)
        return self
