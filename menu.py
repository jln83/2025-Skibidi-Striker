import pygame
import sys
import subprocess

# Initialisation de Pygame
pygame.init()

# Dimensions de l'écran
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Menu de Jeu")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
HIGHLIGHT = (50, 150, 255)

# Police
font = pygame.font.Font(None, 50)

# Options du menu
options = ["Lancer le Jeu", "Settings", "Crédits"]
selected = 0

# Variable d'état
current_menu = "main"

def draw_menu():
    screen.fill(BLACK)
    for i, option in enumerate(options):
        color = HIGHLIGHT if i == selected else WHITE
        text = font.render(option, True, color)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 80))
        pygame.draw.rect(screen, GRAY, text_rect.inflate(20, 20), border_radius=10)
        screen.blit(text, text_rect)
        image = pygame.image.load('images_de _devellopement\imgmenu.jpg')
        image = pygame.transform.scale(image, (300, 200))
        screen.blit(image, (SCREEN_WIDTH//2-300//2, 20))

def draw_credits():
    screen.fill(BLACK)
    text = font.render("Maxime", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)

def main_menu():
    pygame.mixer.init()
    pygame.mixer.music.load("sons/bruitdefond2.mp3")
    volume = 0.5  # Remplacez par une valeur entre 0.0 et 1.0
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1)
    global selected, current_menu
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if current_menu == "main":
                    if event.key == pygame.K_UP:
                        selected = (selected - 1) % len(options)
                    elif event.key == pygame.K_DOWN:
                        selected = (selected + 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        if options[selected] == "Lancer le Jeu":
                            pygame.quit()
                            subprocess.run(["python", "code_gameplay.py"])
                        elif options[selected] == "Settings":
                            current_menu = "coming_soon"
                        elif options[selected] == "Crédits":
                            current_menu = "credits"
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                elif current_menu in ["credits", "coming_soon"]:
                    if event.key == pygame.K_ESCAPE:
                        current_menu = "main"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if current_menu == "main":
                    for i, option in enumerate(options):
                        text_rect = font.render(option, True, WHITE).get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 80))
                        if text_rect.collidepoint(mouse_pos):
                            if option == "Lancer le Jeu":
                                pygame.quit()
                                subprocess.run(["python", "code_gameplay.py"])
                            elif option == "Settings":
                                current_menu = "coming_soon"
                            elif option == "Crédits":
                                current_menu = "credits"

        if current_menu == "main":
            draw_menu()
        elif current_menu == "credits":
            draw_credits()
        elif current_menu == "coming_soon":
            screen.fill(BLACK)
            text = font.render("Coming Soon", True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, text_rect)

        pygame.display.flip()

# Lancer le menu principal
main_menu()
