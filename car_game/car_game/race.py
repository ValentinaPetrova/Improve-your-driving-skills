import pygame
import random
import sys
import os
import time
from pygame.locals import *

# Размери
WINDOWWIDTH = 800
WINDOWHEIGHT = 600
TEXTCOLOR = (255, 255, 255)
BACKGROUNDCOLOR = (0, 0, 0)
FPS = 40
BADDIEMINSIZE = 10
BADDIEMAXSIZE = 40
BADDIEMINSPEED = 8
BADDIEMAXSPEED = 8
ADDNEWBADDIERATE = 6
PLAYERMOVERATE = 5
count = 3
score = 0


def terminate():
    from all_game import main_menu
    main_menu()
    sys.exit()


def wait_for_player_to_press_key():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # escape quits
                    terminate()
                return


def player_has_hit_baddie(player_rect, baddies):
    for b in baddies:
        if player_rect.colliderect(b['rect']):
            return True
    return False


def draw_text(text, font, surface, x, y):
    text_obj = font.render(text, 1, TEXTCOLOR)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)


# инициализация
# pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('car race')
pygame.mouse.set_visible(True)

font = pygame.font.SysFont(None, 30)


# изображения
playerImage = pygame.image.load('image_car1.png')
car3 = pygame.image.load('image_car3.png')
car4 = pygame.image.load('image_car4.png')
playerRect = playerImage.get_rect()
baddieImage = pygame.image.load('image_car2.png')
sample = [car3, car4, baddieImage]
wallLeft = pygame.image.load('image_left.png')
wallRight = pygame.image.load('image.right.png')
wallLeft_second = pygame.image.load('image_left_second.png')
wallRight_second = pygame.image.load('image_right_second.png')


# Същинска част
def run_racing():
    global count

    draw_text('Press any key to start the game.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3))
    draw_text('And Enjoy', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3) + 30)
    pygame.display.update()
    wait_for_player_to_press_key()

    if not os.path.exists("data_save.dat"):
        with open("data_save.dat", 'w') as f:
            f.write("0")

    with open("data_save.dat", 'r') as v:
        top_score = int(v.readline())

    while count > 0:
        # стартиране
        baddies = []
        score = 0
        playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
        move_left = move_right = move_up = move_down = False
        reverse_cheat = slow_cheat = False
        baddie_add_counter = 0

        while True:  # игрален цикъл
            score += 1

            for event in pygame.event.get():
                if event.type == QUIT:
                    from all_game import main_menu
                    main_menu()
                    return
                if event.type == KEYDOWN:
                    if event.key == ord('z'):
                        reverse_cheat = True
                    if event.key == ord('x'):
                        slow_cheat = True
                    if event.key == K_LEFT or event.key == ord('a'):
                        move_right = False
                        move_left = True
                    if event.key == K_RIGHT or event.key == ord('d'):
                        move_left = False
                        move_right = True
                    if event.key == K_UP or event.key == ord('w'):
                        move_down = False
                        move_up = True
                    if event.key == K_DOWN or event.key == ord('s'):
                        move_up = False
                        move_down = True

                if event.type == KEYUP:
                    if event.key == ord('z'):
                        reverse_cheat = False
                        score = 0
                    if event.key == ord('x'):
                        slow_cheat = False
                        score = 0
                    if event.key == K_ESCAPE:
                        from all_game import main_menu
                        main_menu()
                        return

                    if event.key == K_LEFT or event.key == ord('a'):
                        move_left = False
                    if event.key == K_RIGHT or event.key == ord('d'):
                        move_right = False
                    if event.key == K_UP or event.key == ord('w'):
                        move_up = False
                    if event.key == K_DOWN or event.key == ord('s'):
                        move_down = False

        # Add new baddies at the top of the screen
            if not reverse_cheat and not slow_cheat:
                baddie_add_counter += 1
            if baddie_add_counter == ADDNEWBADDIERATE:
                baddie_add_counter = 0
                baddie_size = 30
                new_baddie = {'rect': pygame.Rect(random.randint(140, 485), 0 - baddie_size, 23, 47),
                              'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                              'surface': pygame.transform.scale(random.choice(sample), (23, 47)),
                              }
                baddies.append(new_baddie)
                if score < 1000:
                    side_left = {'rect': pygame.Rect(0, 0, 126, 600),
                                 'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                                 'surface': pygame.transform.scale(wallLeft, (126, 599)),
                                 }
                    baddies.append(side_left)
                    side_right = {'rect': pygame.Rect(497, 0, 303, 600),
                                  'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                                  'surface': pygame.transform.scale(wallRight, (303, 599)),
                                  }
                    baddies.append(side_right)
                else:
                    side_left = {'rect': pygame.Rect(0, 0, 126, 600),
                                 'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                                 'surface': pygame.transform.scale(wallLeft_second, (126, 599)),
                                 }
                    baddies.append(side_left)
                    side_right = {'rect': pygame.Rect(497, 0, 303, 600),
                                  'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                                  'surface': pygame.transform.scale(wallRight_second, (303, 599)),
                                  }
                    baddies.append(side_right)

            # Движения
            if move_left and playerRect.left > 0:
                playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
            if move_right and playerRect.right < WINDOWWIDTH:
                playerRect.move_ip(PLAYERMOVERATE, 0)
            if move_up and playerRect.top > 0:
                playerRect.move_ip(0, -1 * PLAYERMOVERATE)
            if move_down and playerRect.bottom < WINDOWHEIGHT:
                playerRect.move_ip(0, PLAYERMOVERATE)

            for b in baddies:
                if not reverse_cheat and not slow_cheat:
                    b['rect'].move_ip(0, b['speed'])
                elif reverse_cheat:
                    b['rect'].move_ip(0, -5)
                elif slow_cheat:
                    b['rect'].move_ip(0, 1)

            for b in baddies[:]:
                if b['rect'].top > WINDOWHEIGHT:
                    baddies.remove(b)

        # Draw the game world on the window.
            windowSurface.fill(BACKGROUNDCOLOR)

        # Draw the score and top score.
            draw_text(f'Score: {score}', font, windowSurface, 128, 0)
            draw_text(f'Top Score: {top_score}', font, windowSurface, 128, 20)
            draw_text(f'Rest Life: {count}', font, windowSurface, 128, 40)

            windowSurface.blit(playerImage, playerRect)

            for b in baddies:
                windowSurface.blit(b['surface'], b['rect'])

            pygame.display.update()

        # Check if any of the car have hit the player.
            if player_has_hit_baddie(playerRect, baddies):
                if score > top_score:
                    with open("data_save.dat", 'w') as g:
                        g.write(str(score))
                    top_score = score
                break

            mainClock.tick(FPS)

    # "Game Over" screen.
        count -= 1
        time.sleep(1)
        if count == 0:
            draw_text('Game over', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
            draw_text('Press any key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 30)
            pygame.display.update()
            time.sleep(2)
            wait_for_player_to_press_key()
            count = 3
