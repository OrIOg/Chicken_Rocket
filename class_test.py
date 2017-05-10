import pygame

pygame.init()

running=True
size = width, height = 512, 512
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()

backgroundcolour = (255, 255, 255)

#############################################

class Bullet():
    def __init__(self, pos, accel):

        self.position = pos
        self.acceleration = accel

    def gravity(self, delta_time):
        self.acceleration[1] += 1000 * delta_time

    def update(self, delta_time):
        self.gravity(delta_time)
        self.position[0] += self.acceleration[0] * delta_time
        self.position[1] += self.acceleration[1] * delta_time

    def draw(self, screen):
        pygame.draw.circle(screen, (0,0,255), (int(self.position[0]), int(self.position[1])), 15)

#############################################

getting_power = False

X = 0
mult = 0
    
def draw_powerbar(screen):   
    pygame.draw.rect(screen,(0,0,255),(256,256, 200,50))
    global X
    global mult
    X += 0.01
    mult = abs(sin(X))
    pygame.draw.rect(screen,(255,0,0),(256,256, mult*200,50))
    pygame.display.update()

bullets_group = []

PUISSANCE = 1000

cooldown = 0.0

pygame.mixer.music.load("K:/Docs/Downloads/SMAW Rocket Launcher Sound Effects.mp3")
pygame.mixer.music.set_volume(0.8)

from math import cos, sin

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        elif event.type == pygame.MOUSEBUTTONDOWN and cooldown <= 0:
            getting_power = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if getting_power and cooldown <= 0:
                getting_power = False
                cooldown = 1.0
                pygame.mixer.music.play(0,0)
                mouseX, mouseY = pygame.mouse.get_pos()
                bullets_group.append(Bullet([mouseX, mouseY], [PUISSANCE*mult*cos(45),-PUISSANCE*mult*sin(45)]))
                X = 0
            
    delta_time = clock.tick() * 0.001
    if cooldown > 0:
        cooldown -= delta_time

    for bullet in bullets_group:
        bullet.update(delta_time)

    screen.fill(backgroundcolour)
    
    for bullet in bullets_group:
        bullet.draw(screen)

    if getting_power:
        draw_powerbar(screen)

    pygame.display.update()

