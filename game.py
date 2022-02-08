
import pygame as pg
import math


class Car:
    def __init__(self, x, y, window, background):
        image = pg.image.load('images/car1.png')
        image = pg.transform.rotate(image, 90)
        self.car = pg.transform.scale(image, (20, 33))
        self.window, self.background = window, background
        self.x, self.y = x, y
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
        leng = ((w / 2)**2 + (h / 2)**2)**0.5-5
        for a in [30, 150, 210, 330]:
            x1 = x + w // 2 + math.sin(math.radians(self.ang-a)) * leng
            y1 = y + h // 2 + math.cos(math.radians(self.ang-a)) * leng
            c = background.get_at((int(x1), int(y1)))
            if abs(c[0] - 35) + abs(c[1] - 177) + abs(c[2] - 77) < 100:
                return True
        return False

    def get_lengths(self, angs):
        w, h = self.car.get_size()
        lengths = []
        for k in angs:
            angle, leng, block = self.ang + k, 10, False
            while leng < 300 and not block:
                x1 = self.x + w // 2 - math.sin(math.radians(angle)) * leng
                y1 = self.y + h // 2 - math.cos(math.radians(angle)) * leng
                c = background.get_at((int(x1), int(y1)))
                if abs(c[0]-127) + abs(c[1]-127) + abs(c[2]-127) > 100:
                    block = True
                pg.draw.circle(window, (0, 0, 0), (x1, y1), 1)
                leng += 1
                lengths.append(leng-5)
        return lengths

    def move(self):
        self.speed = self.speed + 0.05 if self.speed < 6 else 6
        for _ in range(int(self.speed)):
            x1 = math.sin(math.radians(self.ang))
            y1 = math.cos(math.radians(self.ang))
            if not self.is_crash(self.x - x1*10, self.y - y1*10):
                self.x, self.y = self.x - x1, self.y - y1
            else:
                self.speed -= 0.05
                if not self.is_crash(self.x - x1, self.y):
                    self.x -= math.sin(math.radians(self.ang))
                elif not self.is_crash(self.x, self.y - y1):
                    self.y -= math.cos(math.radians(self.ang))
                else:
                    self.speed = 0

    def control(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                return False
            if e.type == pg.KEYUP:
                if e.key == pg.K_UP:
                    self.speed += 3
                if e.key == pg.K_DOWN:
                    self.speed -= 2

        if pg.key.get_pressed()[pg.K_LEFT]:
            self.ang += 3
        if pg.key.get_pressed()[pg.K_RIGHT]:
            self.ang -= 3

        return True


background = pg.image.load('images/background2.png')

n, m = background.get_size()
pg.init()
window = pg.display.set_mode((n, m))
clock = pg.time.Clock()
font = pg.font.SysFont('cambriacambriamath', 32)

car = Car(90, 250, window, background)


game = True
while game:
    clock.tick(60)

    window.blit(background, (0, 0))

    car.move()
    car.draw()
    # car.get_lengths([-90, -45, 0, 45, 90])
    game = car.control()

    pg.display.flip()
