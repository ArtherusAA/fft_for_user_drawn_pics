import sys, pygame
import time
from math import cos, pi, sin, sqrt, acos

size = width, height = 1080, 900  # screen size
black = 0, 0, 0  # rgb of black color
white = 255, 255, 255 # rgb of white color

class Circle:     # class for circle objects
    def __init__(self, x = 0, y = 0, r = 1):
        self.x = x
        self.y = y
        self.radius = r
        self.angle = 0

    def change_coordinates(self, x, y):
        self.x, self.y = x, y

    def get_coordinates(self):
        return self.x, self.y

    def get_coordinates_of_point(self):
        return self.x + self.radius * cos(self.angle), self.y + self.radius * sin(self.angle)

    def change_angle(self, dphi):
        self.angle += dphi

    def draw(self, screen):
        if abs(round(self.radius)) > 0:
            pygame.draw.circle(screen, white, (round(self.x), round(self.y)), abs(round(self.radius)), 1)
            pygame.draw.line(screen, white, (round(self.x), round(self.y)),
                    (round(self.x + self.radius * cos(self.angle)),
                    round(self.y + self.radius * sin(self.angle))), 1)
        pass

def generate_circles(n):
    res = []
    x, y = 300.0, 300.0
    for i in range(0, n):
        k = 2 * i + 1
        res.append(Circle(x=x, y=y, r=300.0 * 8 * (-1) ** ((k - 1)//2)/((pi * k) ** 2)))
        x += 100.0 * 4/(pi * k)
    return res

def main(n=30):
    global size, width, height
    pygame.init()
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)
    curr_time = time.time()
    finish_signal = False
    objects = generate_circles(n)
    curve = []
    while not finish_signal:
        screen.fill(black)
        prev = objects[0].get_coordinates()
        for i in range(0, n):
            objects[i].change_angle((2 * i + 1) * 0.005 * pi)
            objects[i].change_coordinates(prev[0], prev[1])
            prev = objects[i].get_coordinates_of_point()
        curve.insert(0, prev[1])
        if len(curve) > 800:
            curve.pop()
        points = []
        for y in curve:
            points.append((len(points) + 450, y))
        pygame.draw.line(screen, white, points[0], objects[n - 1].get_coordinates_of_point(), 1)
        if len(points) > 1:
            pygame.draw.lines(screen, white, False, points, 1)
        for object in objects:
            object.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish_signal = True
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(size, pygame.RESIZABLE)
        pygame.display.flip()
        pygame.time.wait(20)
    pygame.quit()


if __name__ == "__main__":
    main()
