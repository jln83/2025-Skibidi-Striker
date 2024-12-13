import pygame
import math
from random import randint


# import mobs


# Mobs:

class Mini_skibidi:
    def __init__(self, x, y, speed, target):
        self.memox = x
        self.memoy = y
        self.x = x
        self.y = y
        self.img_tete = pygame.image.load('images_de _devellopement/tete_skibidi.png').convert_alpha()
        self.img_toilettes = pygame.image.load('images_de _devellopement/toilette_sanst_tete.png').convert_alpha()
        self.largeur = 90
        self.hauteur = 90
        self.speed = speed
        self.target_x = target[0]
        self.target_y = target[1]
        self.vie = 15
        self.degat = 5

    def act_img(self):
        if self.x > self.target_x > self.memox:
            self.memox = ecran_jeu.largeur - self.memox
        ecran_jeu.screen.blit(self.img_toilettes, (self.x, self.y))
        ecran_jeu.screen.blit(self.img_tete, (self.x, self.y))

        dx = (self.x - self.target_x) / (self.target_x - self.memox)
        self.x += self.speed  #* abs(self.targetx-self.memox)/300 #deux version selon celle voulue enlever #
        self.y = (self.memoy - self.target_y) * dx ** 2 + self.target_y

    def touche(self, bullets):
        for bullet in bullets:
            if self.x <= bullet.x <= self.x + self.largeur and self.y <= bullet.y <= self.y + self.hauteur:
                self.vie -= bullet.damage
                bullet.pene -= 1



class Large_skibidi:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.target_x = randint(0, ecran_jeu.largeur)
        self.target_y = randint(5, 200)
        self.img = pygame.image.load('images_de _devellopement/large_skibidi.png').convert_alpha()
        self.img = pygame.transform.scale(self.img, (125, 125))
        self.largeur = 125
        self.hauteur = 125
        self.vie = 100
        self.degat = 10

    def act_img(self):
        temp_x = self.speed * (self.target_x - self.x)
        temp_y = self.speed * (self.target_y - self.y)
        distance = math.sqrt(temp_x ** 2 + temp_y ** 2)
        temp_x /= distance
        temp_y /= distance
        self.x += temp_x * self.speed
        self.y += temp_y * self.speed
        if abs(self.x-self.target_x) < 1 and abs(self.y-self.target_y) < 1:
            self.target_x = randint(0, ecran_jeu.largeur-125)
            self.target_y = randint(5, 200)


        ecran_jeu.screen.blit(self.img, (self.x, self.y))

    def touche(self, bullets):
        for bullet in bullets:
            if self.x <= bullet.x <= self.x + self.largeur and self.y <= bullet.y <= self.y + self.hauteur:
                self.vie -= bullet.damage
                bullet.pene -= 1


#fin mobs
class Vague:
    def __init__(self):
        self.skibidis_ingame = []
        self.skibidis_outgame = []

    def add(self, skibidi, tempo):
        self.skibidis_outgame.append([skibidi, tempo])

    def troupe_mini_skibidi(self, nb, x, y, speed):
        for i in range(nb):
            self.add(Mini_skibidi(x, y, speed, (camera.x, camera.y)),
                     i * Mini_skibidi(-1, -1, -1, (-1, -1)).largeur / speed)

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
            skibidi.touche(camera.bullets)
            if skibidi.vie <= 0:
                self.skibidis_ingame.pop(i)
                ecran_jeu.music.son_dead_skibidi.play()
            i += 1


class Sound: # il faudra changer les son et leurs volumes
    def __init__(self):
        self.music = pygame.mixer.Sound("sons/son skibidi.mp3")
        self.music.set_volume(0.5)
        #self.music.play(-1)
        self.son_dead_skibidi = pygame.mixer.Sound("sons/chasse d'eau.mp3")
        self.son_dead_skibidi.set_volume(0.5)
        self.sound_bullet = pygame.mixer.Sound("sons/chasse d'eau.mp3")
        self.sound_bullet.set_volume(0.1)



class Bullet_friendly:
    def __init__(self, x, y, damage, pene):
        self.x = x
        self.y = y
        self.damage = damage
        self.pene = pene


class Camera:  # joueur
    def __init__(self, speed):
        self.vie = 100
        self.vie_max = self.vie
        self.degats = 10
        self.speed = speed
        self.largeur = 90
        self.hauteur = 47
        self.img = pygame.image.load('images_de _devellopement/camera.png').convert_alpha()
        self.bullet_img = pygame.image.load('images_de _devellopement/bullet.png').convert_alpha()
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
            ecran_jeu.music.sound_bullet.play()



    def touche(self, skibidis):
        if self.NotGetToMuchDamage <= 0:
            for skibidi in skibidis:
                if (
                        skibidi.x + skibidi.largeur >= self.x >= skibidi.x and skibidi.y + skibidi.hauteur >= self.y >= skibidi.y) or (
                        skibidi.x + skibidi.largeur >= self.x + self.largeur >= skibidi.x and skibidi.y + skibidi.hauteur >= self.y + self.hauteur >= skibidi.y):
                    self.vie -= skibidi.degat
                    self.y += skibidi.speed  # knockback
                    self.NotGetToMuchDamage = 20
                    self.precedent_regen = self.delay_regen_dmg
        self.NotGetToMuchDamage -= 1
        print(self.vie)

    def act_regen(self):
        if self.precedent_regen <= 0 and self.vie < self.vie_max:
            self.vie += self.regen
            self.precedent_regen = self.delay_regen
        self.precedent_regen -= 1

    def act_img(self):
        ecran_jeu.screen.blit(self.img, (self.x, self.y))
        self.touche(ecran_jeu.vague.skibidis_ingame)
        self.act_regen()
        for bullet in self.bullets:
            bullet.y -= 20
            if bullet.y < 0 or bullet.pene <= 0:
                self.bullets.pop(0)
            else:
                ecran_jeu.screen.blit(self.bullet_img, (bullet.x, bullet.y))
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
        self.vague = Vague()
        self.music = Sound()


    def boucle_run(self):
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
                    self.vague.troupe_mini_skibidi(7, -100, ecran_jeu.largeur - 350, 4)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    self.vague.add(Large_skibidi(randint(0, self.largeur), randint(5, 200), 1), 50)

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
            self.vague.act_img()
            camera.act_img()
            if camera.vie <= 0:
                continuer = False
                print('dead')
            pygame.display.update()
            self.clock.tick(50)



largeur = 600
hauteur = 600
ecran_jeu = ecran_jeu(largeur, hauteur)
camera = Camera(5)
ecran_jeu.boucle_run()

# bar espace pour tirer
# fleches pour se deplacer
# n pour ajouter des ennemis
# ennemis bougent en largeur de 100 pixels et avancent petit a petit
# et se font eliminer lorsqu'ils touchent une balle
