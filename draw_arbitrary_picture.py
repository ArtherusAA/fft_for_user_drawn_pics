import sys, pygame
import time
from math import cos, pi, sin, sqrt, acos, atan2
import cmath
import numpy

size = width, height = 1080, 900  # screen size
black = 0, 0, 0  # rgb of black color
white = 255, 255, 255 # rgb of white color
red = 255, 0, 0 # rgb of red color
green = 0, 255, 0 # rgb of green color
blue = 0, 0, 255 # rgb of blue color
number_of_integration_steps = 5000 # number of steps which integration function will make
picture_filename = 'drawing.npy' # name of numpy file where numpy array of picture's points is stored
functionY = []

class Circle:     # class for circle objects
    def __init__(self, x = 0, y = 0, r = 1, k = 1, angle = 0):
        self.x = x
        self.y = y
        self.radius = r
        self.angle = angle
        self.k = k

    def change_coordinates(self, x, y):
        self.x, self.y = x, y

    def get_radius(self):
        return self.radius

    def get_coordinates(self):
        return self.x, self.y

    def get_coordinates_of_point(self):
        return self.x + self.radius * cos(self.angle), self.y + self.radius * sin(self.angle)

    def change_angle(self, dphi):
        self.angle += self.k * dphi

    def draw(self, screen):
        if round(self.radius) != 0:
            pygame.draw.circle(screen, white, (round(self.x), round(self.y)), round(self.radius), 1)
        pygame.draw.line(screen, green, (round(self.x), round(self.y)),
                    (round(self.x + self.radius * cos(self.angle)),
                    round(self.y + self.radius * sin(self.angle))), 1)
        pass


def convert_pic_to_complex_function(filename):
    global functionY
    points = numpy.load(filename)
    functionY = []
    for point in points:
        functionY.append(complex(point[0], point[1]))
    return functionY

def f(x):
    if x < 0.0:
        x = 0.0
    elif x > 1.0:
        x = 1.0
    return functionY[round(x * (len(functionY) - 1))]

def integrate(f, a, b, n):
    res = complex(0, 0)
    dx = (b - a) / n
    for i in range(0, n):
        res += f(a + i * dx) * dx
    return res

def generate_circles(n):
    res = []
    c = {}
    convert_pic_to_complex_function(picture_filename)
    for i in range(0, n):
        c[i] = integrate(lambda t:
                f(t) * cmath.exp(complex(0, -2 * pi * i * t)),
                0, 1, max(2 * len(functionY), number_of_integration_steps))
        c[-i] = integrate(lambda t:
                f(t) * cmath.exp(complex(0, -2 * pi * -i * t)),
                0, 1, max(2 * len(functionY), number_of_integration_steps))
    for i in range(0, n):
        res.append(Circle(x=0.0, y=0.0, r=abs(c[i]), k=i,
                                        angle=cmath.phase(c[i])))
        if i > 0:
            res.append(Circle(x=0.0, y=0.0, r=abs(c[-i]), k=-i,
                                        angle=cmath.phase(c[-i])))
    return sorted(res, key = lambda x: x.get_radius(), reverse = True)

def main(n=50):
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
        for i in range(0, len(objects)):
            objects[i].change_angle(0.005)
            objects[i].change_coordinates(prev[0], prev[1])
            prev = objects[i].get_coordinates_of_point()
        curve.append((prev[0], prev[1]))
        if len(curve) > 1400:
            curve.pop(0)
        if len(curve) > 1:
            pygame.draw.lines(screen, red, False, curve, 1)
        for object in objects:
            object.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish_signal = True
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(size, pygame.RESIZABLE)
        pygame.display.flip()
        #pygame.time.wait(20)
    pygame.quit()


if __name__ == "__main__":
    main(100)
