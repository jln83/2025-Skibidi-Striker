import pygame
import sys

class Menu:
    def __init__(self):
        pygame.mixer.init()
        self.menue = pygame.mixer.Sound('sons/menu.mp3')  # Remplacez par votre fichier audio

        # Initialisation de Pygame
        pygame.init()
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
        """Affiche le menu principal."""
        self.screen.fill(self.BLACK)
        for i, option in enumerate(self.options):
            color = self.HIGHLIGHT if i == self.selected else self.WHITE
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=(self.largeur // 2, self.hauteur // 2 + i * 80))
            pygame.draw.rect(self.screen, self.GRAY, text_rect.inflate(20, 20), border_radius=10)
            self.screen.blit(text, text_rect)

        # Image de fond
        image = pygame.image.load('images_de _devellopement/imgmenu.jpg')
        image = pygame.transform.scale(image, (300, 200))
        self.screen.blit(image, (self.largeur // 2 - 300 // 2, 20))

    def draw_settings(self):
        """Affiche le menu des paramètres avec un bouton de retour."""
        self.screen.fill(self.BLACK)

        # Titre
        title = self.font.render("Paramètres", True, self.WHITE)
        title_rect = title.get_rect(center=(self.largeur // 2, 100))
        self.screen.blit(title, title_rect)

        # Contrôles
        controls = [
            "Flèche Haut : Monter",
            "Flèche Bas : Descendre",
            "Flèche Gauche : Aller à gauche",
            "Flèche Droite : Aller à droite",
            "Echap : Retour au menu principal"
        ]
        for i, line in enumerate(controls):
            text = self.font.render(line, True, self.WHITE)
            text_rect = text.get_rect(center=(self.largeur // 2, 200 + i * 50))
            self.screen.blit(text, text_rect)

        # Bouton Retour
        button_text = self.font.render("Retour", True, self.WHITE)
        self.button_rect_settings = button_text.get_rect(center=(self.largeur // 2, self.hauteur - 100))
        pygame.draw.rect(self.screen, self.GRAY, self.button_rect_settings.inflate(20, 20), border_radius=10)
        self.screen.blit(button_text, self.button_rect_settings)

    def draw_credits(self):
        """Affiche le menu des crédits avec un bouton de retour."""
        self.screen.fill(self.BLACK)

        # Crédits
        text = self.font.render("Maxime, Julain, Clément, Tristan", True, self.WHITE)
        text_rect = text.get_rect(center=(self.largeur // 2, self.hauteur // 2))
        self.screen.blit(text, text_rect)

        # Bouton Retour
        button_text = self.font.render("Retour", True, self.WHITE)
        self.button_rect_credits = button_text.get_rect(center=(self.largeur // 2, self.hauteur - 100))
        pygame.draw.rect(self.screen, self.GRAY, self.button_rect_credits.inflate(20, 20), border_radius=10)
        self.screen.blit(button_text, self.button_rect_credits)

    def main_menu(self):
        """Boucle principale du menu."""
        pygame.mixer.music.load("sons/bruitdefond2.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        running = True
        run = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    self.menue.play()
                    if event.key == pygame.K_ESCAPE:
                        if self.current_menu != "main":
                            self.current_menu = "main"
                        else:
                            running = False
                            sys.exit()

                    if self.current_menu == "main":
                        if event.key == pygame.K_UP:
                            self.selected = (self.selected - 1) % len(self.options)
                        elif event.key == pygame.K_DOWN:
                            self.selected = (self.selected + 1) % len(self.options)
                        elif event.key == pygame.K_RETURN:
                            if self.options[self.selected] == "Lancer le Jeu":
                                running = False
                                run = True
                            elif self.options[self.selected] == "Settings":
                                self.current_menu = "settings"
                            elif self.options[self.selected] == "Crédits":
                                self.current_menu = "credits"

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    self.menue.play()
                    if self.current_menu == "settings" and self.button_rect_settings.collidepoint(mouse_pos):
                        self.current_menu = "main"
                    elif self.current_menu == "credits" and self.button_rect_credits.collidepoint(mouse_pos):
                        self.current_menu = "main"
                    elif self.current_menu == "main":
                        for i, option in enumerate(self.options):
                            text_rect = self.font.render(option, True, self.WHITE).get_rect(
                                center=(self.largeur // 2, self.hauteur // 2 + i * 80))
                            if text_rect.collidepoint(mouse_pos):
                                if option == "Lancer le Jeu":
                                    running = False
                                    run = True
                                elif option == "Settings":
                                    self.current_menu = "settings"
                                elif option == "Crédits":
                                    self.current_menu = "credits"

            if self.current_menu == "main":
                self.draw_menu()
            elif self.current_menu == "settings":
                self.draw_settings()
            elif self.current_menu == "credits":
                self.draw_credits()

            pygame.display.flip()
        pygame.quit()
        return run

