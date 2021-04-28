import pygame
import os
from sprites import CactusSprite, DinosaurSpriteDown, DinosaurSpriteRun, WazoSprite

class Dinosaur():
    isJump = False
    maxJumpHeight = 10
    jumpCount = maxJumpHeight
    vel = 8

    

    dino_state = "up"

    # Sprite animations
    run_sprite = DinosaurSpriteRun()
    run_group = pygame.sprite.Group(run_sprite)
    down_sprite = DinosaurSpriteDown()
    down_group = pygame.sprite.Group(down_sprite)

    sprite = run_sprite
    sprite_group = run_group

    def __init__(self,game,x,y):
        self.x = x
        self.y = y
        self.game = game

        self.sound_jump = pygame.mixer.Sound(os.path.join('sounds', 'jump.wav'))
    
    def movements(self,keys):
        self.dino_state = "up"
        if not(self.isJump):
            if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
                self.isJump = True
                self.dino_state = "up"
                self.sound_jump.play()
            elif keys[pygame.K_DOWN]:
                self.dino_state = "down"
        else:
            if self.jumpCount >= -self.maxJumpHeight:
                self.y -= (self.jumpCount * abs(self.jumpCount)) * 0.5
                self.jumpCount -= 1
            else:
                self.jumpCount = self.maxJumpHeight
                self.isJump = False
            
    
    def checkCollision(self,sprite):
        return pygame.sprite.collide_mask(self.sprite,sprite) != None

    def draw(self):
        if self.dino_state == "down":
            self.sprite = self.down_sprite
            self.sprite_group = self.down_group
        else:
            self.sprite = self.run_sprite
            self.sprite_group = self.run_group

        self.sprite.update(self.x,self.y)
        self.sprite_group.draw(self.game.screen)

class Cactus():
    def __init__(self,game,x,y,type):
        self.x = x
        self.y = y
        self.game = game

        self.sprite = CactusSprite(type)
        self.group = pygame.sprite.Group(self.sprite)
    
    def draw(self):
        self.group.update(self.x,self.y)
        self.group.draw(self.game.screen)
    
    def update(self,scroll_speed):
        self.x -= scroll_speed
    
    def kill(self):
        self.sprite.kill()

class Wazo():
    def __init__(self,game,x,y):
        self.x = x
        self.y = y
        self.game = game

        self.sprite = WazoSprite()
        self.group = pygame.sprite.Group(self.sprite)
    
    def draw(self):
        self.group.update(self.x,self.y)
        self.group.draw(self.game.screen)
    
    def update(self,scroll_speed):
        self.x -= scroll_speed
    
    def kill(self):
        self.sprite.kill()