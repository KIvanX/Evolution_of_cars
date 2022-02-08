import pygame as pg
import math
from random import random


class Car:
    def __init__(self, x, y, window, background):
        k = int(random()*6)+1
        image = pg.image.load('images/car' + str(k) + '.png')
        # image.set_colorkey((255, 255, 255))
        image = pg.transform.rotate(image, 90)

        self.brain = [[(random()-0.5) for _ in range(40)],
                      [(random()-0.5) for _ in range(16)]]
        # self.brain = [[1.175, 0.509, -0.161, -2.653, -1.304, 0.665, -0.171, 2.652, -1.224, 0.046, 1.268, -0.635, -0.256, 0.354, -0.134, -2.026, -0.014, 1.11, -2.907, -0.084, -0.133, -1.339, -1.984, -1.279, 1.267, -0.664, -2.082, 3.788, -2.847, 1.558, -0.235, -1.408, 3.072, 0.359, -1.369, 0.153, 0.416, 0.988, -0.702, 2.594],
        #               [1.022, -0.789, 1.219, -0.413, -2.422, 2.486, 1.358, 2.981, -0.944, -1.224, -1.306, 0.533, 0.717, -0.135, -1.511, -4.478]]

        self.car = pg.transform.scale(image, (20, 33))
        self.window, self.background = window, background
        self.x, self.y = x, y
        self.score, self.crash = 0, False
        self.ang, self.speed = 0, 0

    def draw(self):
        w, h = self.car.get_size()
        x, y = self.x + w // 2, self.y + h // 2
        rect = self.car.get_rect(center=(x, y))
        rot_car = pg.transform.rotate(self.car, self.ang)
        rot_rect = rot_car.get_rect(center=rect.center)
        self.window.blit(rot_car, rot_rect)

    def is_crash(self, x, y):
        w, h = self.car.get_size()
        leng = ((w / 2) ** 2 + (h / 2) ** 2) ** 0.5 - 5
        for a in [30, 150, 210, 330]:
            x1 = x + w // 2 + math.sin(math.radians(self.ang - a)) * leng
            y1 = y + h // 2 + math.cos(math.radians(self.ang - a)) * leng
            c = background.get_at((int(x1), int(y1)))
            if abs(c[0] - 35) + abs(c[1] - 177) + abs(c[2] - 77) < 100 or sum(c[:3]) < 100:
                return True
        return False

    def think(self, lengths):
        outputs = lengths
        arr_outputs = [outputs]
        for weights in self.brain:
            inputs = []
            num_i = len(weights) // len(outputs)
            for i in range(num_i):
                summ = 0
                for o in range(len(outputs)):
                    summ += outputs[o] * weights[o * num_i + i]

                inputs.append(1 / (1 + 2.71828 ** (-summ)))

            arr_outputs.append(inputs)
            outputs = inputs.copy()
        return outputs

    def get_lengths(self, angs):
        w, h = self.car.get_size()
        lengths = []
        for k in angs:
            angle, leng, block = self.ang + k, 10, False
            while leng < 300 and not block:
                x1 = self.x + w // 2 - math.sin(math.radians(angle)) * leng
                y1 = self.y + h // 2 - math.cos(math.radians(angle)) * leng
                c = background.get_at((int(x1), int(y1)))
                if abs(c[0] - 127) + abs(c[1] - 127) + abs(c[2] - 127) > 100:
                    block = True
                leng += 1
            lengths.append(leng-5)
        return lengths

    def move(self):
        lengths = self.get_lengths([-90, 45, 0, 45, 90])
        speed, a = self.think([l / 100 for l in lengths])

        self.speed = int(speed * 10)
        self.ang += int((a - 0.5) * 10)
        self.x -= math.sin(math.radians(self.ang)) * self.speed
        self.y -= math.cos(math.radians(self.ang)) * self.speed

        if self.is_crash(self.x, self.y) or self.speed == 0:
            self.crash = True
        else:
            self.score += speed


background = pg.image.load('images/background1.png')

n, m = background.get_size()
pg.init()
window = pg.display.set_mode((n, m))
pg.display.set_caption('Эволюция 3')
clock = pg.time.Clock()
font = pg.font.SysFont('cambriacambriamath', 22)

popul, parents, mut = 12, 2, 150

cars = []
for _ in range(popul):
    cars.append(Car(90, 250, window, background))

game, FPS, gener, step = True, 150, 1, 0
while game:
    step += 1
    clock.tick(FPS)

    window.blit(background, (0, 0))
    render = font.render('FPS ' + str(FPS)
                         + '   Мутации ' + str(mut)
                         + '   Поколение ' + str(gener)
                         + '   Шаг ' + str(step), True, (0, 50, 0))
    window.blit(render, (10, 10))

    test = False
    for car in cars:
        if not car.crash:
            test = True
            car.move()
            car.draw()

    if not test or step > 2000:
        step = 0
        gener += 1

        cars = sorted(cars, reverse=True, key=lambda car: car.score)[:parents]

        children = []
        for car in cars:
            for i in range(popul // parents):
                child = Car(90, 250, window, background)
                for layer in range(len(child.brain)):
                    for gen in range(len(child.brain[layer])):
                        child.brain[layer][gen] = car.brain[layer][gen] + (random() - 0.5) / 100 * mut
                children.append(child)

        cars = children

    pg.display.flip()

    for e in pg.event.get():
        if e.type == pg.QUIT:
            game = False

        if e.type == pg.KEYUP:
            if e.key == pg.K_g:
                print(cars[0].brain)
            if e.key in [pg.K_1, pg.K_2, pg.K_3, pg.K_4]:
                level = [pg.K_1, pg.K_2, pg.K_3, pg.K_4].index(e.key) + 1
                background = pg.image.load('images/background' + str(level) + '.png')

    if pg.key.get_pressed()[pg.K_UP]:
        mut += 1

    if pg.key.get_pressed()[pg.K_DOWN] and mut > 0:
        mut -= 1

    if pg.key.get_pressed()[pg.K_RIGHT] and FPS < 400:
        FPS += 1

    if pg.key.get_pressed()[pg.K_LEFT] and FPS > 1:
        FPS -= 1

