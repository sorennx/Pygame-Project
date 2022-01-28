import pygame
import os
import time
#initialising pygame modules
import random as r

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
BASIC_BACKGROUND_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets/Backgrounds','BasicRoad.png')),(backgroundwidth,backgroundheight))
SCROLLING_BACKGROUND_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets/Backgrounds','ScollingBackgroundTest1.png')),(backgroundwidth,backgroundheight))
MAIN_HERO_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets/mainHero','BaseMageImage.png')),(200,200))
FIREMAGE_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets/mainHero/RedMage','FireMage1.png')),(108,180))
FIREMAGE_STAFF_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets/mainHero/RedMage','FireMageStaff1.png')),(72,128))
BOB_CHARACTER_IMAGE = pygame.image.load(os.path.join('Assets', 'Bob_Character.png'))
JOHN_CHARACTER_IMAGE = pygame.image.load(os.path.join('Assets','John_Character.png'))
TEST_IMAGE = pygame.image.load(os.path.join('Assets','test.png'))
BACKGROUND = pygame.image.load(os.path.join('Assets','Background.png'))
EVILBAKER_CHARACTER_IMAGE = pygame.image.load(os.path.join('Assets','Evilbaker2_Character.png'))
EVILBAKER_CHARACTER_IMAGE = pygame.transform.scale(EVILBAKER_CHARACTER_IMAGE,(250,250))

#Enemies img
WATERDROPLET_IMG = pygame.image.load(os.path.join('Assets/Enemies/WaterDroplet','WaterDroplet.png'))
FLOATINGEMBER_IMG = pygame.image.load(os.path.join('Assets/Enemies/FloatingEmber','FloatingEmber.png'))


HP_BAR_FULL = pygame.image.load(os.path.join('Assets','HP_Bar_Full.png'))
HP_BAR_80 = pygame.image.load(os.path.join('Assets','HP_BAR_80.png'))
HP_BAR_60 = pygame.image.load(os.path.join('Assets','HP_BAR_60.png'))
HP_BAR_40 = pygame.image.load(os.path.join('Assets','HP_BAR_40.png'))
HP_BAR_20 = pygame.image.load(os.path.join('Assets','HP_BAR_20.png'))

HP_BAR = pygame.image.load(os.path.join('Assets/HpBar','HpBar.png'))
#Characters after scaling

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)



#Projectiles:
FROSTBALL = pygame.image.load(os.path.join('Assets/Projectiles/Frostball','Frostball1.png'))
FIREBALL = pygame.image.load(os.path.join('Assets/Projectiles/Fireball','Fireball1.png'))
EVILBAKER_BASIC_ATTACK_IMG_LIST = [
    pygame.image.load(os.path.join('Assets/BaguetteAttack','Evilbaker2_BasicAttack1.png'))
]

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


class Background(pygame.sprite.DirtySprite): #todo: spawn multiple backgrounds for each level instead of rendering them in the present
    def __init__(self,img,window,hero,pos = 'right'):
        super().__init__()
        self.image = img
        self.window = window
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.hero = hero
        self.pos = pos


    def update(self): #Todo: add rolling background class that handles adding backgrounds based on char position
        #
        # if self.rect.x < self.image.get_width() * -1 and self.pos == 'right':
        #     self.rect.x = self.image.get_width()-7
        #
        # if self.pos == 'left' and self.hero.rect.x > self.image.get_width(): #todo: fix this
        #     self.rect.x -= self.image.get_width()
        #
        # if self.hero.movingForward is True:
        #     self.rect.x -= self.hero.movementSpeed
        #
        #
        # if self.hero.movingBackward is True:
        #     self.rect.x += self.hero.movementSpeed
        pass




