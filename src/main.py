import pygame
import os
import time
#initialising pygame modules
import random as r
from Background import *
from Enemies import *
from UserInterface import *
from MainHero import *
from MapLevel import *
from Projectile import *
from Weapon import *
from GameEvents import *
#pygame inits
pygame.font.init()
pygame.mixer.init()

#predifened RBG colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
#Images
backgroundwidth = 1280
backgroundheight =720
BASIC_BACKGROUND_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('./assets/Backgrounds', 'BasicRoad.png')), (backgroundwidth, backgroundheight))
SCROLLING_BACKGROUND_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('./assets/Backgrounds', 'ScollingBackgroundTest1.png')), (backgroundwidth, backgroundheight))
MAIN_HERO_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('./assets/mainHero', 'BaseMageImage.png')), (200, 200))
FIREMAGE_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('./assets/mainHero/RedMage', 'FireMage1.png')), (108, 180))
FIREMAGE_STAFF_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('./assets/mainHero/RedMage', 'FireMageStaff1.png')), (72, 128))



#Enemies img
WATERDROPLET_IMG = pygame.image.load(os.path.join('./assets/Enemies/WaterDroplet', 'WaterDroplet.png'))





HP_BAR = pygame.image.load(os.path.join('./assets/HpBar', 'HpBar.png'))
#Characters after scaling

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)



#Projectiles:


#todo: hpBarInTheCorner, new models for the character, new background image, refractor code into different files/modules, xpbar, manabar

class Game(object):
    def __init__(self, gameName, tickRate,width, height):
        self.gameName = gameName
        self.tickRate = tickRate
        self.width = width
        self.height = height
        self.gameWindow = self.getGameWindow()
        self.characterList = []
        self.characterCount = 0
        self.enemyList = []
        self.enemyCount = 0
        self.healthFont = pygame.font.SysFont('verdana', 14)


    def drawBackground(self, stage=0):
        if stage == 0:
            self.gameWindow.blit(BASIC_BACKGROUND_IMAGE,(0,0))

    def getGameWindow(self):
        window = pygame.display.set_mode((self.width, self.height))  # window
        pygame.display.set_caption(self.gameName)

        return window

    def mainLoop(self):
        run = True
        clock = pygame.time.Clock()

        hero1 = MainHero(50, 550, self.gameWindow,FIREMAGE_IMAGE)

        heroGroup = pygame.sprite.Group()
        heroGroup.add(hero1)
        heroProjGroup = pygame.sprite.Group()

        enemy1 = Enemy(750,550,self.gameWindow,hero1)
        enemy2 = Enemy(850, 550, self.gameWindow,hero1)
        enemyGroup = pygame.sprite.Group()
        enemyGroup.add(enemy1)
        enemyGroup.add(enemy2)

        hpbar1 = HpBar(hero1, self.gameWindow)
        hpBarGroup = pygame.sprite.Group()
        hpBarGroup.add(hpbar1)

        level1 = MapLevel(1,1,5,SCROLLING_BACKGROUND_IMAGE,self.gameWindow,hero1)


        while run:
            clock.tick(self.tickRate)
            hero1.events = []
            #hero1.events = pygame.event.get()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                else:
                    hero1.events.append(event)

            #print(hero1.xCord,hero1.rect.x)
            pygame.display.update()
            #Background

            self.drawWindow()
            self.drawLevel(level1)


            #MainHero handling part
            heroGroup.update()
            heroGroup.draw(self.gameWindow)

            #self.handleHeroAttacks(hero1,keysPressed) #todo: move it to abilities/different class


            #Enemy handling part
            enemyGroup.update()
            self.spawnSomeMobs(enemyGroup,hero1)
            enemyGroup.draw(self.gameWindow)

            #HP bar in the corner handling part
            hpBarGroup.update()
            hpBarGroup.draw(self.gameWindow)

            #Projectile handling part
            # heroProjGroup.update()
            # heroProjGroup.draw(self.gameWindow)

            #self.handleHeroProj(hero1,heroProjGroup) #todo: move it somewhere else

            self.handleCollisions(hero1,enemyGroup)


    def drawWindow(self):
        self.gameWindow.fill(WHITE)
        #self.drawBackground()

    def drawLevel(self,level): #todo: move it somewhere else
        for i in level.backgroundList:
            self.gameWindow.blit(i.image,(i.rect.x,i.rect.y))
        level.moveAllBackgrounds()

    # def handleHeroProj(self,hero,heroProjGroup): #todo: move it somewhere else
    #     for i in hero.projectileList:
    #         if i not in heroProjGroup:
    #             heroProjGroup.add(i)


    # def handleProjCollision(self,projGroup,targetGroup,hero): #todo: move it somwhere else
    #     targetsHit = pygame.sprite.groupcollide(projGroup,targetGroup,False,False)
    #     for proj in targetsHit.keys():
    #         for tar in targetsHit.values():
    #             for i in tar:
    #                 i.currentHp -= (proj.damage * 0.3*hero.currentSpellPower)
    #                 if proj.lifeSteal and hero.currentHp < hero.maxHp:
    #                     hero.currentHp += (proj.damage * hero.currentSpellPower)*hero.lifeStealPower
    #                 proj.kill()

    def handleCollisions(self, hero, targetGroup):
        beamGroup = hero.beamGroup
        projGroup = hero.projectileGroup

        BeamCollision.checkBeamCollision(beamGroup, targetGroup)
        ProjectileCollision.checkProjCollision(projGroup,targetGroup)

    def spawnSomeMobs(self,enemyGroup,hero): #todo: move it somwhere else
        if len(enemyGroup) <=2:
            for i in range(2):
                enemy = Enemy(850-r.randint(50,100), 550-r.randint(50,100), self.gameWindow,hero)
                enemyGroup.add(enemy)


def main():
    gameName = "Entity Unknown by CCCC"
    WIDTH = 1280
    HEIGHT = 720
    TICKRATE = 60
    game = Game(gameName, TICKRATE, WIDTH, HEIGHT)
    game.mainLoop()

if __name__ == '__main__':
    main()

