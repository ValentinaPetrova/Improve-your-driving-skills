import pygame
import sys

pygame.init()

# Екран
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Паркирай колата")

# Зареждане на коли
car_images = ["car_for_parking.png", "car_for_parking2.png", "car_for_parking3.png"]  # Списък с различни коли
current_car_index = 0
car = pygame.image.load(car_images[current_car_index]).convert_alpha()
car = pygame.transform.scale(car, (car.get_width() // 5, car.get_height() // 5))
car_rect = car.get_rect(center=(WIDTH // 2, HEIGHT - 100))

# Нива и паркинг места
levels = [pygame.Rect(200, 100, 160, 100), pygame.Rect(500, 300, 160, 100), pygame.Rect(700, 500, 160, 100),
          pygame.Rect(300, 400, 160, 100), pygame.Rect(600, 150, 160, 100), pygame.Rect(800, 600, 160, 100),
          pygame.Rect(150, 500, 160, 100), pygame.Rect(750, 250, 160, 100), pygame.Rect(450, 550, 160, 100),
          pygame.Rect(350, 250, 160, 100)]
current_level = 0
unlocked_levels = 1
parking_spot = levels[current_level]

# Други коли (препятствия)
obstacles = [pygame.Rect(400, 200, 80, 40), pygame.Rect(600, 400, 80, 40)]

# Животи
lives = 3
score = 0

# Бонус точки (жълти и оранжеви квадрати)
yellow_bonus_levels = {2, 4, 6, 8}
orange_bonus_levels = {7, 9}
yellow_bonus = [pygame.Rect(250, 250, 40, 40), pygame.Rect(700, 150, 40, 40), pygame.Rect(500, 500, 40, 40)]
orange_bonus = [pygame.Rect(400, 300, 50, 50)]

# Функция за показване на статистики
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

        for i in range(unlocked_levels):
            color = (0, 255, 0) if i == selected else (255, 255, 255)
            pygame.draw.rect(screen, color, (WIDTH // 2 - 50, 100 + i * 50, 120, 40))
            level_text = font.render(f"Ниво {i + 1}", True, (0, 0, 0))
            screen.blit(level_text, (WIDTH // 2 - 40, 110 + i * 50))

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and selected > 0:
                    selected -= 1
                elif event.key == pygame.K_DOWN and selected < unlocked_levels - 1:
                    selected += 1
                elif event.key == pygame.K_RETURN:
                    current_level = selected
                    parking_spot = levels[current_level]
                    return


show_level_selection()

# Игрален цикъл
alive = True
clock = pygame.time.Clock()
angle = 0
speed = 5

while alive:
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (0, 255, 0), parking_spot)  # Зона за паркиране
    draw_stats()

    for obstacle in obstacles:
        pygame.draw.rect(screen, (255, 0, 0), obstacle)  # Препятствия

    if current_level in yellow_bonus_levels:
        for bonus in yellow_bonus:
            pygame.draw.rect(screen, (255, 255, 0), bonus)  # Жълти бонуси
    elif current_level in orange_bonus_levels:
        for bonus in orange_bonus:
            pygame.draw.rect(screen, (255, 165, 0), bonus)  # Оранжев бонус

    # Въртим и рисуваме колата
    rotated_car = pygame.transform.rotate(car, angle)
    car_rect = rotated_car.get_rect(center=car_rect.center)
    screen.blit(rotated_car, car_rect.topleft)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            alive = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Смяна на кола
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
        if car_rect.colliderect(obstacle):
            lives -= 1
            car_rect.center = (WIDTH // 2, HEIGHT - 100)
            if lives == 0:
                show_message("Опитай отново!")
                lives = 3
                show_level_selection()

    # Проверка за събиране на бонуси
    if current_level in yellow_bonus_levels:
        #yellow_bonus = [b for b in yellow_bonus if not car_rect.colliderect(b)]
        for b in yellow_bonus:
            if car_rect.colliderect(b):
                score += 5
                yellow_bonus.remove(b)
    elif current_level in orange_bonus_levels:
        #orange_bonus = [b for b in orange_bonus if not car_rect.colliderect(b)]
        for b in orange_bonus:
            if car_rect.colliderect(b):
                score += 10
                orange_bonus.remove(b)

    # Проверка за паркиране (пълно съдържание в зоната)
    if parking_spot.contains(car_rect):
        show_message(f"Поздравления! Ти успешно премина {current_level + 1}-во ниво!")
        if current_level < unlocked_levels:
            unlocked_levels = min(unlocked_levels + 1, len(levels))
        current_level += 1
        if current_level < len(levels):
            parking_spot = levels[current_level]
        else:
            show_level_selection()
        yellow_bonus = [pygame.Rect(250, 250, 40, 40), pygame.Rect(700, 150, 40, 40), pygame.Rect(500, 500, 40, 40)]
        orange_bonus = [pygame.Rect(400, 300, 50, 50)]

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