class MapLevel:
    def __init__(self,areaLevel,enemyLevel,length,backgroundImg,window,hero):
        self.areaLevel = areaLevel
        self.enemyLevel = enemyLevel
        self.levelLength = length
        self.backgroundImg = backgroundImg
        self.window = window
        self.hero = hero
        self.backgroundList = []

        self.createLevel()

    def createLevel(self):

        for i in range(self.levelLength):
            t = Background(self.backgroundImg,self.window,self.hero)
            t.rect.x = t.image.get_width()*i
            self.backgroundList.append(t)

    def moveAllBackgrounds(self):
        for i in range(len(self.backgroundList)):
            if self.hero.movingForward:
                self.backgroundList[i].rect.x -= self.hero.movementSpeed
            if self.hero.movingBackward:
                self.backgroundList[i].rect.x += self.hero.movementSpeed


class MainHero(pygame.sprite.DirtySprite):
    def __init__(self, x,y,window, img = MAIN_HERO_IMAGE ):
        super().__init__()
        self.window = window
        #Hero related images and general info:

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.xCord = self.rect.x
        self.yCord = y
        #Hero general attributes:
        self.maxHp = 100
        self.baseMovementSpeed = 6
        self.baseHpBarHeight = 10
        self.baseHpBarWidth = 50
        self.projectileSpawnCords = [0,0]
        self.hostile = False
        self.baseSpellPower = 1


        #Hero weapon related stuff:
        self.weaponXoffset = 66
        self.weaponYoffset = 56
        self.weaponImg = FIREMAGE_STAFF_IMAGE
        self.weaponGroup = pygame.sprite.Group()
        self.weapon = None
        self.spawnWeapon()

        #Combat stats
        self.lifeSteal = True
        self.lifeStealPower = 0.1
        self.currentSpellPower = self.baseSpellPower + 3


        #Hero projectile related stuff:
        self.projectileList = []
        self.projectileImg = FIREBALL

        #Hero active atributes:
        self.currentHp = self.maxHp -69
        self.movementSpeed = self.baseMovementSpeed
        self.visible = True
        self.gcd = False
        self.attackFrame = 0
        self.currentAttack = 0
        self.movingForward = False
        self.movingBackward = False


    def update(self):
        #self.rect.center = pygame.mouse.get_pos()
        keysPressed = pygame.key.get_pressed()
        self.handleHeroMovement(keysPressed)
        self.drawWeapon()
        #self.handleHeroAttacks(keysPressed)
        self.drawHpBar()


    def drawHpBar(self):
        pygame.draw.rect(self.window,(0,0,0),(self.rect.center[0]-(self.baseHpBarWidth/2)-1,self.rect.y-1,self.baseHpBarWidth+2,self.baseHpBarHeight+2), border_radius=0) #black border around hp bar
        pygame.draw.rect(self.window,(255,0,0),(self.rect.center[0]-(self.baseHpBarWidth/2),self.rect.y,self.baseHpBarWidth,self.baseHpBarHeight), border_radius=0) #red hp bar
        pygame.draw.rect(self.window,(0,167,0),(self.rect.center[0]-(self.baseHpBarWidth/2),self.rect.y,self.baseHpBarWidth*(self.currentHp/self.maxHp),10),border_radius = 0) #green hp bar

    def basicRangeAttack(self): #todo: attacks as seperate class
        sound = pygame.mixer.Sound(os.path.join('Assets/Sounds/AttackSounds/Fireball','FireballSound.wav'))
        sound.set_volume(0.3)
        attackFrames = 15

        self.currentAttack = 1
        self.projectileSpawnCords = [self.rect.x+180, self.rect.y+50]
        projImage = self.projectileImg
        projImage = pygame.transform.scale(projImage,(32,32))
        t = None
        # if self.attackFrame == 1:
        #     sound.play()
        #
        if self.attackFrame == 7:
            proj = Projectile(self.window, self.weapon.weaponProjectileSpawnCords[0], self.weapon.weaponProjectileSpawnCords[1], projImage, self)
            self.projectileList.append(proj)
            t = proj

        if self.attackFrame > attackFrames-1:
            self.attackFrame = 0
            self.currentAttack = 0
            if t in self.projectileList:
                self.projectileList.remove(t)
            self.gcd = False
            if len(self.projectileList)>0:
                del self.projectileList[0]

        tx = self.rect
        #self.image = MAINHERO_BASICRANGEATTACK[self.attackFrame]
        self.weapon.image = pygame.transform.rotate(self.weaponImg, -1*self.attackFrame)
        x,y = self.weapon.rect.center
        self.weapon.rect = self.weapon.image.get_rect()
        self.weapon.rect.center = [x,y]

        self.attackFrame += 1


    def handleHeroMovement(self,keysPressed):
        self.movingForward = False
        self.movingBackward = False

        if keysPressed[pygame.K_a]:
            if self.xCord - self.movementSpeed <0:
                self.movingBackward = False
            else:
                self.movingBackward = True
                if self.rect.x - self.movementSpeed <0:
                    self.xCord -= self.movementSpeed
                else:
                    self.rect.x -= self.movementSpeed
                    self.xCord -= self.movementSpeed


        if keysPressed[pygame.K_s]:
            self.rect.y += self.movementSpeed
            self.moving = True

        if keysPressed[pygame.K_w]:
            self.rect.y -= self.movementSpeed

        if keysPressed[pygame.K_d]:
            if self.rect.x + self.movementSpeed < 1280/1.5:

                self.rect.x += self.movementSpeed
            self.xCord += self.movementSpeed
            self.movingForward = True

    def spawnWeapon(self):
        wep = Weapon(self.rect.x+72,self.rect.y+56,self.window,self.weaponImg,'Staff')
        self.weapon = wep
        self.weaponGroup.add(wep)

    def drawWeapon(self):
        self.weaponGroup.update() #Order of updating and THEN drawing matters a lot!

        for i in self.weaponGroup.sprites():
            i.rect.x = self.rect.x+self.weaponXoffset
            i.rect.y = self.rect.y+self.weaponYoffset
        self.weaponGroup.draw(self.window)

