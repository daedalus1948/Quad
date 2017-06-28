# this is a NON-COMMERCIAL project created for educative purposes
# the aim of this project is to introduce  basics concept of programming a video-game
# FPS, rendering, game loop, keystroke events and game logic are discussed below
# many concepts are simplified due to the abstractions provided by the PyGame library
# this example does not aim to represent a completely finished video-game
# or any particular video-game in general even though it draws inspiration from arcade games
# some notable issues are not addressed (collision detection between objects) for the sake of simplicity
# thank you creators of Python and PyGame for making this possible
# created by Daedalus1948@github, 2017

import pygame
import random


class Board:
    data = []

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.data = [[0 for _ in range(x)] for _ in range(y)]

    def update(self):
        self.data = [[0 for _ in range(self.x)] for _ in range(self.y)]
        for part in all_parts:
            if part.y < board.y and part.x < board.x:
                self.data[part.y][part.x] = part.value

    def clear_rows(self):
        for row in range(len(board.data)):
            if sum(board.data[row]) == 3 * len(board.data[row]):
                for i in range(len(all_parts) - 1, -1, -1):
                    if all_parts[i].y == row:
                        del all_parts[i]
                        global score
                        score += 1
                for part in all_parts:
                    if part.y < row:
                        part.y += 1
                global speed
                speed += 1
                global game_speed
                game_speed = pygame.time.set_timer(31, 1000 - (speed * 100))
        self.update()


class Quad:
    land = False
    _blueprints = [[[-1, 0], [0, 0], [1, 0], [1, 1]], [[-1, 0], [0, 0], [1, 0], [2, 0]],
                   [[-1, 0], [0, 0], [1, 0], [0, -1]], [[-1, 0], [0, 0], [0, 1], [1, 1]],
                   [[-1, 0], [0, 0], [-1, 1], [0, 1]]]

    def __init__(self, x, y):
        self.color = (rand_color())
        self.pivot = [x, y]
        self.blueprint = self._blueprints[random.randint(0, len(self._blueprints)-1)]
        self.real = []
        self.build()

    def build(self):
        for part in self.blueprint:
            self.real.append(Part(part[0]+self.pivot[0], part[1]+self.pivot[1], self.color, 3))

    def rotate(self):
        for point in self.blueprint:
            point[0], point[1] = -point[1], point[0]
        for i, point in enumerate(self.real):
            point.x = self.pivot[0] + self.blueprint[i][0]
            point.y = self.pivot[1] + self.blueprint[i][1]

    def move(self, new_x, new_y):
        if self.test_position(new_x, new_y):
            self.pivot[0] += new_x
            self.pivot[1] += new_y
            for part in self.real:
                part.x += new_x
                part.y += new_y

    def test_position(self, x, y):  # check for collision detection based on the new coordinates
        for part in self.real:  # tests only the move(), not the rotate()
            new_x = part.x+x  # calculate new x
            new_y = part.y+y  # calculate new y
            if 0 <= new_x <= board.x - 1 and new_y <= board.y - 1:  # inside the game board, disable above-check
                if board.data[new_y][new_x] == 0:
                    if new_y == board.y-1:  # landed on bottom
                        self.land = True
                if board.data[new_y][new_x] == 3:  # quad position
                    if y > 0:  # landed on another quad
                        self.land = True
                    return False
            else:
                return False
        return True


class Part:
    def __init__(self, x, y, color, value):
        self.x = x
        self.y = y
        self.color = color
        self.value = value
        all_parts.append(self)


def draw_objects_and_info():
    ln = len(board.data)
    for part in all_parts:
        pygame.draw.rect(screen, part.color, ((part.x*res[0]//ln, part.y*res[1]//ln), (res[0]//ln, res[1]//ln)))
    screen.blit(score_text.render("SCORE: " + str(score), True, (255, 0, 0)), (res[0] - 100, 10))
    screen.blit(score_text.render("SPEED: " + str(speed), True, (255, 0, 0)), (res[0] - 98, 30))


def rand_color():
    return random.randint(10, 255), random.randint(10, 255), random.randint(10, 255)

pygame.init()

res = (600, 600)  # const
screen = pygame.display.set_mode(res)  # const
game_speed = pygame.time.set_timer(31, 1000)  # modified by clear_rows()
all_parts = []  # global modified by clear_rows() and a new Quad instance
board = Board(12, 12)  # const
quad = Quad(board.x // 2 - 1, 0)  # const
clock = pygame.time.Clock()  # const
score = 0  # modified by clear_rows()
speed = 0  # modified by clear_rows()
score_text = pygame.font.Font(None, 24)  # const
speed_text = pygame.font.Font(None, 24)  # const
playing = True

while playing:
    for event in pygame.event.get():
        if event.type == 31:
            pass
            quad.move(0, 1)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                playing = False
            if event.key == pygame.K_DOWN:
                quad.move(0, 1)
            if event.key == pygame.K_LEFT:
                quad.move(-1, 0)
            if event.key == pygame.K_RIGHT:
                quad.move(1, 0)
            if event.key == pygame.K_r:
                quad.rotate()

    pygame.Surface.fill(screen, (0, 0, 0))

    if quad.land:
        board.update()
        board.clear_rows()
        quad = Quad(board.x // 2 - 1, 0)

    draw_objects_and_info()
    pygame.display.update()
    clock.tick(30)
