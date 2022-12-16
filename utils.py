import sys
from math import floor
from common import *

yPush = 0.000001

def GetCornerPositionsOfTile(pos : Pos) -> tuple:
    return (
        pos.Copy(),
        Pos(pos.x - 1 + Settings.tileSize, pos.y),
        Pos(pos.x, pos.y - yPush + Settings.tileSize),
        Pos(pos.x - 1 + Settings.tileSize, pos.y - yPush + Settings.tileSize)
    )

def CheckCollision(position : Pos, tilePositions : tuple, groundMap : list) -> bool:
    for tilePosition in tilePositions:
        # We'll check corner points of each tile for collision
        tilePosition = position + tilePosition * Settings.tileSize

        for cornerPosition in GetCornerPositionsOfTile(tilePosition):
            tileX = floor(cornerPosition.x / Settings.tileSize)
            tileY = floor(cornerPosition.y / Settings.tileSize)
            
            if tileX < 0 or tileX >= Settings.levelWidth \
            or tileY < 0 or tileY >= Settings.levelHeight \
            or groundMap[tileX][tileY] != 0:
                return True
    
    return False

# Rounds to closest number divisible by divider
def RoundTo(value, divider):
    return round(value / divider) * divider

# Linear interpolation
def Lerp(x, x1, y1, x0 = 0, y0 = 0):
    return (y0 * (x1 - x) + y1 * (x - x0)) / (x1 - x0)

def LerpColors(percent, c1, c2):
    return (
        Lerp(percent, 1, c2[0], 0, c1[0]),
        Lerp(percent, 1, c2[1], 0, c1[1]),
        Lerp(percent, 1, c2[2], 0, c1[2])
    )
