from math import floor
import pygame
#from scipy.interpolate import interp1d
import blocks
from blocks import Pos
from common import *
import utils
from input import *
from states import *

class DefaultState(DrawState):
    def __init__(self, game):
        self.game = game
        self.lockTimer = 0

    def Enter(self):
        game = self.game

        if game.currentBlock == None:
            game.currentBlock = blocks.GetRandom()
            game.currentBlock.position = Pos(Settings.levelWidth / 2 * Settings.tileSize, 2 * Settings.tileSize)
    
    def Update(self):
        game = self.game
        currentBlock = game.currentBlock

        if currentBlock == None:
            return
        
        if game.input.hardDrop:
            newPos = currentBlock.position.Copy()
            
            # Add to Y position until it collides, remove reminder
            while utils.CheckCollision(newPos, currentBlock.tilePositions, game.groundMap) == False:
                newPos.y += Settings.tileSize / 2
            
            newPos.y = utils.RoundTo(newPos.y, Settings.tileSize)
            self.lockTimer = 0
            currentBlock.position = newPos
            game.stateMachine.TransitionTo("Locking")

            return
        
        newPos = currentBlock.position.Copy()
        speed = Settings.fastforwardSpeed if game.input.y > 0 else Settings.speed
        
        newPos.y += speed * game.delta
        COLLIDING = False

        if utils.CheckCollision(newPos, currentBlock.tilePositions, game.groundMap):
            COLLIDING = True
            # New Y position collides, remove reminder
            newPos.y = utils.RoundTo(newPos.y, Settings.tileSize)

            # Lock if lock timer is up
            self.lockTimer += game.delta

            if self.lockTimer > Settings.lockTime:
                self.lockTimer = 0
                currentBlock.position = newPos
                game.stateMachine.TransitionTo("Locking")
                return
            else:
                currentBlock.color = utils.LerpColors(self.lockTimer / Settings.lockTime, Settings.currentBlockColor, Settings.groundColor)

        else:
            self.lockTimer = 0
            currentBlock.color = Settings.currentBlockColor
        
        #print("COLLIDING: " + str(COLLIDING))

        if game.input.x != 0:
            #if COLLIDING:
            #    print("trying to move X while Y collides")

            newPos.x += Settings.tileSize * game.input.x
        
            if utils.CheckCollision(newPos, currentBlock.tilePositions, game.groundMap):
                # New X position collides, do not move on X axis
                newPos.x = currentBlock.position.x
                yReminderToNext = newPos.y % Settings.tileSize

                # Check if block can 'wiggle' into next open x block
                if yReminderToNext < Settings.wiggleRoom:
                    checkPos = Pos(newPos.x + Settings.tileSize * game.input.x, utils.RoundTo(newPos.y + Settings.tileSize, Settings.tileSize))
                    
                    if utils.CheckCollision(checkPos, currentBlock.tilePositions, game.groundMap) == False:
                        newPos = checkPos

        currentBlock.position = newPos

        if game.input.rotate != 0:
            currentBlock.Rotate(game.input.rotate)

            if utils.CheckCollision(currentBlock.position, currentBlock.tilePositions, game.groundMap):
                # New rotation collides, rotate back
                currentBlock.Rotate(-game.input.rotate)
    
    def Draw(self):
        self.game.DrawWall(Settings.wallColor)
        self.game.DrawGround(Settings.groundColor)
        self.game.DrawLimitLine()
        img = Settings.font.render("state: default", True, (0, 0, 0))
        pygame.screen.blit(img, (220, 300))
    
    def Exit(self):
        pass

class LockingState(DrawState):
    def __init__(self, game):
        self.game = game
        self.timer = 0

    def Enter(self):
        pass
    
    def Update(self):
        game = self.game
        game.currentBlock.color = Settings.currentBlockColor
        overLimit = False

        for tilePos in game.currentBlock.tilePositions:
            tileX = floor(game.currentBlock.position.x / Settings.tileSize + tilePos.x)
            tileY = floor(game.currentBlock.position.y / Settings.tileSize + tilePos.y)

            if tileY < Settings.limitHeight:
                overLimit = True

            game.groundMap[tileX][tileY] = 1
        
        game.currentBlock = None

        if overLimit:
            game.stateMachine.TransitionTo("Turning")
        else:
            game.stateMachine.TransitionTo("Default")
        
        
        return

        self.timer += game.delta

        if self.timer > 900:
            self.timer = 0
            game.currentBlock.color = Settings.currentBlockColor
            game.LockCurrentBlock()
            game.stateMachine.TransitionTo("Default")
        
        elif floor(self.timer / 150) % 2 == 0:
            game.currentBlock.color = (255, 255, 255)
        
        else:
            game.currentBlock.color = Settings.currentBlockColor
    
    def Draw(self):
        self.game.DrawWall(Settings.wallColor)
        self.game.DrawGround(Settings.groundColor)
        self.game.DrawLimitLine()
        img = Settings.font.render("state: locking", True, (0, 0, 0))
        pygame.screen.blit(img, (220, 300))
        
    def Exit(self):
        pass

