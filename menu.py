import pygame
import sys
import subprocess

class Menu:
    def __init__(self):
        pygame.mixer.init()
        self.menue = pygame.mixer.Sound('sons/menu.mp3')  # Remplacez par votre fichier audio

        # Initialisation de Pygame
        pygame.init()
        # Dimensions de l'écran
        self.largeur, self.hauteur = 1280, 720
        self.screen = pygame.display.set_mode((self.largeur, self.hauteur))
        pygame.display.set_caption("Menu de Jeu")

        # Couleurs
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (100, 100, 100)
        self.HIGHLIGHT = (50, 150, 255)

        # Police
        self.font = pygame.font.Font(None, 50)
        # Options du menu
        self.options = ["Lancer le Jeu", "Settings", "Crédits"]
        self.selected = 0
        # Variable d'état
        self.current_menu = "main"

    def draw_menu(self):
        self.screen.fill(self.BLACK)
        for i, option in enumerate(self.options):
            color = self.HIGHLIGHT if i == self.selected else self.WHITE
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=(self.largeur // 2, self.hauteur // 2 + i * 80))
            pygame.draw.rect(self.screen, self.GRAY, text_rect.inflate(20, 20), border_radius=10)
            self.screen.blit(text, text_rect)
            image = pygame.image.load('images_de _devellopement/imgmenu.jpg')
            image = pygame.transform.scale(image, (300, 200))
            self.screen.blit(image, (self.largeur//2-300//2, 20))

    def draw_credits(self):
        self.screen.fill(self.BLACK)
        text = self.font.render("Maxime, Julain, Clément, Tristant", True, self.WHITE)
        text_rect = text.get_rect(center=(self.largeur // 2, self.hauteur // 2))
        self.screen.blit(text, text_rect)

    def main_menu(self):

        pygame.mixer.music.load("sons/bruitdefond2.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    sys.exit()


                if event.type == pygame.KEYDOWN:
                    self.menue.play()
                    if self.current_menu == "main":
                        if event.key == pygame.K_UP:
                            self.selected = (self.selected - 1) % len(self.options)
                        elif event.key == pygame.K_DOWN:
                            self.selected = (self.selected + 1) % len(self.options)
                        elif event.key == pygame.K_RETURN:
                            if self.options[self.selected] == "Lancer le Jeu":
                                running=False
                                subprocess.Popen(["python", "code_gameplay.py"])
                            elif self.options[self.selected] == "Settings":
                                self.current_menu = "coming_soon"
                            elif self.options[self.selected] == "Crédits":
                                self.current_menu = "credits"
                        elif event.key == pygame.K_ESCAPE:
                            running = False
                            sys.exit()
                    elif self.current_menu in ["credits", "coming_soon"]:
                        if event.key == pygame.K_ESCAPE:
                            self.current_menu = "main"

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    self.menue.play()
                    if self.current_menu == "main":
                        for i, option in enumerate(self.options):
                            text_rect = self.font.render(option, True, self.WHITE).get_rect(center=(self.largeur // 2, self.hauteur // 2 + i * 80))
                            if text_rect.collidepoint(mouse_pos):
                                if option == "Lancer le Jeu":
                                    running=False
                                    subprocess.Popen(["python", "code_gameplay.py"])
                                elif option == "Settings":
                                    self.current_menu = "coming_soon"
                                elif option == "Crédits":
                                    self.current_menu = "credits"

            if self.current_menu == "main":
                self.draw_menu()
            elif self.current_menu == "credits":
                self.draw_credits()
            elif self.current_menu == "coming_soon":
                self.screen.fill(self.BLACK)
                text = self.font.render("Coming Soon", True, self.WHITE)
                text_rect = text.get_rect(center=(self.largeur // 2, self.hauteur // 2))
                self.screen.blit(text, text_rect)

            pygame.display.flip()
        pygame.quit()


    # Lancer le menu principal
Menu().main_menu()
