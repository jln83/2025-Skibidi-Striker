import pygame
import math
from random import randint, choice

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


class Mini_skibidi:
    def __init__(self, ecran_jeu, x, y, speed, target, lvl):
        self.ecran_jeu = ecran_jeu
        self.score = 1000
        self.memox = x
        self.memoy = y
        self.x = x
        self.y = y
        self.largeur = 65
        self.hauteur = 65
        self.img_tete = pygame.image.load('images_de _devellopement/tete_skibidi.png').convert_alpha()
        self.img_toilettes = pygame.image.load('images_de _devellopement/toilette_sanst_tete.png').convert_alpha()
        self.img_tete = pygame.transform.scale(self.img_tete, (self.largeur, self.hauteur))
        self.img_toilettes = pygame.transform.scale(self.img_toilettes, (self.largeur, self.hauteur))
        self.lvl = lvl
        self.speed = speed
        self.target_x = target[0]
        self.target_y = target[1]
        self.sens = (self.target_x-self.x)/abs(self.target_x-self.x+1)
        self.vie_act = 15*math.sqrt(lvl)
        self.vie_max = self.vie_act
        self.vie = Vie(self)
        self.degat = 5*math.sqrt(lvl)
        self.dmg_timer_init = (self.ecran_jeu.camera.largeur + self.largeur)/self.speed
        self.dmg_timer = self.dmg_timer_init

    def act_img(self):
        if self.x >= self.target_x >= self.memox or self.x < self.target_x < self.memox:
            self.memox = self.ecran_jeu.largeur - self.memox
        self.ecran_jeu.screen.blit(self.img_toilettes, (self.x, self.y))
        self.ecran_jeu.screen.blit(self.img_tete, (self.x, self.y))

        dx = (self.x - self.target_x) / (self.target_x - self.memox)
        self.x += self.speed *self.sens # * abs(self.target_x-self.memox)/300 # deux version selon celle voulue enlever #
        self.y = (self.memoy - self.target_y) * dx ** 2 + self.target_y
        self.vie.act_img()
        self.dmg_timer -= 1

    def touche(self, bullets):
        for bullet in bullets:
            if self.x <= bullet.x <= self.x + self.largeur and self.y <= bullet.y <= self.y + self.hauteur:
                self.vie_act -= bullet.damage
                bullet.pene -= 1


class Bullet_Ennemi:
    def __init__(self, ecran_jeu, x, y, degat, pene, speed):
        self.ecran_jeu = ecran_jeu
        self.img = pygame.image.load('images_de _devellopement/bullet.png').convert_alpha()
        self.x = x
        self.y = y
        self.speed = speed
        self.degat = degat
        self.vie_act = pene
        self.largeur = 1
        self.hauteur = 1
        self.dmg_timer_init = (self.ecran_jeu.camera.hauteur+self.hauteur)/self.speed
        self.dmg_timer = self.dmg_timer_init

    def act_img(self):
        self.y += self.speed
        self.ecran_jeu.screen.blit(self.img, (self.x, self.y))
        self.dmg_timer -= 1

    def touche(self, bullets):
        pass


