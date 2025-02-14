import pygame
import sys


pygame.init()

# Цветове
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.Font(None, 36)


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def main_menu():
    while True:
        screen.fill(BLACK)
        draw_text("Game Menu", font, WHITE, screen, 300, 100)
        draw_text("1. Park the Car", font, BLUE, screen, 300, 200)
        draw_text("2. Car Race", font, BLUE, screen, 300, 300)
        draw_text("3. Coming Soon", font, BLUE, screen, 300, 400)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    # print("Start Park the Car")
                    from game import run_parking
                    run_parking()
                if event.key == pygame.K_2:
                    from car_game import run_racing
                    run_racing()
                if event.key == pygame.K_3:
                    print("Coming Soon")

