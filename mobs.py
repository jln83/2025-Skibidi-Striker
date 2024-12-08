import pygame

class Skibidi:
    def __init__(self, x):
        self.x = x
        self.y = -50
        self.img = pygame.image.load('images_de _devellopement/skibidi.png').convert_alpha()
        self.speedx = 2
        self.speedy = 2
        self.xmin = max(x - 50, 0)
        self.xmax = min(x + 50, ecran_jeu.largeur - 50)

    def act_img(self):
        ecran_jeu.screen.blit(self.img, (self.x, self.y))

        self.x += self.speedx
        self.y += self.speedy
        if self.x < self.xmin or self.x > self.xmax:
            self.speedx *= -1