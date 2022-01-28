import pygame
import os
import random as r
#Enemies img
WATERDROPLET_IMG = pygame.image.load(os.path.join('./assets/Enemies/WaterDroplet', 'WaterDroplet.png'))
FLOATINGEMBER_IMG = pygame.image.load(os.path.join('./assets/Enemies/FloatingEmber', 'FloatingEmber.png'))


class Enemy(pygame.sprite.DirtySprite): #todo: create class for each enemy type - WaterDroplet and so on, that inherits from Enemy class
    def __init__(self, x,y,window,hero):
        super().__init__()
        self.window = window
        #Hero related images and general info:
        self.image = FLOATINGEMBER_IMG
        self.hero = hero
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.rect.center = [2000,150]
        self.xCord = self.rect.x
        self.yCord = self.rect.y


        #Enemy general attributes:
        self.maxHp = 100
        self.baseMovementSpeed = 6
        self.baseHpBarHeight = 10
        self.baseHpBarWidth = 50
        self.projectileSpawnCords = [0,0]
        self.hostile = True

        #Enemy active atributes:
        self.currentHp = self.maxHp
        self.movementSpeed = self.baseMovementSpeed
        self.visible = True
        self.gcd = False
        self.attackFrame = 0
        self.currentAttack = 0
        self.projectileList = []
        self.randomMovement = True

        #Enemy type:
        self.undead = False

    def update(self):
        self.drawHpBar()
        if self.currentHp <= 0 and not self.undead :
            print("dead")
            self.kill()

        if self.randomMovement == True:
            self.randomMove()

        if self.hero.movingBackward:
            self.rect.x += self.hero.movementSpeed
        if self.hero.movingForward:
            self.rect.x -= self.hero.movementSpeed

    def drawHpBar(self):
        pygame.draw.rect(self.window,(0,0,0),(self.rect.center[0]-(self.baseHpBarWidth/2)-1,self.rect.y-1,self.baseHpBarWidth+2,self.baseHpBarHeight+2), border_radius=0) #black border around hp bar
        pygame.draw.rect(self.window,(255,0,0),(self.rect.center[0]-(self.baseHpBarWidth/2),self.rect.y,self.baseHpBarWidth,self.baseHpBarHeight), border_radius=0) #red hp bar
        pygame.draw.rect(self.window,(0,167,0),(self.rect.center[0]-(self.baseHpBarWidth/2),self.rect.y,self.baseHpBarWidth*(self.currentHp/self.maxHp),10),border_radius = 0) #green hp bar

    def randomMove(self):
        rx = r.randint(0,2)
        ry = r.randint(0,2)

        if rx == 1:
            self.rect.x += 1
        elif rx ==2:
            self.rect.x -= 1
        if ry ==1:
            self.rect.y += 2
        elif ry==2:
            self.rect.y -= 2