import pygame
import scenes

pygame.init()
screen = pygame.display.set_mode((0, 0))
LOGICAL_WIDTH = 1920
LOGICAL_HEIGHT = 1080
display = pygame.Surface((LOGICAL_WIDTH, LOGICAL_HEIGHT))  # we will draw on this surface then transform it to screen coordinates
clock = pygame.time.Clock()

active_scene = scenes.MainMenu(screen)  # TODO

while active_scene != None:
    pressed_keys = pygame.key.get_pressed()

    # Event filtering
    filtered_events = []
    for event in pygame.event.get():
        quit_attempt = False
        if event.type == pygame.QUIT:
            quit_attempt = True
        elif event.type == pygame.KEYDOWN:
            alt_pressed = pressed_keys[pygame.K_LALT] or \
                          pressed_keys[pygame.K_RALT]
            if event.key == pygame.K_ESCAPE:
                quit_attempt = True
            elif event.key == pygame.K_F4 and alt_pressed:
                quit_attempt = True
        elif event.type in [pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION]:
            # transform from actual screen coordinates to logical coordinates
            scaling_factor_x = LOGICAL_WIDTH / screen.get_width()
            scaling_factor_y = LOGICAL_HEIGHT / screen.get_height()
            event.pos = (event.pos[0]*scaling_factor_x, event.pos[1]*scaling_factor_y)

        if quit_attempt:
            active_scene.terminate()
        else:
            filtered_events.append(event)

    active_scene.process_input(filtered_events, pressed_keys)
    active_scene.update()
    active_scene.render(display)

    pygame.transform.scale(display, screen.get_size(), screen)

    active_scene = active_scene.next

    pygame.display.flip()
    # clock.tick(120)   # run at a max of 120 fps