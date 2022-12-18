from datetime import datetime
import sys, pygame
from game import Game
from common import Settings

pygame.init()

size = width, height = 640, 480
dx = 1
dy = 1
x= 163
y = 120
black = (0,0,0)
white = (255,255,255)

pygame.screen = screen = pygame.display.set_mode(size)
Settings.font = pygame.font.SysFont(None, 38)


game = Game()
lastTime = datetime.now()
clock = pygame.time.Clock()

while 1:
    newTime = datetime.now()
    delta = newTime - lastTime
    delta = delta.microseconds / 1000
    lastTime = newTime

    game.HandleEvents()
    game.Update(delta)
    game.Draw()

    pygame.display.flip()

    # Cap the frame rate
    clock.tick(200)

class BattleshipsGame:
    def __init__(self):
        pass


