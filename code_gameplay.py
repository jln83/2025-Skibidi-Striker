import pygame
import math
from random import randint
import subprocess
import sys

# import mobs


# Mobs:

class Mini_skibidi:
    def __init__(self, ecran_jeu, x, y, speed, target):
        self.ecran_jeu = ecran_jeu
        self.memox = x
        self.memoy = y
        self.x = x
        self.y = y
        self.img_tete = pygame.image.load('images_de _devellopement/tete_skibidi.png').convert_alpha()
        self.img_toilettes = pygame.image.load('images_de _devellopement/toilette_sanst_tete.png').convert_alpha()
        self.img_tete = pygame.transform.scale(self.img_tete, (60, 60))
        self.img_toilettes = pygame.transform.scale(self.img_toilettes, (60, 60))
        self.largeur = 65
        self.hauteur = 65
        self.speed = speed
        self.target_x = target[0]
        self.target_y = target[1]
        self.vie = 15
        self.degat = 5

    def act_img(self):
        if self.x > self.target_x > self.memox:
            self.memox = self.ecran_jeu.largeur - self.memox
        self.ecran_jeu.screen.blit(self.img_toilettes, (self.x, self.y))
        self.ecran_jeu.screen.blit(self.img_tete, (self.x, self.y))

        dx = (self.x - self.target_x) / (self.target_x - self.memox)
        self.x += self.speed  # * abs(self.target_x-self.memox)/300 # deux version selon celle voulue enlever #
        self.y = (self.memoy - self.target_y) * dx ** 2 + self.target_y

    def touche(self, bullets):
        for bullet in bullets:
            if self.x <= bullet.x <= self.x + self.largeur and self.y <= bullet.y <= self.y + self.hauteur:
                self.vie -= bullet.damage
                bullet.pene -= 1


class Bullet_Ennemi:
    def __init__(self, ecran_jeu, x, y, degat, pene, speed):
        self.ecran_jeu = ecran_jeu
        self.img = pygame.image.load('images_de _devellopement/bullet.png').convert_alpha()
        self.x = x
        self.y = y
        self.speed = speed
        self.degat = degat
        self.vie = pene
        self.largeur = 1
        self.hauteur = 1

    def act_img(self):
        self.y += self.speed
        self.ecran_jeu.screen.blit(self.img, (self.x, self.y))

    def touche(self, bullets):
        pass


class Large_skibidi:
    def __init__(self, ecran_jeu, x, y, speed):
        self.ecran_jeu = ecran_jeu
        self.x = x
        self.y = y
        self.speed = speed
        self.target_x = randint(0, ecran_jeu.largeur)
        self.target_y = randint(5, 200)
        self.img = pygame.image.load('images_de _devellopement/boss4.png').convert_alpha()
        self.img = pygame.transform.scale(self.img, (125, 125))
        self.largeur = 125
        self.hauteur = 125
        self.vie = 100
        self.degat = 10
        self.cadence_tir = 50  # a ameliorer mais fonctionel (1 tir toutes les 25 images 50 images par sec)
        self.precedent_tir = self.cadence_tir

    def add_bullet(self):
        if self.precedent_tir <= 0:
            self.ecran_jeu.vague.add(Bullet_Ennemi(self.ecran_jeu, self.x + 60, self.y + 110, self.degat, 1, 5), 0)
            self.precedent_tir = self.cadence_tir
        self.precedent_tir -= 1

    def act_img(self):
        temp_x = self.speed * (self.target_x - self.x)
        temp_y = self.speed * (self.target_y - self.y)
        distance = math.sqrt(temp_x ** 2 + temp_y ** 2)
        temp_x /= distance
        temp_y /= distance
        self.x += temp_x * self.speed
        self.y += temp_y * self.speed
        if abs(self.x-self.target_x) < 1 and abs(self.y-self.target_y) < 1:
            self.target_x = randint(0, self.ecran_jeu.largeur-125)
            self.target_y = randint(5, 200)
        self.add_bullet()
        self.ecran_jeu.screen.blit(self.img, (self.x, self.y))

    def touche(self, bullets):
        for bullet in bullets:
            if self.x <= bullet.x <= self.x + self.largeur and self.y <= bullet.y <= self.y + self.hauteur:
                self.vie -= bullet.damage
                bullet.pene -= 1


