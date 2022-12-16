import pygame

class Settings:
    tileSize = 20
    levelWidth = 10
    levelHeight = 23
    lockTime = 400
    turnTime = 1200
    limitHeight = 13
    speed = 0.05
    fastforwardSpeed = 0.5

    # Moving block
    currentBlockColor = (255, 255, 255)
    # Locked blocks
    groundColor = (240, 55, 55)
    # Level background
    wallColor = (0, 0, 0)
    wallRect = pygame.Rect(10, 10, levelWidth * tileSize, levelHeight * tileSize)
    # Game background
    backgroundColor = (0, 0, 140)
    # Limit line
    limitLineRect = pygame.Rect(wallRect.left, wallRect.top + tileSize * limitHeight - 2, wallRect.width, 2)

class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return "{ x: " + str(self.x) + ", y: " + str(self.y) + " }"

    def __repr__(self) -> str:
        return "{ x: " + str(self.x) + ", y: " + str(self.y) + " }"

    def __add__(self, pos):
        return Pos(self.x + pos.x, self.y + pos.y)
    
    def __mul__(self, multiplier):
        return Pos(self.x * multiplier, self.y * multiplier)

    def Copy(self):
        return Pos(self.x, self.y)