import pygame
import os
import random
from tkinter import simpledialog, Tk

from database import ScoreSaver
from objects import Cactus, Dinosaur, Wazo


class Game:
    screen = None
    width = 1280
    height = 300
    frame_rate = 60

    ground_height = 270

    # Scrolling ground image
    ground = pygame.image.load(os.path.join('sprites', 'ground.png'))
    ground_w, ground_h = ground.get_size()

    def __init__(self):
        self.font50 = pygame.font.Font('8-BIT WONDER.ttf', 50)
        self.font30 = pygame.font.Font('8-BIT WONDER.ttf', 30)
        self.font20 = pygame.font.Font('8-BIT WONDER.ttf', 20)

        self.sound_death = pygame.mixer.Sound(os.path.join('sounds', 'death.wav'))
        self.sound_highscore = pygame.mixer.Sound(os.path.join('sounds', 'highscore.wav'))

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        self.dinosaur = Dinosaur(self, self.width/5, self.ground_height)

        Tk().wm_withdraw()
        self.player_name = simpledialog.askstring(
            title="Scores", prompt="Quel est votre pseudo ?")

        if(self.player_name == None):
            self.player_name = "unknown"

        self.scoreSaver = ScoreSaver()

        self.highscore = self.scoreSaver.get_player_highscore(self.player_name)

    def setup_start(self):
        self.cactusList = []
        self.wazoList = []

        self.spawnX = self.width+100

        self.ground_scroll = 0
        self.done = False

        self.scroll_speed = 10

        self.score = 0

    def draw_score(self):
        score_text = self.font30.render(
            "Score "+str(int(self.score)), False, (50, 50, 50))
        highscore_text = self.font20.render(
            "highscore "+str(self.highscore), False, (70, 70, 70))
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(highscore_text, (10, 40))

    def getLastObstacleX(self,minDistance):
        # Take x from last wazo if no cactus exist
        if len(self.cactusList) != 0 and len(self.wazoList) == 0:
            lastCactusX = self.cactusList[len(self.cactusList)-1].x
            return lastCactusX
        # Take x from last cactus if no wazo exist
        elif len(self.cactusList) == 0 and len(self.wazoList) != 0:
            lastWazoX =  self.wazoList[len(self.wazoList)-1].x
            return lastWazoX
        # Take the last cactus or wazo spawned
        elif len(self.cactusList) != 0 or len(self.wazoList) != 0:
            lastCactusX =  self.cactusList[len(self.cactusList)-1].x
            lastWazoX =  self.wazoList[len(self.wazoList)-1].x
            if lastCactusX > lastWazoX:
                return lastCactusX
            else:
                return lastWazoX
        else:
            return self.width-minDistance
    
    def isSpawningAllowed(self,minDistance,maxDistance):
        distance_between = abs(self.spawnX - self.getLastObstacleX(minDistance))
        return distance_between >= minDistance and distance_between <= maxDistance
    
    def updateObstacles(self,list):
        for obj in list:
            # Check for collision
            if self.dinosaur.checkCollision(obj.sprite):
                self.game_over()

            # update position
            obj.update(self.scroll_speed)
            if obj.x < -100:
                obj.kill()
                list.remove(obj)
            else:
                obj.draw()

    def drawGround(self):
        self.ground_scroll -= self.scroll_speed

        if self.ground_scroll < -self.ground_w:
            self.ground_scroll = 0

        self.screen.blit(self.ground,(self.ground_scroll,300-50))
        self.screen.blit(self.ground,(self.ground_scroll + self.ground_w,300-50))

    def generateObstacle(self):
        # Spawn new obstacle if the previous is not too close
        if self.isSpawningAllowed(300,1000):
            obstacleType = random.choice(["cactus","wazo"])

            if obstacleType == "cactus":
                # 1/10 of getting a new cactus spawned
                if random.randrange(10) == 1:
                    type = random.choice(["small","big"])
                    self.cactusList.append(Cactus(self,self.spawnX, self.ground_height,type))
            else:
                # 1/30 of getting a new wazo spawned
                if random.randrange(30) == 1:
                    self.wazoList.append(Wazo(self,self.spawnX, self.ground_height-65))

    def drawGameOverTexts(self):
        gameOverText = self.font50.render("GAME OVER", False, (0, 0, 0))
        retryText = self.font30.render("press enter to retry", False, (50, 50, 50))
        highscoreText = self.font20.render("New highscore", False, (255, 128, 0))

        gameOver_text_rect = gameOverText.get_rect(center=(self.width/2, (self.height/2)-50))
        retry_text_rect = retryText.get_rect(center=(self.width/2, self.height/2))
        highscore_text_rect = highscoreText.get_rect(center=(self.width/2, (self.height/2)+50))

        self.screen.blit(gameOverText, gameOver_text_rect)
        self.screen.blit(retryText, retry_text_rect)

        if(int(self.score) > self.highscore):
            self.screen.blit(highscoreText, highscore_text_rect)
            self.scoreSaver.save_player_highscore(self.player_name,int(self.score))
            self.highscore = int(self.score)
            self.sound_highscore.play()

    # Main game loop
    def play(self):
        self.setup_start()

        while not self.done:
            pressed = pygame.key.get_pressed()
            self.dinosaur.movements(pressed)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True

            # Generate next obstacles
            self.generateObstacle()
            
            # 60 FPS
            self.clock.tick(self.frame_rate)
            self.screen.fill((255, 255, 255)) # Clear screen

            # Draw scrolling ground
            self.drawGround()

            # Draw scrolling cactus
            self.updateObstacles(self.cactusList)
            self.updateObstacles(self.wazoList)

            # Draw dinosaur
            self.dinosaur.draw()

            # Increment score
            self.score += 1/self.frame_rate # 1sec = 1pt
            self.draw_score()

            # Increment scroll speed
            self.scroll_speed += 0.005

            pygame.display.update()
        
        # Game over loop
        while self.done:
            pygame.font.init()

            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_RETURN]:
                self.play()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = False

            self.clock.tick(self.frame_rate)

            self.drawGameOverTexts()

            pygame.display.update()

    def game_over(self):
        self.done = True
        self.scroll_speed = 0
        if(int(self.score) <= self.highscore):
            self.sound_death.play()
    
if __name__ == '__main__':
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
    pygame.init()

    programIcon = pygame.image.load(os.path.join('sprites', 'icon.png'))
    pygame.display.set_icon(programIcon)

    pygame.display.set_caption('TODG : Totally Original Dinosaur Game')

    game = Game()
    game.play()
