import pygame
import math
from random import randint, choice
import menu
import mobs


class Vague:
    def __init__(self, ecran_jeu):
        self.ecran_jeu = ecran_jeu
        self.lvl = 1
        self.chrono = 0
        self.prec_add = randint(200, 400)
        self.skibidis_ingame = []
        self.skibidis_outgame = []

    def __contains__(self, skibidi): #on admet que skibidi est ennemi
        for skibidis in self.skibidis_ingame:
            if type(skibidis) == type(skibidi):
                #print('yes')
                return True
        return False


    def add(self, skibidi, tempo):
        self.skibidis_outgame.append([skibidi, tempo])

    def troupe_mini_skibidi(self, nb, x, y, speed, lvl):
        for i in range(nb):
            self.add(mobs.Mini_skibidi(self.ecran_jeu, x, y, speed, (self.ecran_jeu.camera.x, self.ecran_jeu.camera.y), lvl),
                     i * mobs.Mini_skibidi(self.ecran_jeu, -1, -1, -1, (-1, -1), 1).largeur / speed)

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
            if skibidi.vie_act <= 0:
                self.ecran_jeu.score += skibidi.score
                self.skibidis_ingame.pop(i)
                self.ecran_jeu.music.son_dead_skibidi.play()
            i += 1
        self.prec_add -= 1
        self.infinite_vague()

    def infinite_vague(self):
        if self.chrono == 3000:
            self.add(mobs.Skibidi_boss(self.ecran_jeu, randint(0, self.ecran_jeu.largeur), randint(5, 200), 1, self.lvl), 0)
            self.lvl += 1
            self.chrono = 0
            print(str(self.lvl))
        elif not(mobs.Skibidi_boss(self.ecran_jeu, -100, -100, 0, self.lvl) in self):
            if self.prec_add <= 0:
                #print('why')
                self.prec_add = randint(round(200-self.chrono*0.01), round(400-self.chrono*0.01))
                if randint(0, 4) == 0:
                    self.add(mobs.Large_skibidi(self.ecran_jeu, randint(0, self.ecran_jeu.largeur), randint(5, 200), 1, self.lvl), 0)
                else:
                    self.troupe_mini_skibidi(7, choice((-100, self.ecran_jeu.largeur+100)), self.ecran_jeu.hauteur - randint(350, 500), 4, self.lvl)
            self.chrono += 1
        self.ecran_jeu.score += 2


class Vie:
    def __init__(self, entity):
        self.entity = entity
        self.vie_img = pygame.image.load('images_de _devellopement/img_vie.png')
        self.vie_img = pygame.transform.scale(self.vie_img, (self.entity.largeur, 5))

    def act_regen(self):
        if self.entity.precedent_regen <= 0 and self.entity.vie_act < self.entity.vie_max:
            self.entity.vie_act += self.entity.regen
            self.entity.precedent_regen = self.entity.delay_regen
        self.entity.precedent_regen -= 1

    def act_img(self):
        self.vie_img = pygame.transform.scale(self.vie_img,
                                              (self.entity.vie_act / self.entity.vie_max * self.entity.largeur, 5))
        self.entity.ecran_jeu.screen.blit(self.vie_img, (self.entity.x, self.entity.y + self.entity.hauteur + 5))


