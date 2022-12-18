import random, pygame
from common import *

class Block:
    def __init__(self):
        self.rotation = 0
        self.tilePositions = self.tileShapes[0]
        self.color = Settings.currentBlockColor

    def Draw(self):
        for tilePosition in self.tilePositions:

            x = Settings.wallRect.left + self.position.x + tilePosition.x * Settings.tileSize
            y = Settings.wallRect.top + self.position.y + tilePosition.y * Settings.tileSize

            tileRect = pygame.Rect(x, y, Settings.tileSize, Settings.tileSize)
            pygame.draw.rect(pygame.screen, self.color, tileRect)

    def Rotate(self, turnCount):
        self.rotation += turnCount
        
        if self.rotation < 0:
            self.rotation = 3
        elif self.rotation > 3:
            self.rotation = 0
        
        self.tilePositions = self.tileShapes[self.rotation]

    '''def Rotate(self):
        # for tilePosition in self.tilePositions:
        newTilePositions = []

        for tilePosition in self.tilePositions:
            xPivot = 0
            yPivot = 0
            xBrickCenter = tilePosition.x + 0.5
            yBrickCenter = tilePosition.y + 0.5
            
            x = xBrickCenter - xPivot
            y = yBrickCenter - yPivot

            x1 = -y = yPivot - yBrickCenter
            y1 = x = xBrickCenter - xPivot

            newXBrickCenter = xPivot + x1 = xPivot + yPivot - yBrickCenter
            newYBrickCenter = yPivot + y1 = yPivot - xPivot + xBrickCenter

                        
            newTilePositions.append(Pos(x, y))'''

class Square(Block):
    tileShapes = (
        (Pos(-1, -1), Pos(0, -1), Pos(-1, 0), Pos(0, 0)),
        (Pos(-1, -1), Pos(0, -1), Pos(-1, 0), Pos(0, 0)),
        (Pos(-1, -1), Pos(0, -1), Pos(-1, 0), Pos(0, 0)),
        (Pos(-1, -1), Pos(0, -1), Pos(-1, 0), Pos(0, 0))
    )

class Long(Block):
    tileShapes = (
        (Pos(-2, -1), Pos(-1, -1), Pos(0, -1), Pos(1, -1)),
        (Pos(-1, -2), Pos(-1, -1), Pos(-1, 0), Pos(-1, 1)),
        (Pos(-2, 0), Pos(-1, 0), Pos(0, 0), Pos(1, 0)),
        (Pos(0, -2), Pos(0, -1), Pos(0, 0), Pos(0, 1))
    )

class T(Block):
    tileShapes = (
        (Pos(-1, -1), Pos(-2, -0), Pos(-1, 0), Pos(0, 0)),
        (Pos(0, -1), Pos(-1, -2), Pos(-1, -1), Pos(-1, 0)),
        (Pos(0, 0), Pos(1, -1), Pos(0, -1), Pos(-1, -1)),
        (Pos(-1, 0), Pos(0, 1), Pos(0, 0), Pos(0, -1))
    )

class Z(Block):
    tileShapes = (
        (Pos(-2, -1), Pos(-1, -1), Pos(-1, 0), Pos(0, 0)),
        (Pos(0, -2), Pos(0, -1), Pos(-1, -1), Pos(-1, 0)),
        (Pos(1, 0), Pos(0, 0), Pos(0, -1), Pos(-1, -1)),
        (Pos(-1, 1), Pos(-1, 0), Pos(0, 0), Pos(0, -1))
    )

class RevZ(Block):
    tileShapes = (
        (Pos(-1, 0), Pos(0, 0), Pos(0, -1), Pos(1, -1)),
        (Pos(-1, -1), Pos(-1, 0), Pos(0, 0), Pos(0, 1)),
        (Pos(0, -1), Pos(-1, -1), Pos(-1, 0), Pos(-2, 0)),
        (Pos(-1, -2), Pos(-1, -1), Pos(0, -1), Pos(0, 0))
    )

class L(Block):
    tileShapes = (
        (Pos(-1, -2), Pos(-1, -1), Pos(-1, 0), Pos(0, 0)),
        (Pos(-1, -1), Pos(-1, 0), Pos(0, -1), Pos(1, -1)),
        (Pos(-1, -1), Pos(0, -1), Pos(0, 0), Pos(0, 1)),
        (Pos(0, -1), Pos(-2, 0), Pos(-1, 0), Pos(0, 0))
    )

class RevL(Block):
    tileShapes = (
        (Pos(0, -2), Pos(0, -1), Pos(0, 0), Pos(-1, 0)),
        (Pos(-1, -1), Pos(-1, 0), Pos(0, 0), Pos(1, 0)),
        (Pos(-1, -1), Pos(0, -1), Pos(-1, 0), Pos(-1, 1)),
        (Pos(-2, -1), Pos(-1, -1), Pos(0, -1), Pos(0, 0))
    )

blocks = (
    Square(),
    Long(),
    T(),
    Z(),
    RevZ(),
    L(),
    RevL(),
)

def GetRandom():
    return random.choice(blocks)