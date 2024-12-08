import pygame


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Camera:  # joueur
    def __init__(self):
        self.img = pygame.image.load('images_de _devellopement/camera.png').convert_alpha()
        self.bullet_img = pygame.image.load('images_de _devellopement/bullet.png').convert_alpha()
        self.bullets = []  # liste des balles en train d'etre tirées
        self.x = 275
        self.y = 500
        self.cadence_tir = 10  # a ameliorer mais fonctionel (1 tir toutes les dix images)
        self.precedent_tir = self.cadence_tir
        self.life = 100  # inutile pour le moment
        self.speed = 10

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

    def boucle_run(self):
        right = False
        left = False
        up = False
        down = False
        bullet = False
        camera = Camera()
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

            if bullet:
                camera.add_bullet()
            if right and camera.x < self.largeur - 50:
                camera.x += camera.speed
            if left and camera.x > 0:
                camera.x -= camera.speed
            if up and camera.y > self.hauteur - 200:
                camera.y -= camera.speed
            if down and camera.y < self.hauteur - 50:
                camera.y += camera.speed

            for Back in self.fond:
                Back.act_img()
            camera.act_img()
            pygame.display.update()
            self.clock.tick(50)


ecran_jeu = ecran_jeu(600, 600)
ecran_jeu.boucle_run()

# bar espace pour tirer
# fleches pour se deplacer
