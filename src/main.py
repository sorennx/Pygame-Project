import pygame
import os
import time
#initialising pygame modules
import random as r
from Background import *
from Enemy import *
from HpBar import *
from MainHero import *
from MapLevel import *
from Projectile import *
from Weapon import *

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
BOB_CHARACTER_IMAGE = pygame.image.load(os.path.join('./assets', 'Bob_Character.png'))
JOHN_CHARACTER_IMAGE = pygame.image.load(os.path.join('./assets', 'John_Character.png'))
TEST_IMAGE = pygame.image.load(os.path.join('./assets', 'test.png'))
BACKGROUND = pygame.image.load(os.path.join('./assets', 'Background.png'))
EVILBAKER_CHARACTER_IMAGE = pygame.image.load(os.path.join('./assets', 'Evilbaker2_Character.png'))
EVILBAKER_CHARACTER_IMAGE = pygame.transform.scale(EVILBAKER_CHARACTER_IMAGE,(250,250))

#Enemies img
WATERDROPLET_IMG = pygame.image.load(os.path.join('./assets/Enemies/WaterDroplet', 'WaterDroplet.png'))
FLOATINGEMBER_IMG = pygame.image.load(os.path.join('./assets/Enemies/FloatingEmber', 'FloatingEmber.png'))




HP_BAR = pygame.image.load(os.path.join('./assets/HpBar', 'HpBar.png'))
#Characters after scaling

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)



#Projectiles:
FROSTBALL = pygame.image.load(os.path.join('./assets/Projectiles/Frostball', 'Frostball1.png'))
FIREBALL = pygame.image.load(os.path.join('./assets/Projectiles/Fireball', 'Fireball1.png'))

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

        #bg3 = Background(SCROLLING_BACKGROUND_IMAGE,self.gameWindow,hero1,'left')
        # bg1 = Background(SCROLLING_BACKGROUND_IMAGE, self.gameWindow, hero1)
        # bg2 = Background(SCROLLING_BACKGROUND_IMAGE, self.gameWindow, hero1)
        level1 = MapLevel(1,1,5,SCROLLING_BACKGROUND_IMAGE,self.gameWindow,hero1)
        print(level1.backgroundList)


        #bg3.rect.x -= bg1.image.get_width()
        # bg2.rect.x = bg1.image.get_width()
        # backgroundGroup = pygame.sprite.Group()
        # backgroundGroup.add(bg1)
        # backgroundGroup.add(bg2)
        #backgroundGroup.add(bg3)

        while run:
            clock.tick(self.tickRate)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            keysPressed = pygame.key.get_pressed()

            #print(hero1.xCord,hero1.rect.x)
            pygame.display.update()
            #Background

            self.drawWindow()
            self.drawLevel(level1)


            #MainHero handling part
            heroGroup.update()
            heroGroup.draw(self.gameWindow)

            self.handleHeroAttacks(hero1,keysPressed)


            #Enemy handling part
            enemyGroup.update()
            self.spawnSomeMobs(enemyGroup,hero1)
            enemyGroup.draw(self.gameWindow)

            #HP bar in the corner handling part
            hpBarGroup.update()
            hpBarGroup.draw(self.gameWindow)

            #Projectile handling part
            heroProjGroup.update()
            heroProjGroup.draw(self.gameWindow)
            self.handleHeroProj(hero1,heroProjGroup)
            self.handleProjCollision(heroProjGroup,enemyGroup,hero1)


    def drawWindow(self):
        self.gameWindow.fill(WHITE)
        #self.drawBackground()

    def drawLevel(self,level):
        for i in level.backgroundList:
            self.gameWindow.blit(i.image,(i.rect.x,i.rect.y))
        level.moveAllBackgrounds()

    def handleHeroProj(self,hero,heroProjGroup):
        for i in hero.projectileList:
            if i not in heroProjGroup:
                heroProjGroup.add(i)
        #print(heroProjGroup)

    def handleHeroAttacks(self,hero,keysPressed):
        if keysPressed[pygame.K_SPACE]:  # Is there a way to move it to the MainHero class ?
            if hero.gcd == False:
                hero.basicRangeAttack()
                hero.gcd = True

        if hero.gcd == True:
            if hero.currentAttack == 1:
                hero.basicRangeAttack()

    def handleProjCollision(self,projGroup,targetGroup,hero):
        targetsHit = pygame.sprite.groupcollide(projGroup,targetGroup,False,False)
        for proj in targetsHit.keys():
            for tar in targetsHit.values():
                for i in tar:
                    i.currentHp -= (proj.damage * 0.3*hero.currentSpellPower)
                    if proj.lifeSteal and hero.currentHp < hero.maxHp:
                        hero.currentHp += (proj.damage * hero.currentSpellPower)*hero.lifeStealPower
                    proj.kill()

    def spawnSomeMobs(self,enemyGroup,hero):
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