# fin mobs
class Vague:
    def __init__(self, ecran_jeu):
        self.ecran_jeu = ecran_jeu
        self.skibidis_ingame = []
        self.skibidis_outgame = []

    def add(self, skibidi, tempo):
        self.skibidis_outgame.append([skibidi, tempo])

    def troupe_mini_skibidi(self, nb, x, y, speed):
        for i in range(nb):
            self.add(Mini_skibidi(self.ecran_jeu, x, y, speed, (self.ecran_jeu.camera.x, self.ecran_jeu.camera.y)),
                     i * Mini_skibidi(self.ecran_jeu, -1, -1, -1, (-1, -1)).largeur / speed)

    def act_img(self):
        i = 0
        for skibidi in self.skibidis_outgame:
            if skibidi[1] <= 0:
                self.skibidis_outgame.pop(i)
                self.skibidis_ingame.append(skibidi[0])
            skibidi[1] -= 1
            i += 1
        i = 0
        for skibidi in self.skibidis_ingame:
            skibidi.act_img()
            skibidi.touche(self.ecran_jeu.camera.bullets)
            if skibidi.vie <= 0:
                self.skibidis_ingame.pop(i)
                self.ecran_jeu.music.son_dead_skibidi.play()
            i += 1


class Sound:  # il faudra changer les son et leurs volumes
    def __init__(self):
        self.music = pygame.mixer.Sound("sons/bruitdefond2.mp3")#il exiset aussi "bruitdefond"
        self.music.set_volume(0.5)
        self.music.play(-1)
        self.son_dead_skibidi = pygame.mixer.Sound("sons/mortennemie.mp3")
        self.son_dead_skibidi.set_volume(0.5)
        self.sound_bullet = pygame.mixer.Sound("sons/chasse d'eau.mp3")
        self.sound_bullet.set_volume(0.1)
        self.son_menu=pygame.mixer.Sound("sons/chasse d'eau.mp3")
        self.son_menu.set_volume(0.1)
        self.son_click=pygame.mixer.Sound("sons/chasse d'eau.mp3")
        self.son_click.set_volume(0.1)



class Bullet_friendly:
    def __init__(self, x, y, damage, pene):
        self.x = x
        self.y = y
        self.damage = damage
        self.pene = pene


class Camera:  # joueur
    def __init__(self, ecran_jeu, speed):
        self.ecran_jeu = ecran_jeu
        self.vie = 100
        self.vie_max = self.vie
        self.degats = 10
        self.speed = speed
        self.largeur = 90
        self.hauteur = 47
        self.img = pygame.image.load('images_de _devellopement/camera.png').convert_alpha()
        self.bullet_img = pygame.image.load('images_de _devellopement/bullet.png').convert_alpha()
        self.vie_img = pygame.image.load('images_de _devellopement/img_vie.png')
        self.vie_img = pygame.transform.scale(self.vie_img, (self.largeur, 5))
        self.bullets = []  # liste des balles en train d'etre tirées
        self.x = 275
        self.y = 500
        self.cadence_tir = 25  # a ameliorer mais fonctionel (1 tir toutes les 25 images 50 images par sec)
        self.precedent_tir = self.cadence_tir
        self.NotGetToMuchDamage = 0
        self.delay_regen_dmg = 250
        self.delay_regen = 100
        self.precedent_regen = self.delay_regen
        self.regen = 1

    def add_bullet(self):
        if self.precedent_tir >= self.cadence_tir:
            self.bullets.append(Bullet_friendly(self.x + 30, self.y + 10, self.degats, 1))
            self.precedent_tir = 0
            self.ecran_jeu.music.sound_bullet.play()

    def touche(self, skibidis):
        if self.NotGetToMuchDamage <= 0:
            for skibidi in skibidis:
                if (
                        skibidi.x + skibidi.largeur >= self.x >= skibidi.x and (
                        skibidi.y + skibidi.hauteur >= self.y >= skibidi.y or skibidi.y + skibidi.hauteur >= self.y + self.hauteur >= skibidi.y) or (
                        skibidi.x + skibidi.largeur >= self.x + self.largeur >= skibidi.x and (
                        skibidi.y + skibidi.hauteur >= self.y >= skibidi.y or skibidi.y + skibidi.hauteur >= self.y + self.hauteur >= skibidi.y)) or (
                        self.x <= skibidi.x <= self.x + self.largeur and (
                        self.y <= skibidi.y <= self.y + self.hauteur or self.y <= skibidi.y <= self.y + self.hauteur)) or (
                        self.x <= skibidi.x <= self.x + self.largeur and (
                        self.y <= skibidi.y <= self.y + self.hauteur or self.y <= skibidi.y <= self.y + self.hauteur))):

                    self.vie -= skibidi.degat
                    self.y += skibidi.speed  # knockback
                    self.NotGetToMuchDamage = 20
                    self.precedent_regen = self.delay_regen_dmg
        self.NotGetToMuchDamage -= 1
        print(self.vie)

    def act_bullet(self):
        for bullet in self.bullets:
            bullet.y -= 20
            if bullet.y < 0 or bullet.pene <= 0:
                self.bullets.pop(0)
            else:
                self.ecran_jeu.screen.blit(self.bullet_img, (bullet.x, bullet.y))
        self.precedent_tir += 1

    def act_regen(self):
        if self.precedent_regen <= 0 and self.vie < self.vie_max:
            self.vie += self.regen
            self.precedent_regen = self.delay_regen
        self.precedent_regen -= 1

    def act_img_vie(self):
        self.vie_img = pygame.transform.scale(self.vie_img, (self.vie/self.vie_max*self.largeur, 5))
        self.ecran_jeu.screen.blit(self.vie_img, (self.x, self.y + self.hauteur + 5))

    def act_img(self):
        self.act_img_vie()
        self.touche(self.ecran_jeu.vague.skibidis_ingame)
        self.act_regen()
        self.act_bullet()
        self.ecran_jeu.screen.blit(self.img, (self.x, self.y))



