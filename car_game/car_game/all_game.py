import pygame
import sys


pygame.init()

# Екран
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Menu")

# Цветове
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
HOVER_COLOR = (173, 216, 230)

font = pygame.font.Font(None, 50)

# Опции в менюто
menu_items = [
    ("Park the car", "park", 200),
    ("Car Race", "race", 300),
    ("Maze", "maze", 400)
]


def draw_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


def main_menu():
    while True:
        screen.fill(BLACK)
        draw_text("Game Menu", WHITE, 300, 100)

        mouse_x, mouse_y = pygame.mouse.get_pos()

        for i, (text, module, y) in enumerate(menu_items):
            # Highlight text if hovered
            color = HOVER_COLOR if 280 <= mouse_x <= 520 and y <= mouse_y <= y + 50 else BLUE
            draw_text(f"{i+1}. {text}", color, 300, y)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    from park import run_parking
                    run_parking(main_menu)
                elif event.key == pygame.K_2:
                    from race import run_racing
                    run_racing()
                elif event.key == pygame.K_3:
                    from maze import get_the_snickers
                    get_the_snickers()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, (text, module, y) in enumerate(menu_items):
                    if 280 <= mouse_x <= 520 and y <= mouse_y <= y + 50:
                        if module == "park":
                            from park import run_parking
                            run_parking(main_menu)
                        elif module == "race":
                            from race import run_racing
                            run_racing()
                        elif module == "maze":
                            from maze import get_the_snickers
                            get_the_snickers()


main_menu()
