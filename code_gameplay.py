import pygame
import mobs
import math
from random import randint





# Mobs:

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
        if (self.target_x-self.x)**2+(self.target_y-self.y) >=0: #au cas ou c'est nul pour pas que ça crash
            distance = math.sqrt((self.target_x-self.x)**2+(self.target_y-self.y))
        else:
            distance = 0
        if distance > 5:
            delta_x = self.target_x - self.x
            delta_y = self.target_y - self.y

            direction_x = delta_x / distance
            direction_y = delta_y / distance

            self.x += direction_x * self.speed
            self.y += direction_y * self.speed
        else:
            self.target_x = randint(0, ecran_jeu.largeur)
            self.target_y = randint(5,200)

        ecran_jeu.screen.blit(self.img, (self.x, self.y))



class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def touche(self):
        for i in range(len(ecran_jeu.skibidis)):
            if ecran_jeu.skibidis[i].x + 60 > self.x > ecran_jeu.skibidis[i].x and ecran_jeu.skibidis[i].y + 60 > self.y > ecran_jeu.skibidis[i].y:
                ecran_jeu.skibidis.pop(i)
                break


class Camera:  # joueur
    def __init__(self, health, damages, speed):
        self.vie = health
        self.degats = damages
        self.speed = speed
        self.img = pygame.image.load('images_de _devellopement/camera.png').convert_alpha()
        self.bullet_img = pygame.image.load('images_de _devellopement/bullet.png').convert_alpha()
        self.bullets = []  # liste des balles en train d'etre tirées
        self.x = 275
        self.y = 500
        self.cadence_tir = 10  # a ameliorer mais fonctionel (1 tir toutes les dix images)
        self.precedent_tir = self.cadence_tir

    def add_bullet(self):
        if self.precedent_tir >= self.cadence_tir:
            self.bullets.append(Bullet(self.x + 24, self.y + 10))
            self.precedent_tir = 0

    def act_img(self):
        ecran_jeu.screen.blit(self.img, (self.x, self.y))
        for bullet in self.bullets:
            bullet.y -= 20
            if bullet.y < 0:
                self.bullets.pop(0)
            else:
                ecran_jeu.screen.blit(self.bullet_img, (bullet.x, bullet.y))
                bullet.touche()
        self.precedent_tir += 1



class Back:
    def __init__(self, y):
        self.fond = pygame.image.load('images_de _devellopement/fond.jpg').convert()
        self.y = y
        self.hauteur = 320
        self.speed = 5

    def act_img(self):
        self.y += self.speed
        if self.y > 2 * self.hauteur:
            self.y -= 3 * self.hauteur
        ecran_jeu.screen.blit(self.fond, (0, self.y))


class ecran_jeu:
    def __init__(self, largeur, hauteur):
        pygame.init()
        self.clock = pygame.time.Clock()

        self.largeur = largeur
        self.hauteur = hauteur
        self.screen = pygame.display.set_mode((largeur, hauteur))
        self.fond = []
        for i in range(hauteur // 80):
            self.fond.append(Back(i * 320))
        self.skibidis = []

    def boucle_run(self):
        right = False
        left = False
        up = False
        down = False
        bullet = False
        camera = Camera(100,10,10)

        continuer = True
        while continuer:
            # test touches appuyées
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    continuer = False
                if (event.type == pygame.KEYDOWN or event.type == pygame.KEYUP) and event.key == pygame.K_RIGHT:
                    right = event.type == pygame.KEYDOWN
                if (event.type == pygame.KEYDOWN or event.type == pygame.KEYUP) and event.key == pygame.K_LEFT:
                    left = event.type == pygame.KEYDOWN
                if (event.type == pygame.KEYDOWN or event.type == pygame.KEYUP) and event.key == pygame.K_UP:
                    up = event.type == pygame.KEYDOWN
                if (event.type == pygame.KEYDOWN or event.type == pygame.KEYUP) and event.key == pygame.K_DOWN:
                    down = event.type == pygame.KEYDOWN
                if (event.type == pygame.KEYDOWN or event.type == pygame.KEYUP) and event.key == pygame.K_SPACE:
                    bullet = event.type == pygame.KEYDOWN
                if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                    self.skibidis.append(Mini_skibidi(randint(0, self.largeur),-50,3))
                if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    self.skibidis.append(Large_skibidi(randint(0, self.largeur),randint(5,200),1.5))

            if bullet:
                camera.add_bullet()
            if right and camera.x < self.largeur - 34:
                camera.x += camera.speed
            if left and camera.x > -25:
                camera.x -= camera.speed
            if up and camera.y > self.hauteur - 200:
                camera.y -= camera.speed
            if down and camera.y < self.hauteur - 25:
                camera.y += camera.speed

            for back in self.fond:
                back.act_img()
            for skibidi in self.skibidis:
                skibidi.act_img()
            camera.act_img()
            pygame.display.update()
            self.clock.tick(50)


ecran_jeu: ecran_jeu = ecran_jeu(600, 600)
camera: camera=Camera(100,10,5)
ecran_jeu.boucle_run()

# bar espace pour tirer
# fleches pour se deplacer
# n pour ajouter des ennemis
# ennemis bougent en largeur de 100 pixels et avancent petit a petit
# et se font eliminer lorsqu'ils touchent une balle
