import pygame
import random
import time
import sys

pygame.init()

title_font = pygame.font.SysFont(None, 100)
font = pygame.font.SysFont(None, 50)
error_font = pygame.font.SysFont(None, 35)

size = 30
speed = 30
limit = 600

controls = {
    "UP": pygame.K_UP,
    "DOWN": pygame.K_DOWN,
    "LEFT": pygame.K_LEFT,
    "RIGHT": pygame.K_RIGHT,
    "PAUSE": pygame.K_p
}

clock = pygame.time.Clock()

square_surf = pygame.Surface((size - 2, size - 2))
square_surf.fill((0, 255, 0))

head_surf = pygame.Surface((size - 2, size - 2))
head_surf.fill((255, 255, 255))

def reset_game():
    global x, y, snake_body, snake_length, direction, ticks, Paused, limit, screen, initial_limit, apple_rect

    initial_limit = limit
    screen = pygame.display.set_mode((initial_limit, initial_limit))

    Paused = False
    waiting_for_key = None
    Error_1 = Error_2 = Error_3 = Error_4 = False
    menu_state = "Main"

    direction = "right"
    x = 0
    y = 300
    ticks = 0
    snake_body = []
    snake_length = 3

    apple_x = random.randrange(30, limit - size, size)
    apple_y = random.randrange(30, limit - size, size)
    apple_rect = pygame.Rect(apple_x, apple_y, size, size)



    while True:
        screen.fill((0, 0, 0))
        Back = font.render("Go Back", True, (255, 255, 255))
        Back_rect = Back.get_rect(center=(initial_limit // 2, initial_limit // 2 + 250))

        if menu_state == "Main":
            title = title_font.render("Snake+", True, (0, 255, 0))
            diff = font.render("Difficulty", True, (255, 255, 255))
            diff_rect = diff.get_rect(center=(initial_limit // 2, initial_limit // 2))
            settings = font.render("Settings", True, (255, 255, 255))
            settings_rect = settings.get_rect(center=(initial_limit // 2, initial_limit // 2 + 50))
            Start = font.render("Start", True, (255, 255, 255))
            Start_rect = Start.get_rect(center=(initial_limit // 2, initial_limit // 2 - 50))

            screen.blit(title, (initial_limit // 2 - 110, initial_limit // 2 - 200))
            screen.blit(Start, Start_rect)
            screen.blit(diff, diff_rect)
            screen.blit(settings, settings_rect)

            if Error_3:
                screen.blit(Error3, Error3_rect)

        elif menu_state == "Difficulty":
            E = font.render("Easy", True, (255, 255, 255))
            M = font.render("Medium", True, (255, 255, 255))
            H = font.render("Hard", True, (255, 255, 255))
            E_rect = E.get_rect(center=(initial_limit // 2, initial_limit // 2 - 50))
            M_rect = M.get_rect(center=(initial_limit // 2, initial_limit // 2))
            H_rect = H.get_rect(center=(initial_limit // 2, initial_limit // 2 + 50))

            screen.blit(E, E_rect)
            screen.blit(M, M_rect)
            screen.blit(H, H_rect)
            screen.blit(Back, Back_rect)

        elif menu_state == "Settings":
            control = font.render("Controls", True, (255, 255, 255))
            control_rect = control.get_rect(center=(initial_limit // 2, initial_limit // 2))
            resolution = font.render("Graphics", True, (255, 255, 255))
            resolution_rect = resolution.get_rect(center=(initial_limit // 2, initial_limit // 2 - 50))

            screen.blit(resolution, resolution_rect)
            screen.blit(control, control_rect)
            screen.blit(Back, Back_rect)

        elif menu_state == "Controls":
            y_pos = 100
            ctrl_rects = {}

            for action, key in controls.items():
                color = (0, 255, 0) if waiting_for_key == action else (255, 255, 255)
                label = font.render(f"{action}: {pygame.key.name(key).upper()}", True, color)
                rect = label.get_rect(center=(initial_limit // 2, y_pos))
                screen.blit(label, rect)
                ctrl_rects[action] = rect
                y_pos += 60

            screen.blit(Back, Back_rect)

            if Error_4:
                screen.blit(Error4, Error4_rect)

        elif menu_state == "Resolution":
            Increase = title_font.render(">", True, (255, 255, 255))
            Increase_rect = Increase.get_rect(center=(initial_limit // 2 + 100, initial_limit // 2 - 5))
            Limit = title_font.render(f"{limit}", True, (255, 255, 255))
            Limit_rect = Limit.get_rect(center=(initial_limit // 2, initial_limit // 2))
            Decrease = title_font.render("<", True, (255, 255, 255))
            Decrease_rect = Decrease.get_rect(center=(initial_limit // 2 - 100, initial_limit // 2 - 5))

            screen.blit(Increase, Increase_rect)
            screen.blit(Limit, Limit_rect)
            screen.blit(Decrease, Decrease_rect)
            screen.blit(Back, Back_rect)

            if Error_1:
                screen.blit(Error1, Error1_rect)
            elif Error_2:
                screen.blit(Error2, Error2_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                if menu_state == "Main":
                    if diff_rect.collidepoint(mouse_pos):
                        menu_state = "Difficulty"
                    elif settings_rect.collidepoint(mouse_pos):
                        menu_state = "Settings"
                    elif Start_rect.collidepoint(mouse_pos) and ticks > 0:
                        return
                    elif Start_rect.collidepoint(mouse_pos) and ticks == 0:
                        Error3 = error_font.render("Select a difficulty First", True, (255, 0, 0))
                        Error3_rect = Error3.get_rect(center=(initial_limit // 2, initial_limit // 2 + 200))
                        Error_3 = True

                elif menu_state == "Difficulty":
                    if E_rect.collidepoint(mouse_pos):
                        ticks = 5
                        menu_state = "Main"
                    if M_rect.collidepoint(mouse_pos):
                        ticks = 10
                        menu_state = "Main"
                    if H_rect.collidepoint(mouse_pos):
                        ticks = 15
                        menu_state = "Main"
                    if Back_rect.collidepoint(mouse_pos):
                        initial_limit = limit
                        menu_state = "Settings"


                elif menu_state == "Settings":
                    if control_rect.collidepoint(mouse_pos):
                        menu_state = "Controls"
                    if resolution_rect.collidepoint(mouse_pos):
                        menu_state = "Resolution"
                    if Back_rect.collidepoint(mouse_pos):
                        initial_limit = limit
                        menu_state = "Settings"

                elif menu_state == "Resolution":
                    if Increase_rect.collidepoint(mouse_pos) and limit + 30 < 1201:
                        limit += 30
                        initial_limit = limit
                        screen = pygame.display.set_mode((limit, limit))
                        Error_2 = False

                    elif Increase_rect.collidepoint(mouse_pos) and limit + 30 > 1200:
                        Error1 = error_font.render("Limit is 1200 max", True, (255, 0, 0))
                        Error1_rect = Error1.get_rect(center=(initial_limit // 2, initial_limit // 2 + 200))
                        Error_1 = True

                    if Decrease_rect.collidepoint(mouse_pos) and limit - 30 > 389:
                        limit -= 30
                        initial_limit = limit
                        screen = pygame.display.set_mode((limit, limit))
                        Error_1 = False

                    elif Decrease_rect.collidepoint(mouse_pos) and limit - 30 < 390:
                        Error2 = error_font.render("Limit is 390 min", True, (255, 0, 0))
                        Error2_rect = Error2.get_rect(center=(initial_limit // 2, initial_limit // 2 + 200))
                        Error_2 = True

                    if Back_rect.collidepoint(mouse_pos):
                        initial_limit = limit
                        menu_state = "Settings"

                elif menu_state == "Controls":
                    for action, rect in ctrl_rects.items():
                        if rect.collidepoint(mouse_pos):
                            waiting_for_key = action

                    if Back_rect.collidepoint(mouse_pos):
                        initial_limit = limit
                        menu_state = "Settings"

            if event.type == pygame.KEYDOWN and waiting_for_key:
                if event.key in controls.values():
                    Error4 = error_font.render(f"Key {pygame.key.name(event.key)} is already in use!", True, (255, 0, 0))
                    Error4_rect = Error4.get_rect(center=(initial_limit // 2, initial_limit // 2 + 200))
                    Error_4 = True
                else:
                    controls[waiting_for_key] = event.key
                    waiting_for_key = None
                    Error_4 = False

def end():
    text1 = font.render('Game Over!', True, (255, 255, 255))
    text2 = font.render(f"Score: {int(snake_length) - 3}", True, (255, 255, 255))
    screen.blit(text1, (limit // 2 - 100, limit // 2 - 50))
    screen.blit(text2, (limit // 2 - 100, limit // 2))
    pygame.display.flip()
    time.sleep(2)
    reset_game()

reset_game()

screen = pygame.display.set_mode((limit, limit))
running = True

while running:
    pygame.event.pump()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == controls["PAUSE"]:
                Paused = not Paused
            if event.key == controls["UP"] and direction != "down":
                direction = "up"
            elif event.key == controls["DOWN"] and direction != "up":
                direction = "down"
            elif event.key == controls["LEFT"] and direction != "right":
                direction = "left"
            elif event.key == controls["RIGHT"] and direction != "left":
                direction = "right"

    if Paused:
        screen.fill((0, 0, 0))
        text = font.render("Paused", True, (255, 255, 255))
        screen.blit(text, (limit // 2 - 60, limit // 2))
        pygame.display.flip()
        clock.tick(10)
        continue

    if direction == "right": x += speed
    if direction == "left":  x -= speed
    if direction == "up":    y -= speed
    if direction == "down":  y += speed

    if x < 0 or x >= limit or y < 0 or y >= limit:
        end()

    if [x, y] in snake_body[1:]:
        end()
        continue

    snake_body.insert(0, [x, y])
    if len(snake_body) > snake_length:
        snake_body.pop()

    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 0, 0), apple_rect)

    for i, segment in enumerate(snake_body):
        if i == 0:
            screen.blit(head_surf, (segment[0], segment[1]))
        else:
            screen.blit(square_surf, (segment[0], segment[1]))

    head_rect = pygame.Rect(x, y, size, size)
    if head_rect.colliderect(apple_rect):
        snake_length += 1
        apple_rect.x = random.randrange(30, limit - 60, size)
        apple_rect.y = random.randrange(30, limit - 60, size)

    pygame.display.flip()
    clock.tick(ticks)

pygame.quit()