class Back:
    def __init__(self,ecran_jeu, y):
        self.fond = pygame.image.load('images_de _devellopement/fond.jpg').convert()
        self.fond = pygame.transform.scale(self.fond, (ecran_jeu.largeur, 320))
        self.y = y
        self.hauteur = 320
        self.speed = 5

    def act_img(self):
        self.y += self.speed
        if self.y > 2 * self.hauteur:
            self.y -= 3 * self.hauteur


class ecran_jeu:
    def __init__(self, largeur, hauteur):
        pygame.init()
        pygame.display.set_caption("jeu")
        self.clock = pygame.time.Clock()

        self.largeur = largeur
        self.hauteur = hauteur
        self.screen = pygame.display.set_mode((largeur, hauteur))
        self.fond = []
        for i in range(hauteur // 80):
            self.fond.append(Back(self,i * 320))
        self.music = Sound()

    def boucle_run(self):
        self.camera = Camera(self, 5)
        self.vague = Vague(self)
        right = False
        left = False
        up = False
        down = False
        bullet = False

        continuer = True
        while continuer:
            # test touches appuyées
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    # subprocess.Popen(["python", "menu.py"])
                # Quitter le programme actuel
                    running = False
                    pygame.quit()
                    sys.exit()
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
                    self.vague.troupe_mini_skibidi(7, -100, self.largeur - 350, 4)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    self.vague.add(Large_skibidi(self, randint(0, self.largeur), randint(5, 200), 1), 50)

            if bullet:
                self.camera.add_bullet()
            if right and self.camera.x < self.largeur - 34:
                self.camera.x += self.camera.speed
            if left and self.camera.x > -25:
                self.camera.x -= self.camera.speed
            if up and self.camera.y > self.hauteur - 200:
                self.camera.y -= self.camera.speed
            if down and self.camera.y < self.hauteur - 25:
                self.camera.y += self.camera.speed

            for back in self.fond:
                back.act_img()
                self.screen.blit(back.fond, (0, back.y))

            self.vague.act_img()
            self.camera.act_img()
            if self.camera.vie <= 0:
                continuer = False
                print('dead')
            pygame.display.update()
            self.clock.tick(50)
            
        

            



largeur =  600
hauteur = 600
ecran_jeu = ecran_jeu(largeur, hauteur)
ecran_jeu.boucle_run()

# bar espace pour tirer
# fleches pour se deplacer
# n pour ajouter des ennemis
# ennemis bougent en largeur de 100 pixels et avancent petit a petit
# et se font eliminer lorsqu'ils touchent une balle