class Sound:  # il faudra changer les son et leurs volumes
    def __init__(self):
        self.music = pygame.mixer.Sound("sons/bruitdefond2.mp3")  # il exiset aussi "bruitdefond"
        self.music.set_volume(0.5)
        self.music.play(-1)
        self.son_dead_skibidi = pygame.mixer.Sound("sons/mortennemie.mp3")
        self.son_dead_skibidi.set_volume(0.5)
        self.sound_bullet = pygame.mixer.Sound("sons/chasse d'eau.mp3")
        self.sound_bullet.set_volume(0.1)
        self.son_menu = pygame.mixer.Sound("sons/chasse d'eau.mp3")
        self.son_menu.set_volume(0.1)
        self.son_click = pygame.mixer.Sound("sons/chasse d'eau.mp3")
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
        self.degats = 10
        self.speed = speed
        self.largeur = 90
        self.hauteur = 47
        self.img = pygame.image.load('images_de _devellopement/camera.png').convert_alpha()
        self.x = 275
        self.y = 500
        #bullets
        self.bullet_img = pygame.image.load('images_de _devellopement/bullet.png').convert_alpha()
        self.bullets = []  # liste des balles en train d'etre tirées
        self.cadence_tir = 25  # a ameliorer mais fonctionel (1 tir toutes les 25 images 50 images par sec)
        self.precedent_tir = self.cadence_tir
        self.NotGetToMuchDamage = 0
        # vie/regen
        self.vie_act = 100   # 1000000
        self.vie_max = self.vie_act
        self.delay_regen_dmg = 250  # 0
        self.delay_regen = 100  # 1
        self.precedent_regen = self.delay_regen
        self.regen = 1  # 10000
        self.vie = Vie(self)

    def add_bullet(self):
        if self.precedent_tir >= self.cadence_tir:
            self.bullets.append(Bullet_friendly(self.x + 30, self.y + 10, self.degats, 1))
            self.precedent_tir = 0
            self.ecran_jeu.music.sound_bullet.play()

    def touche(self, skibidis):
            for skibidi in skibidis:
                if (
                        skibidi.x + skibidi.largeur >= self.x >= skibidi.x and (
                        skibidi.y + skibidi.hauteur >= self.y >= skibidi.y or skibidi.y + skibidi.hauteur >= self.y + self.hauteur >= skibidi.y) or (
                        skibidi.x + skibidi.largeur >= self.x + self.largeur >= skibidi.x and (
                        skibidi.y + skibidi.hauteur >= self.y >= skibidi.y or skibidi.y + skibidi.hauteur >= self.y + self.hauteur >= skibidi.y)) or (
                        self.x <= skibidi.x <= self.x + self.largeur and (
                        self.y <= skibidi.y <= self.y + self.hauteur or self.y <= skibidi.y <= self.y + self.hauteur)) or (
                        self.x <= skibidi.x <= self.x + self.largeur and (
                        self.y <= skibidi.y <= self.y + self.hauteur or self.y <= skibidi.y <= self.y + self.hauteur))) and (
                        skibidi.dmg_timer <= 0
                ):
                    skibidi.dmg_timer = skibidi.dmg_timer_init
                    self.vie_act -= skibidi.degat
                    self.y += skibidi.speed  # knockback
                    self.NotGetToMuchDamage = 20
                    self.precedent_regen = self.delay_regen_dmg
                    print('oh no')
            #print(self.vie_act)

    def act_bullet(self):
        for bullet in self.bullets:
            bullet.y -= 20
            if bullet.y < 0 or bullet.pene <= 0:
                self.bullets.pop(0)
            else:
                self.ecran_jeu.screen.blit(self.bullet_img, (bullet.x, bullet.y))
        self.precedent_tir += 1

    def act_img(self):
        self.vie.act_img()
        self.touche(self.ecran_jeu.vague.skibidis_ingame)
        self.vie.act_regen()
        self.act_bullet()
        self.y += self.ecran_jeu.fond[0].speed
        self.ecran_jeu.screen.blit(self.img, (self.x, self.y))


class Back:
    def __init__(self, ecran_jeu, y):
        self.fond = pygame.image.load('images_de _devellopement/fond.jpg').convert()
        self.fond = pygame.transform.scale(self.fond, (ecran_jeu.largeur, 320))
        self.y = y
        self.hauteur = 320
        self.speed = 1

    def act_img(self):
        self.y += self.speed
        if self.y > 2 * self.hauteur:
            self.y -= 3 * self.hauteur


class Ecran_jeu:
    def __init__(self, largeur, hauteur):
        pygame.init()
        pygame.display.set_caption("jeu")
        self.clock = pygame.time.Clock()
        self.score = 0

        self.largeur = largeur
        self.hauteur = hauteur
        self.screen = pygame.display.set_mode((largeur, hauteur))
        self.fond = []
        for i in range(hauteur // 80):
            self.fond.append(Back(self, i * 320))
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
                    #self.vague.troupe_mini_skibidi(7, -100, self.hauteur - 350, 4)y
                    self.vague.troupe_mini_skibidi(7, choice((-100,self.largeur+100)), self.hauteur - randint(350, 500),4,1)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    self.vague.add(mobs.Large_skibidi(self, randint(0, self.largeur), randint(5, 200), 1, 1), 50)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                    self.vague.add(mobs.Skibidi_boss(self, randint(0, self.largeur), randint(5, 200), 1, 1), 50)

            self.camera.add_bullet()
            if right and self.camera.x < self.largeur - 34:
                self.camera.x += self.camera.speed
            if left and self.camera.x > -25:
                self.camera.x -= self.camera.speed
            if up and self.camera.y > 0:  # and self.camera.y > self.hauteur - 200:
                self.camera.y -= self.camera.speed
            if self.camera.y < self.hauteur - self.camera.hauteur/2:
                if down:
                    self.camera.y += self.camera.speed
            else: self.camera.y = self.hauteur - self.camera.hauteur/2

            for back in self.fond:
                back.act_img()
                self.screen.blit(back.fond, (0, back.y))

            self.vague.act_img()
            self.camera.act_img()
            if self.camera.vie_act <= 0:
                continuer = False
                print('dead')
            self.screen.blit(pygame.font.Font(None, 50).render(str(self.score), True, (0,0,0)),(0,0))
            print(self.score)
            pygame.display.update()
            self.clock.tick(50)

def jeu():
    game = True
    while game:
        largeur = 600
        hauteur = 600
        menue = menu.Menu()
        if menue.main_menu():
            ecran_jeu = Ecran_jeu(largeur, hauteur)
            ecran_jeu.boucle_run()
        else:
            game = False

jeu()


# bar espace pour tirer
# fleches pour se deplacer
# n pour ajouter des ennemis
# ennemis bougent en largeur de 100 pixels et avancent petit a petit
# et se font eliminer lorsqu'ils touchent une balle