class HpBar(pygame.sprite.DirtySprite):
    def __init__(self,hero,window):
        super().__init__()
        self.window = window
        self.hero = hero
        self.image = HP_BAR
        self.rect = self.image.get_rect()
        self.rect.y = 720-50
        self.rect.x = 0


    def update(self):
        pygame.draw.rect(self.window, (0, 0, 0), (self.rect.x+1, self.rect.y-1, 50, 50))
        pygame.draw.rect(self.window, (180, 0, 0), (self.rect.x, self.rect.y+(50 - 50* self.hero.currentHp/self.hero.maxHp), 50,  50* self.hero.currentHp/self.hero.maxHp))


class Enemy(pygame.sprite.DirtySprite): #todo: create class for each enemy type - WaterDroplet and so on, that inherits from Enemy class
    def __init__(self, x,y,window,hero):
        super().__init__()
        self.window = window
        #Hero related images and general info:
        self.image = FLOATINGEMBER_IMG
        self.hero = hero
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.rect.center = [1300,150]
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


class Projectile(pygame.sprite.DirtySprite):
    def __init__(self,window, x,y,image,hero, velocity = 12):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

        self.velocity = velocity
        self.window = window
        self.damage = 10
        self.hero = hero


        if self.hero.lifeSteal == True:
            self.lifeSteal = True




    def update(self):
        if self.rect.x < backgroundwidth:
            self.rect.x += self.velocity
        else:
            self.kill()


class Weapon(pygame.sprite.DirtySprite):
    def __init__(self,x,y,window, img,weaponType):
        super().__init__()
        self.window = window

        # Weapon related images and general info:
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.weaponType = weaponType
        self.weaponProjectileSpawnCords = [self.rect.x+72,self.rect.y+10]

    def update(self):
        self.weaponProjectileSpawnCords[0],self.weaponProjectileSpawnCords[1] = self.rect.x+72, self.rect.y+10



def main():
    gameName = "Entity Unknown by CCCC"
    WIDTH = 1280
    HEIGHT = 720
    TICKRATE = 60
    game = Game(gameName, TICKRATE, WIDTH, HEIGHT)
    game.mainLoop()

if __name__ == '__main__':
    main()

