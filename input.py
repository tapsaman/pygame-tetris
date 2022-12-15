'''
class Button:
    def __init__(self, key):
        self.key = key
        self.pressed = False
        self.pressedFor = 0

class InputController:
    def __init__(self):
        self.x = 0
        self.y = 0
        
        self.btnUp = Button(pygame.K_UP)
        self.btnDown = Button(pygame.K_DOWN)
        self.btnRight = Button(pygame.K_RIGHT)
        self.btnLeft = Button(pygame.K_LEFT)

        self.buttons = (
            self.btnUp,
            self.btnDown,
            self.btnRight,
            self.btnLeft
        )
    
    def Update(self, delta):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()
            
            elif event.type == pygame.KEYDOWN:
                for button in self.buttons:
                    if event.key == button.key:
                        button.pressed = True
                        break
            
            elif event.type == pygame.KEYUP:
                for button in self.buttons:
                    if event.key == button.key:
                        button.pressed = False
                        break

                if event.key == pygame.K_UP:
                    input.y -= 1
                if event.key == pygame.K_RIGHT:
                    input.x += 1
                if event.key == pygame.K_DOWN:
                    input.y += 1
                if event.key == pygame.K_LEFT:
                    input.x -= 1
'''
import sys, pygame

class Input:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.rotate = 0
        self.confirm = False
        self.cancel = False

class InputController:
    def __init__(self):
        self.keyState = None
        self.previousKeyState = pygame.key.get_pressed()

    def Update(self):
        self.previousKeyState = self.keyState
        self.keyState = pygame.key.get_pressed()
    
    def IsPressed(self, key) -> bool:
        return self.keyState[key]

    def JustPressed(self, key) -> bool:
        return self.keyState[key] and self.previousKeyState[key] == False
    
    def GetInput(self) -> Input:
        input = Input()

        if self.IsPressed(pygame.K_DOWN):
            input.y += 1
        
        if self.JustPressed(pygame.K_UP) or self.JustPressed(pygame.K_x):
            input.rotate += 1
        
        if self.JustPressed(pygame.K_z):
            input.rotate -= 1
        
        if self.JustPressed(pygame.K_RIGHT):
            input.x += 1
        
        if self.JustPressed(pygame.K_LEFT):
            input.x -= 1
        
        if self.JustPressed(pygame.K_ESCAPE):
            sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        
        return input