class Skibidi_boss:
    def __init__(self, ecran_jeu, x, y, speed, lvl):
        self.ecran_jeu = ecran_jeu
        self.score = 10000
        self.x = x
        self.y = y
        self.target_x = randint(0, ecran_jeu.largeur)
        self.target_y = randint(5, 200)
        self.speed = speed
        self.largeur = 130
        self.hauteur = 130
        self.img = pygame.image.load('images_de _devellopement/boss5.png').convert_alpha()
        self.img = pygame.transform.scale(self.img, (self.largeur, self.hauteur))
        self.lvl = lvl
        self.vie_act = 500*math.sqrt(lvl)
        self.vie_max = self.vie_act
        self.vie = Vie(self)
        self.degat = 40*math.sqrt(lvl)
        self.cadence_tir = 120
        self.invocgoal = randint(300, 1250)
        self.currentinvoc = 0
        self.precedent_tir = self.cadence_tir
        self.dmg_timer_init = (math.sqrt(self.ecran_jeu.camera.largeur**2+self.ecran_jeu.camera.hauteur**2)+math.sqrt(self.hauteur**2+self.largeur**2))/self.ecran_jeu.camera.speed
        self.dmg_timer = self.dmg_timer_init

        # Charge le joueur
        self.ancien_x = self.x
        self.ancien_y = self.y
        self.current_charge = 0
        self.charge_goal = randint(400, 1250)
        self.charging = False
        self.returning = False
        self.charge_steps = 0
        self.charge_distance = 500
        self.charge_direction = (0, 0)


    def add_bullet(self):
        if self.precedent_tir <= 0:
            self.ecran_jeu.vague.add(Bullet_Ennemi(self.ecran_jeu, self.x + 60, self.y + 110, self.degat, 1, 5), 0)
            self.precedent_tir = self.cadence_tir
        self.precedent_tir -= 1

    def act_img(self):
        temp_x = self.speed * (self.target_x - self.x)
        temp_y = self.speed * (self.target_y - self.y)
        distance = math.sqrt(temp_x**2 + temp_y**2)
        if distance != 0:
            temp_x /= distance
            temp_y /= distance
        self.x += temp_x * self.speed
        self.y += temp_y * self.speed
        if abs(self.x - self.target_x) < 1 and abs(self.y - self.target_y) < 1:
            self.target_x = randint(0, self.ecran_jeu.largeur - 125)
            self.target_y = randint(5, 200)
        self.add_bullet()
        self.invocation()
        self.ecran_jeu.screen.blit(self.img, (self.x, self.y))
        self.vie.act_img()
        self.dmg_timer -= 1
        self.charge()

    def touche(self, bullets):
        for bullet in bullets:
            if self.x <= bullet.x <= self.x + self.largeur and self.y <= bullet.y <= self.y + self.hauteur:
                self.vie_act -= bullet.damage
                bullet.pene -= 1

    def invocation(self):
        self.currentinvoc += 1
        if self.currentinvoc == self.invocgoal:
            self.ecran_jeu.vague.troupe_mini_skibidi(7, choice((-100,self.ecran_jeu.largeur+100)), self.ecran_jeu.hauteur - randint(350, 500), 4, self.lvl)
            self.currentinvoc = 0
            self.invocgoal = randint(300, 1250)

    def charge(self):
        if not self.charging and not self.returning:
            self.current_charge += 1
            if self.current_charge == self.charge_goal:
                self.ancien_x = self.x
                self.ancien_y = self.y
                temp_x = self.ecran_jeu.camera.x
                temp_y = self.ecran_jeu.camera.y
                distance = math.sqrt(temp_x**2 + temp_y**2)
                if distance != 0:
                    temp_x /= distance
                    temp_y /= distance

                self.charge_direction = (temp_x, temp_y)
                self.charging = True
                self.charge_steps = 0
        elif self.charging:
            if self.charge_steps < 10:
                self.x += self.charge_direction[0] * (self.charge_distance / 10)
                self.y += self.charge_direction[1] * (self.charge_distance / 10)
                self.charge_steps += 1
            else:
                self.charging = False
                self.returning = True
                self.charge_steps = 0
        elif self.returning:
            if self.charge_steps < 10:
                self.x -= self.charge_direction[0] * (self.charge_distance / 10)
                self.y -= self.charge_direction[1] * (self.charge_distance / 10)
                self.charge_steps += 1
            else:
                self.returning = False
                self.current_charge = 0
                self.charge_goal = randint(300, 1250)


class Large_skibidi:
    def __init__(self, ecran_jeu, x, y, speed, lvl):
        self.ecran_jeu = ecran_jeu
        self.score = 1000
        self.x = x
        self.y = y
        self.target_x = randint(0, ecran_jeu.largeur)
        self.target_y = randint(5, 200)
        self.largeur = 110
        self.hauteur = 110
        self.img = pygame.image.load('images_de _devellopement/boss4.png').convert_alpha()
        self.img = pygame.transform.scale(self.img, (self.largeur, self.hauteur))
        self.lvl = lvl
        self.speed = speed
        self.vie_act = 100*math.sqrt(lvl)
        self.vie_max = self.vie_act
        self.vie = Vie(self)
        self.degat = 10*math.sqrt(lvl)
        self.cadence_tir = 25  # a ameliorer mais fonctionel (1 tir toutes les 25 images 50 images par sec)
        self.precedent_tir = self.cadence_tir
        self.dmg_timer_init = (math.sqrt(self.ecran_jeu.camera.largeur**2+self.ecran_jeu.camera.hauteur**2)+math.sqrt(self.hauteur**2+self.largeur**2))/self.ecran_jeu.camera.speed
        self.dmg_timer = self.dmg_timer_init

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
        if abs(self.x - self.target_x) < 1 and abs(self.y - self.target_y) < 1:
            self.target_x = randint(0, self.ecran_jeu.largeur - 125)
            self.target_y = randint(5, 200)
        self.add_bullet()
        self.ecran_jeu.screen.blit(self.img, (self.x, self.y))
        self.vie.act_img()
        self.dmg_timer -= 1

    def touche(self, bullets):
        for bullet in bullets:
            if self.x <= bullet.x <= self.x + self.largeur and self.y <= bullet.y <= self.y + self.hauteur:
                self.vie_act -= bullet.damage
                bullet.pene -= 1

