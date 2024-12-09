import pygame
import math
from random import randint


class Mini_skibidi:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.img_tete = pygame.image.load('images_de _devellopement/tete_skibidi.png').convert_alpha()
        self.img_toilettes = pygame.image.load('images_de _devellopement/toilette_sanst_tete.png').convert_alpha()
        self.speedx = speed
        self.speedy = speed*2
        self.targetx = 0
        self.targety = 0

    def act_img(self):
        ecran_jeu.screen.blit(self.img_toilettes, (self.x, self.y))
        ecran_jeu.screen.blit(self.img_tete, (self.x, self.y))
        normx = self.targetx-self.x
        normy = self.targety-self.y
        d=math.sqrt(normx**2+normy**2)
        self.x += self.speedx*normx/d
        self.y += self.speedy*normy/d
        self.targetx=camera.x
        self.targety=camera.y

class Large_skibidi:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.target_x = randint(0, ecran_jeu.largeur)
        self.target_y = randint(5,200)
        self.img = pygame.image.load('images_de _devellopement/large_skibidi.png').convert_alpha()
        self.img = pygame.transform.scale(self.img,(125,125))

    def act_img(self):
        if abs(self.x - self.target_x) > 1: #or abs(self.y - self.target_y) > 1:
            temp_x = self.speed * (self.target_x - self.x)
            temp_y = self.speed * (self.target_y - self.y)
            distance = math.sqrt(temp_x**2 + temp_y**2)
            temp_x /= distance
            temp_y /= distance
            self.x += temp_x * self.speed
            self.y += temp_y * self.speed
        else: # RAHHH ça veut pas marcher ça jsp pourquoi dcp euh bah il bouge que une fois pour l'instant
            self.target_x = randint(0, ecran_jeu.largeur)
            self.target_y = randint(5,200)

        self.x = int(self.x)
        self.y = int(self.y)

        if 0 <= self.x <= ecran_jeu.largeur - 125 and 0 <= self.y <= ecran_jeu.hauteur - 125:
            ecran_jeu.screen.blit(self.img, (self.x, self.y))
