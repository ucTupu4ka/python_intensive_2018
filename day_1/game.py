import math
import os
import random
import turtle

BASE_PATH = os.path.dirname(os.path.dirname(__file__))

window = turtle.Screen()
window.setup(1200 + 29, 800 + 3)
window.bgpic(os.path.join(BASE_PATH, "images", "background.png"))
window.screensize(1200, 800)
#window.tracer(n=2)

BASE_X, BASE_Y = 0, -300
ENEMY_COUNT = 5



class Missile:

    def  __init__(self, x, y, color, x2, y2):
        self.x = x
        self.y = y
        self.color = color

        pen = turtle.Turtle(visible=False)
        pen.speed(0)
        pen.color(color)
        pen.penup()
        pen.setpos(x=x, y=y)
        pen.pendown()
        heading = pen.towards(x2, y2)
        pen.setheading(heading)
        pen.showturtle()
        self.pen  = pen

        self.state = 'launched'
        self.target = x2, y2
        self.radius = 0


    def step(self):
        pass


def fire_missile(x, y):
    info =  Missile(color='white', x=BASE_X, y=BASE_Y, x2=x, y2=y)
    our_missiles.append(info)


def fire_enemy_missile():
    x = random.randint(-600, 600)
    y = 380
    info = Missile(color='red', x=x, y=y, x2=BASE_X, y2=BASE_Y)
    enemy_missiles.append(info)


def move_missiles(missiles):
    for info in missiles:
        state = info['state']
        missile = info['missile']
        if state == 'launched':
            missile.forward(4)
            target = info['target']
            if missile.distance(x=target[0], y=target[1]) < 20:
                info['state'] = 'explode'
                missile.shape('circle')
        elif state == 'explode':
            info['radius'] += 1
            if info['radius'] > 5:
                missile.clear()
                missile.hideturtle()
                info['state'] = 'dead'
            else:
                missile.shapesize(info['radius'])
        elif state == 'dead':
            missile.clear()
            missile.hideturtle()

    dead_missiles = [info for info in missiles if info['state'] == 'dead']
    for dead in dead_missiles:
        missiles.remove(dead)


def check_interceptions():
    for our_info in our_missiles:
        if our_info['state'] != 'explode':
            continue
        our_missile = our_info['missile']
        for enemy_info in enemy_missiles:
            enemy_missile = enemy_info['missile']
            if enemy_missile.distance(our_missile.xcor(), our_missile.ycor()) < our_info['radius'] * 10:
                enemy_info['state'] = 'dead'


def check_enemy_count():
    if len(enemy_missiles) < ENEMY_COUNT:
        fire_enemy_missile()


window.onclick(fire_missile)

our_missiles = []
enemy_missiles = []


base = turtle.Turtle()
base.hideturtle()
base.speed(0)
base.penup()
base.setpos(x=BASE_X, y=BASE_Y)
base.showturtle()
pic_path = os.path.join(BASE_PATH, "images", "base.gif")
window.register_shape(pic_path)
base.shape(pic_path)


base_health = 2000


def game_over():
    return base_health < 0


def check_inpact():
    global base_health
    for enemy_info in enemy_missiles:
        if enemy_info['state'] != 'explode':
            continue
        enemy_missile = enemy_info['missile']
        if enemy_missile.distance(BASE_X, BASE_Y) < enemy_info['radius'] * 10:
            base_health -= 100


while True:
    window.update()
    if game_over():
        continue
    check_inpact()
    check_enemy_count()
    check_interceptions()
    move_missiles(missiles=our_missiles)
    move_missiles(missiles=enemy_missiles)
