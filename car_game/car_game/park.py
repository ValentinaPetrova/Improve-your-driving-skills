import pygame
import random

# pygame.init()

DEFAULT_IMAGE_SIZE = (100, 80)

# Екран
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Park the car")
background = pygame.image.load("background1.jpg").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Зареждане на коли
car_images = ["car_for_parking.png", "car_for_parking2.png", "car_for_parking3.png"]
current_car_index = 0
car = pygame.image.load(car_images[current_car_index]).convert_alpha()
car = pygame.transform.scale(car, (car.get_width()//5, car.get_height()//5))
car_rect = car.get_rect(center=(WIDTH // 2, HEIGHT - 100))

# Нива и паркинг места
levels = [pygame.Rect(100, 100, 100, 160), pygame.Rect(450, 400, 100, 160), pygame.Rect(750, 100, 100, 160),
          pygame.Rect(300, 400, 100, 160), pygame.Rect(600, 150, 100, 160), pygame.Rect(750, 400, 100, 160),
          pygame.Rect(100, 400, 100, 160), pygame.Rect(750, 150, 100, 160), pygame.Rect(450, 400, 100, 160),
          pygame.Rect(250, 400, 100, 160)]
current_level = 0
unlocked_levels = 1
parking_spot = levels[current_level]

# Други коли (препятствия)
obstacle_images = [pygame.image.load("parked_car1.png").convert_alpha(), pygame.image.load(
    "parked_car2.png").convert_alpha(), pygame.image.load("parked_car3.png").convert_alpha()]
obstacles = [
    {"rect": pygame.Rect(400, 200, 80, 40), "image": pygame.transform.scale(obstacle_images[0], (120, 80))},
    {"rect": pygame.Rect(600, 400, 80, 40), "image": pygame.transform.scale(obstacle_images[1], (140, 80))},
    {"rect": pygame.Rect(800, 400, 80, 40), "image": pygame.transform.scale(obstacle_images[2], (120, 160))}
]

level_obstacles = {
    0: [pygame.Rect(400, 200, 80, 40), pygame.Rect(600, 400, 80, 40)],
    1: [pygame.Rect(300, 150, 80, 40), pygame.Rect(700, 300, 80, 40)],
    2: [pygame.Rect(500, 250, 80, 40), pygame.Rect(600, 450, 80, 40)],
    3: [pygame.Rect(200, 200, 80, 40), pygame.Rect(600, 550, 80, 40), pygame.Rect(600, 400, 80, 40), pygame.Rect(400, 100, 80, 40), pygame.Rect(300, 550, 80, 40)],
    4: [pygame.Rect(400, 100, 80, 40), pygame.Rect(750, 300, 80, 40), pygame.Rect(600, 300, 80, 40), pygame.Rect(750, 550, 80, 40), pygame.Rect(150, 200, 80, 40)],
    5: [pygame.Rect(400, 100, 80, 40), pygame.Rect(600, 400, 80, 40), pygame.Rect(600, 200, 80, 40), pygame.Rect(300, 200, 80, 40), pygame.Rect(750, 550, 80, 40)],
    6: [pygame.Rect(400, 100, 80, 40), pygame.Rect(250, 400, 80, 40), pygame.Rect(600, 400, 80, 40), pygame.Rect(100, 550, 80, 40), pygame.Rect(750, 550, 80, 40)],
    7: [pygame.Rect(400, 100, 80, 40), pygame.Rect(750, 400, 80, 40), pygame.Rect(600, 400, 80, 40), pygame.Rect(300, 200, 80, 40), pygame.Rect(500, 400, 80, 40)],
    8: [pygame.Rect(400, 100, 80, 40), pygame.Rect(750, 400, 80, 40), pygame.Rect(600, 400, 80, 40), pygame.Rect(800, 300, 80, 40), pygame.Rect(450, 200, 80, 40), pygame.Rect(300, 200, 80, 40)],
    9: [pygame.Rect(400, 100, 80, 40), pygame.Rect(750, 400, 80, 40), pygame.Rect(600, 400, 80, 40), pygame.Rect(800, 300, 80, 40), pygame.Rect(500, 550, 80, 40), pygame.Rect(300, 200, 80, 40)],
}

# obstacles = [pygame.Rect(400, 200, 80, 40), pygame.Rect(600, 400, 80, 40)]

# Животи
lives = 3
score = 0

# Бонус точки (жълти и оранжеви квадрати)
yellow_bonus_levels = {2, 4, 6, 8}
orange_bonus_levels = {7, 9}
yellow_bonus = [pygame.Rect(150, 250, 40, 40), pygame.Rect(700, 150, 40, 40), pygame.Rect(150, 500, 40, 40)]
orange_bonus = [pygame.Rect(600, 300, 50, 50)]

yellow_bonus_image = pygame.image.load("snikers.png").convert_alpha()
yellow_bonus_image = pygame.transform.scale(yellow_bonus_image, (60, 25))

orange_bonus_image = pygame.image.load("krenvirsh.png").convert_alpha()
orange_bonus_image = pygame.transform.scale(orange_bonus_image, (50, 50))

font = pygame.font.Font(None, 36)


def draw_stats():
    lives_text = font.render(f"Животи: {lives}", True, (0, 0, 0))
    score_text = font.render(f"Точки: {score}", True, (0, 0, 0))
    screen.blit(lives_text, (20, 20))
    screen.blit(score_text, (20, 50))


def show_message(text):
    message = font.render(text, True, (0, 0, 0))
    screen.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT // 2 - message.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(2000)


# Основно меню за избор на ниво
def show_level_selection():
    global current_level, parking_spot
    selected = 0
    while True:
        screen.fill((200, 200, 200))
        title = font.render("Избери ниво", True, (0, 0, 0))
        screen.blit(title, (WIDTH // 2 - 50, 50))
        draw_stats()

        level_buttons = []
        for i in range(unlocked_levels):
            color = (0, 255, 0) if i == selected else (255, 255, 255)
            button_rect = pygame.Rect((WIDTH // 2 - 50, 100 + i * 50, 120, 40))
            pygame.draw.rect(screen, color, button_rect)
            level_text = font.render(f"Ниво {i + 1}", True, (0, 0, 0))
            screen.blit(level_text, (WIDTH // 2 - 40, 110 + i * 50))
            level_buttons.append((button_rect, i))

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #pygame.quit()
                #sys.exit()
                from all_game import main_menu
                main_menu()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and selected > 0:
                    selected -= 1
                elif event.key == pygame.K_DOWN and selected < unlocked_levels - 1:
                    selected += 1
                elif event.key == pygame.K_RETURN:
                    current_level = selected
                    parking_spot = levels[current_level]
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for button, level in level_buttons:
                    if button.collidepoint(mouse_pos):
                        current_level = level
                        parking_spot = levels[current_level]
                        return


def check_overlap(rect, others):
    return any(rect.colliderect(other) for other in others)


def load_level(level, testing=False):
    if testing:
        return
    global parking_spot, obstacles, yellow_bonus, orange_bonus

    parking_spot = levels[level]

    all_parking_spots = levels[:unlocked_levels]

    obstacles = []
    for rect in level_obstacles.get(level, []):
        if not check_overlap(rect, all_parking_spots):
            obstacles.append({"rect": rect, "image": pygame.transform.scale(random.choice(obstacle_images), (160, 100))})

    yellow_bonus = [b for b in [pygame.Rect(250, 250, 40, 40), pygame.Rect(700, 150, 40, 40), pygame.Rect(450, 500, 40, 40)]
                    if not check_overlap(b, all_parking_spots + [o["rect"] for o in obstacles])]

    orange_bonus = [b for b in [pygame.Rect(600, 300, 50, 50)]
                    if not check_overlap(b, all_parking_spots + [o["rect"] for o in obstacles] + yellow_bonus)]


previous_parking_spots = []
current_car_index = 0


def run_parking(main_menu_callback, testing=False):
    if testing:
        return

    global car, car_rect, lives, score, current_level, unlocked_levels, parking_spot, yellow_bonus, orange_bonus

    # Екран
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Park the car")
    background = pygame.image.load("background1.jpg").convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    # Игрален цикъл
    alive = True
    clock = pygame.time.Clock()
    angle = 0
    speed = 5

    show_level_selection()
    load_level(current_level)

    while alive:
        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, (0, 255, 0), parking_spot)
        draw_stats()

        for obstacle in obstacles:
            screen.blit(obstacle["image"], obstacle["rect"].topleft)

        if current_level in yellow_bonus_levels:
            for bonus in yellow_bonus:
                screen.blit(yellow_bonus_image, bonus.topleft)
        if current_level in orange_bonus_levels:
            for bonus in orange_bonus:
                screen.blit(orange_bonus_image, bonus.topleft)

        # Въртим и рисуваме колата
        rotated_car = pygame.transform.rotate(car, angle)
        car_rect = rotated_car.get_rect(center=car_rect.center)
        screen.blit(rotated_car, car_rect.topleft)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                alive = False
                main_menu_callback()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    global current_car_index
                    current_car_index = (current_car_index + 1) % len(car_images)
                    car = pygame.image.load(car_images[current_car_index]).convert_alpha()
                    car = pygame.transform.scale(car, (car.get_width() // 5, car.get_height() // 5))

    # Движение
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            car_rect.x -= speed
            angle = 90
        if keys[pygame.K_RIGHT]:
            car_rect.x += speed
            angle = -90
        if keys[pygame.K_UP]:
            car_rect.y -= speed
            angle = 0
        if keys[pygame.K_DOWN]:
            car_rect.y += speed
            angle = 180

    # Проверка за сблъсък с препятствия
        for obstacle in obstacles:
            if car_rect.colliderect(obstacle["rect"]):
                lives -= 1
                car_rect.center = (WIDTH // 2, HEIGHT - 100)
                if lives == 0:
                    show_message("Опитай отново!")
                    lives = 3
                    show_level_selection()

    # Проверка за събиране на бонуси
        if current_level in yellow_bonus_levels:
            for b in yellow_bonus:
                if car_rect.colliderect(b):
                    score += 5
                    yellow_bonus.remove(b)
        elif current_level in orange_bonus_levels:
            for b in orange_bonus:
                if car_rect.colliderect(b):
                    score += 10
                    orange_bonus.remove(b)

    # Проверка за паркиране
        if parking_spot.contains(car_rect):
            show_message(f"Поздравления! Ти успешно премина ниво {current_level + 1}!")
            if current_level < unlocked_levels:
                unlocked_levels = min(unlocked_levels + 1, len(levels))
            current_level += 1
            if current_level < len(levels):
                parking_spot = levels[current_level]
                load_level(current_level)
            else:
                show_level_selection()
            yellow_bonus = [pygame.Rect(250, 250, 40, 40), pygame.Rect(700, 150, 40, 40), pygame.Rect(100, 500, 40, 40)]
            orange_bonus = [pygame.Rect(400, 300, 50, 50)]

        pygame.display.flip()
        clock.tick(60)
    main_menu_callback()
    # pygame.quit()
    # levels_menu()
