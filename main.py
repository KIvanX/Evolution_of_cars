from random import random
import pygame as pg
import math


def draw_NN(xs, ys, size, window, brain):
    neurons = [5]
    list_weight = []
    for layer in range(len(brain)):
        neurons.append(len(brain[layer]) // neurons[-1])
        list_weight += brain[layer]
    max_neuron = max(neurons)

    all_cord = []
    for layer in range(len(neurons)):
        cord = []
        for i in range(neurons[layer]):
            k = (max_neuron - neurons[layer]) / 2 * size * 3
            x, y = xs + size * 15 * layer, ys + k + i * size * 3
            pg.draw.circle(window, [0, 0, 0], (x, y), size)
            cord.append((x, y))
        all_cord.append(cord)

    k = 0
    minl = min(list_weight)
    for i in range(len(all_cord)-1):
        for x, y in all_cord[i]:
            for x1, y1 in all_cord[i+1]:
                color = [int((list_weight[k]-minl)/(max(list_weight)-minl) * 250)]*3
                pg.draw.line(window, color, (x, y), (x1, y1))
                k += 1


class Car:
    def __init__(self, x, y, window, background):
        image_0 = pg.image.load(f'images/car{int(random() * 6) + 1}.png')
        image = pg.transform.rotate(image_0, 90)

        # self.brain = [[(random()-0.5) for _ in range(40)],
        #               [(random()-0.5) for _ in range(16)]]

        # self.brain = [[22.84314458508083, -2.403786660213477, 4.067291338767675, -0.17535794537611993, -18.588607027629543,
        #   0.9063969558308813, 13.668292261966467, -9.633478402673452, -23.061376875688893, -4.9157912384614715,
        #   7.368097090186204, 1.6835219424434833, 5.667847200524733, -20.366387560709352, -36.080943080583715,
        #   -20.469515530218285, -15.08489601214686, 1.1635338168581209, 3.701625122988467, 18.70740951741545,
        #   -7.717373947595668, -15.108877866065743, 4.191617367320692, -11.395812655607875, -8.823872282794799,
        #   -9.996330901436945, -7.304448546309481, 0.12063035002865745, -7.079232422239365, 22.13100851499116,
        #   -18.828551988300475, -4.1196580158521305, -2.4677846981351443, -8.787015826609935, 0.21528613185762008,
        #   -0.1244595722625797, -4.833825099853969, -8.758510801836945, 8.831100182149097, -18.9785963488911],
        #  [-0.8679404350638094, -24.56595774048922, -1.0714558828437029, 3.978776934645174, 7.997781732048607,
        #   5.69903247169785, -7.964746853149648, -0.30293168447046637, 9.115951369708194, -4.886571208722541,
        #   -5.256817214352713, -26.266776138250183, -0.47471345065048887, -21.835102456964062, -5.638944208869452,
        #   26.27073401077757]]

        # self.brain = [[(random()-0.5) for _ in range(30)],
        #               [(random()-0.5) for _ in range(24)],
        #               [(random()-0.5) for _ in range(8)]]

        self.brain = [[(random()-0.5) for _ in range(10)]]

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
            c = self.background.get_at((int(x1), int(y1)))
            if abs(c[0] - 35) + abs(c[1] - 177) + abs(c[2] - 77) < 100 or sum(c[:3]) < 100:
                return True
        return False

    def _think(self, lengths: list[5]):
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

    def _get_lengths(self, angs: list[5]):
        w, h = self.car.get_size()
        lengths = []
        for k in angs:
            angle, leng, block = self.ang + k, 10, False
            while leng < 300 and not block:
                x1 = self.x + w // 2 - math.sin(math.radians(angle)) * leng
                y1 = self.y + h // 2 - math.cos(math.radians(angle)) * leng
                c = self.background.get_at((int(x1), int(y1)))
                if abs(c[0] - 127) + abs(c[1] - 127) + abs(c[2] - 127) > 100:
                    block = True
                leng += 1
            lengths.append(leng-5)
        return lengths

    def move(self):
        lengths = self._get_lengths([-90, 45, 0, 45, 90])

        speed, a = self._think([leng / 100 for leng in lengths])

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
pg.display.set_caption('Эволюция машинок')
clock = pg.time.Clock()
font = pg.font.SysFont('cambriacambriamath', 22)

POPULATION, PARENTS = 12, 2

cars = []
for _ in range(POPULATION):
    cars.append(Car(90, 250, window, background))

game, FPS, mutations, gener, step = True, 150, 100, 1, 0
while game:
    step += 1
    clock.tick(FPS)

    window.blit(background, (0, 0))
    render = font.render('FPS ' + str(FPS)
                         + '   Мутации ' + str(mutations)
                         + '   Поколение ' + str(gener)
                         + '   Шаг ' + str(step), True, (0, 50, 0))
    window.blit(render, (10, 10))

    num_live = 0
    for car in cars:
        if not car.crash:
            num_live += 1
            car.move()
            if num_live == 1:
                car.draw()

    if num_live == 0 or step > 1500:
        step = 0
        gener += 1

        cars = sorted(cars, reverse=True, key=lambda car: car.score)[:PARENTS]

        children = []
        for car in cars:
            for i in range(POPULATION // PARENTS):
                child = Car(90, 250, window, background)
                for layer in range(len(child.brain)):
                    for gen in range(len(child.brain[layer])):
                        child.brain[layer][gen] = car.brain[layer][gen] + (random() - 0.5) / 100 * mutations
                children.append(child)

        cars = children

    draw_NN(10, 470, 3, window, cars[0].brain)
    pg.display.flip()

    for e in pg.event.get():
        if e.type == pg.QUIT:
            game = False

        if e.type == pg.KEYUP:
            if e.key == pg.K_g:
                print(cars[0].brain)
            if e.key in [pg.K_1, pg.K_2, pg.K_3, pg.K_4, pg.K_5]:
                level = [pg.K_1, pg.K_2, pg.K_3, pg.K_4, pg.K_5].index(e.key) + 1
                background = pg.image.load('images/background' + str(level) + '.png')

    if pg.key.get_pressed()[pg.K_UP]:
        mutations += 1

    if pg.key.get_pressed()[pg.K_DOWN] and mutations > 0:
        mutations -= 1

    if pg.key.get_pressed()[pg.K_RIGHT] and FPS < 400:
        FPS += 1

    if pg.key.get_pressed()[pg.K_LEFT] and FPS > 1:
        FPS -= 1
