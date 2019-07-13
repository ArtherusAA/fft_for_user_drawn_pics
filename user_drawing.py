import sys, pygame
import time
from math import cos, pi, sin, sqrt, acos
import numpy as np

size = width, height = 1080, 900  # screen size
black = 0, 0, 0  # rgb of black color
white = 255, 255, 255 # rgb of white color


def get_user_drawn_picture(screen, size, width, height):
    curr_time = time.time()
    finish_signal = False
    curve = []
    while not finish_signal:
        screen.fill(black)
        if len(curve) > 1:
            pygame.draw.lines(screen, white, False, curve, 1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish_signal = True
                return curve
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(size, pygame.RESIZABLE)
            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    curve.append(event.pos)
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)
    curve = get_user_drawn_picture(screen, size, width, height)
    np.save('drawing', np.array(curve))
    pygame.quit()