class TurningState(DrawState):
    def __init__(self, game):
        self.game = game
        self.timer = 0

    def Enter(self):
        self.game.limitLineTimer = 0
    
    def Update(self):
        game = self.game
        self.timer += game.delta

        if self.timer > Settings.turnTime:
            self.timer = 0

            self.FlipGroundMap()
            
            game.stateMachine.TransitionTo("Default")
    
    def Draw(self):
        game = self.game

        changePercentage = self.timer / Settings.turnTime
        wallColor = utils.LerpColors(changePercentage, Settings.wallColor, Settings.groundColor)
        groundColor = utils.LerpColors(changePercentage, Settings.groundColor, Settings.wallColor)

        game.DrawWall(wallColor)

        for tileX in range(Settings.levelWidth):
            for tileY0 in range(Settings.limitHeight, Settings.levelHeight):
                if game.groundMap[tileX][tileY0] == 0:
                    continue
                
                x = tileX * Settings.tileSize + Settings.wallRect.left
                y0 = tileY0 * Settings.tileSize + Settings.wallRect.top
                y1 = (Settings.levelHeight - 1 - tileY0 + Settings.limitHeight) * Settings.tileSize + Settings.wallRect.top

                y = utils.Lerp(changePercentage, 1, y1, 0, y0)

                tileRect = pygame.Rect(x, y, Settings.tileSize, Settings.tileSize)
                pygame.draw.rect(pygame.screen, groundColor, tileRect)

        img = Settings.font.render("state: turning", True, (0, 0, 0))
        pygame.screen.blit(img, (220, 300))
        
    def FlipGroundMap(self):
        game = self.game
        '''
        for xRow in game.groundMap:
            for tileY0 in range(Settings.levelHeight):
                if tileY0 < Settings.limitHeight:
                    xRow[tileY0] = 0
                else:
                    tileY1 = Settings.levelHeight - 1 - tileY0 + Settings.limitHeight
                    #newValue = xRow[prevYOfNewValue]
                    xRow[tileY0] = 0 if xRow[tileY1] == 1 else 1'''
        
        newGroundMap = []

        for x in range(Settings.levelWidth):
            newXRow = []
            newGroundMap.append(newXRow)
            
            for tileY0 in range(Settings.levelHeight):
                if tileY0 < Settings.limitHeight:
                    newXRow.append(0)
                else:
                    tileY1 = Settings.levelHeight - 1 - tileY0 + Settings.limitHeight
                    #newValue = xRow[prevYOfNewValue]
                    newXRow.append(0 if game.groundMap[x][tileY1] == 1 else 1)
        
        game.groundMap = newGroundMap

    def Exit(self):
        pass

def TestWiggleGame():
    game = Game()
    game.groundMap[5][16] = 1
    game.groundMap[5][17] = 1
    game.groundMap[5][20] = 1
    game.groundMap[6][16] = 1
    game.groundMap[6][17] = 1
    game.groundMap[6][20] = 1
    return game


class Game:
    def __init__(self):
        self.Reset()
    
    def Reset(self):
        #self.groundMap = Settings.levelWidth * [Settings.levelHeight * [0]]
        self.groundMap = []

        for x in range(Settings.levelWidth):
            self.groundMap.append(Settings.levelHeight * [0])

        self.currentBlock = None
        self.inputController = InputController()
        self.limitLineTimer = 0

        self.stateMachine = StateMachine("Default", {
            "Default": DefaultState(self),
            "Locking": LockingState(self),
            "Turning": TurningState(self)
        })
        self.stateMachine.currentState.Enter()
    
    def HandleEvents(self):
        self.inputController.Update()
        self.input = self.inputController.GetInput()

        if self.inputController.IsPressed(pygame.K_r):
            self.Reset()

    def Update(self, delta):
        self.delta = delta
        self.stateMachine.Update()
    
    def Draw(self):
        pygame.screen.fill(Settings.backgroundColor)
        self.stateMachine.Draw()
        self.DrawCurrentBlock(pygame.screen)

    def DrawWall(self, color):
        levelWallRect = pygame.Rect(Settings.wallRect)
        levelWallRect.top += Settings.limitHeight * Settings.tileSize
        levelWallRect.height -= Settings.limitHeight * Settings.tileSize
        pygame.draw.rect(pygame.screen, Settings.wallColor, Settings.wallRect)
        pygame.draw.rect(pygame.screen, color, levelWallRect)

    def DrawGround(self, color):
        for tileX in range(Settings.levelWidth):
            for tileY in range(Settings.levelHeight):
                if self.groundMap[tileX][tileY] == 0:
                    continue
                
                x = tileX * Settings.tileSize + Settings.wallRect.left
                y = tileY * Settings.tileSize + Settings.wallRect.top
                tileRect = pygame.Rect(x, y, Settings.tileSize, Settings.tileSize)
                pygame.draw.rect(pygame.screen, color, tileRect)
    
    def DrawLimitLine(self):
        self.limitLineTimer += self.delta

        if self.limitLineTimer < 1000:
            c = self.limitLineTimer
        elif self.limitLineTimer < 2000:
            c = 1000 - (self.limitLineTimer - 1000)
        else:
            c = self.limitLineTimer = 0
        
        c = 255 / 1000 * c
        pygame.draw.rect(pygame.screen, (c, c, c), Settings.limitLineRect)
    
    def DrawCurrentBlock(self, screen):
        if self.currentBlock != None:
            self.currentBlock.Draw()
            y = 20

            for cornerPos in utils.GetCornerPositionsOfTile(self.currentBlock.position):
                txt = str(cornerPos)
                img = Settings.font.render(txt, True, (0, 0, 0))
                screen.blit(img, (220, y))
                y += 30
    
    def LockCurrentBlock(self):
        print("START LOCK")

        for tilePos in self.currentBlock.tilePositions:
            tileX = floor(self.currentBlock.position.x / Settings.tileSize + tilePos.x)
            tileY = floor(self.currentBlock.position.y / Settings.tileSize + tilePos.y)
            self.groundMap[tileX][tileY] = 1
            print("LOCK tilePos " + str(tilePos))
        
        self.currentBlock = None