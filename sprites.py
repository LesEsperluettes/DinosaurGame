import pygame

class DinosaurSpriteRun(pygame.sprite.Sprite):
    def __init__(self):
        super(DinosaurSpriteRun,self).__init__()
        self.images = []
        self.images.append(pygame.image.load('./sprites/dino2.png'))
        self.images.append(pygame.image.load('./sprites/dino3.png'))

        self.framesBySprite = 5
        self.frameCounter = 0

        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(0,0,88,94)

    def update(self,x,y):
        self.rect.x = x
        self.rect.bottom = y

        if self.frameCounter >= self.framesBySprite:
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index]
            self.frameCounter = 0
        else:
            self.frameCounter += 1

class DinosaurSpriteDown(pygame.sprite.Sprite):
    def __init__(self):
        super(DinosaurSpriteDown,self).__init__()
        self.images = []
        self.images.append(pygame.image.load('./sprites/dino_down_0.png'))
        self.images.append(pygame.image.load('./sprites/dino_down_1.png'))

        self.framesBySprite = 5
        self.frameCounter = 0

        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(0,0,117,60)

    def update(self,x,y):
        self.rect.x = x
        self.rect.bottom = y

        if self.frameCounter >= self.framesBySprite:
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index]
            self.frameCounter = 0
        else:
            self.frameCounter += 1

class CactusSprite(pygame.sprite.Sprite):
    def __init__(self,type):
        super(CactusSprite,self).__init__()

        if type == "small":
            self.image = pygame.image.load('./sprites/cactus_small_0.png')
            self.size = (34,70)
        else:
            self.image = pygame.image.load('./sprites/cactus_big_0.png')
            self.size = (50,94)

        self.rect = pygame.Rect(0,0,self.size[0],self.size[1])
    
    def update(self,x,y):
        self.rect.x = x
        self.rect.bottom = y

class WazoSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(WazoSprite,self).__init__()
        self.images = []
        self.images.append(pygame.image.load('./sprites/wazo0.png'))
        self.images.append(pygame.image.load('./sprites/wazo1.png'))

        self.framesBySprite = 5
        self.frameCounter = 0

        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(0,0,92,68)

    def update(self,x,y):
        self.rect.x = x
        self.rect.bottom = y

        if self.frameCounter >= self.framesBySprite:
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index]
            self.frameCounter = 0
        else:
            self.frameCounter += 1