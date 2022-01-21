import pygame
import os
import time
#initialising pygame modules
import velocity as velocity
import random as r
pygame.font.init()


#predifened RBG colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
#Images
backgroundwidth = 1280
backgroundheight =720
BASIC_BACKGROUND_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets/Backgrounds','BasicRoad.png')),(backgroundwidth,backgroundheight))
MAIN_HERO_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets/mainHero','BaseMageImage.png')),(200,200))
FIREMAGE_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets/mainHero/RedMage','FireMage1.png')),(108,180))
FIREMAGE_STAFF_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets/mainHero/RedMage','FireMageStaff1.png')),(72,128))
BOB_CHARACTER_IMAGE = pygame.image.load(os.path.join('Assets', 'Bob_Character.png'))
JOHN_CHARACTER_IMAGE = pygame.image.load(os.path.join('Assets','John_Character.png'))
TEST_IMAGE = pygame.image.load(os.path.join('Assets','test.png'))
BACKGROUND = pygame.image.load(os.path.join('Assets','Background.png'))
EVILBAKER_CHARACTER_IMAGE = pygame.image.load(os.path.join('Assets','Evilbaker2_Character.png'))
EVILBAKER_CHARACTER_IMAGE = pygame.transform.scale(EVILBAKER_CHARACTER_IMAGE,(250,250))

HP_BAR_FULL = pygame.image.load(os.path.join('Assets','HP_Bar_Full.png'))
HP_BAR_80 = pygame.image.load(os.path.join('Assets','HP_BAR_80.png'))
HP_BAR_60 = pygame.image.load(os.path.join('Assets','HP_BAR_60.png'))
HP_BAR_40 = pygame.image.load(os.path.join('Assets','HP_BAR_40.png'))
HP_BAR_20 = pygame.image.load(os.path.join('Assets','HP_BAR_20.png'))
#Characters after scaling
#BOB_CHARACTER = pygame.transform.scale(BOB_CHARACTER_IMAGE, (150,150))
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)

#Attacks
EVILBAKER_BASIC_ATTACK_IMG1 = pygame.transform.scale(pygame.image.load(os.path.join('Assets/BaguetteAttack','Evilbaker2_BasicAttack1.png')),(250,250))
EVILBAKER_BASIC_ATTACK_IMG2 = pygame.transform.scale(pygame.image.load(os.path.join('Assets/BaguetteAttack','Evilbaker2_BasicAttack2.png')),(250,250))
EVILBAKER_BASIC_ATTACK_IMG3 = pygame.transform.scale(pygame.image.load(os.path.join('Assets/BaguetteAttack','Evilbaker2_BasicAttack3.png')),(250,250))
EVILBAKER_BASIC_ATTACK_IMG4 = pygame.transform.scale(pygame.image.load(os.path.join('Assets/BaguetteAttack','Evilbaker2_BasicAttack4.png')),(250,250))
EVILBAKER_BASIC_ATTACK_IMG5 = pygame.transform.scale(pygame.image.load(os.path.join('Assets/BaguetteAttack','Evilbaker2_BasicAttack5.png')),(250,250))
EVILBAKER_BASIC_ATTACK_IMG6 = pygame.transform.scale(pygame.image.load(os.path.join('Assets/BaguetteAttack','Evilbaker2_BasicAttack6.png')),(250,250))

MAINHERO_BASICRANGEATTACK = [
pygame.transform.scale(pygame.image.load(os.path.join('Assets/mainHero/BasicRangeAttack','BasicRangeAttack1.png')),(200,200)),
pygame.transform.scale(pygame.image.load(os.path.join('Assets/mainHero/BasicRangeAttack','BasicRangeAttack2.png')),(200,200)),
pygame.transform.scale(pygame.image.load(os.path.join('Assets/mainHero/BasicRangeAttack','BasicRangeAttack3.png')),(200,200)),
pygame.transform.scale(pygame.image.load(os.path.join('Assets/mainHero/BasicRangeAttack','BasicRangeAttack4.png')),(200,200)),
pygame.transform.scale(pygame.image.load(os.path.join('Assets/mainHero/BasicRangeAttack','BasicRangeAttack5.png')),(200,200)),
pygame.transform.scale(pygame.image.load(os.path.join('Assets/mainHero/BasicRangeAttack','BasicRangeAttack6.png')),(200,200)),
pygame.transform.scale(pygame.image.load(os.path.join('Assets/mainHero/BasicRangeAttack','BasicRangeAttack7.png')),(200,200)),
pygame.transform.scale(pygame.image.load(os.path.join('Assets/mainHero/BasicRangeAttack','BasicRangeAttack6.png')),(200,200)),
pygame.transform.scale(pygame.image.load(os.path.join('Assets/mainHero/BasicRangeAttack','BasicRangeAttack5.png')),(200,200)),
pygame.transform.scale(pygame.image.load(os.path.join('Assets/mainHero/BasicRangeAttack','BasicRangeAttack4.png')),(200,200)),
pygame.transform.scale(pygame.image.load(os.path.join('Assets/mainHero/BasicRangeAttack','BasicRangeAttack3.png')),(200,200)),
pygame.transform.scale(pygame.image.load(os.path.join('Assets/mainHero/BasicRangeAttack','BasicRangeAttack2.png')),(200,200)),
pygame.transform.scale(pygame.image.load(os.path.join('Assets/mainHero/BasicRangeAttack','BasicRangeAttack1.png')),(200, 200))

]
#Projectiles:
FROSTBALL = pygame.image.load(os.path.join('Assets/Projectiles/Frostball','Frostball1.png'))
FIREBALL = pygame.image.load(os.path.join('Assets/Projectiles/Fireball','Fireball1.png'))
EVILBAKER_BASIC_ATTACK_IMG_LIST = [
    pygame.image.load(os.path.join('Assets/BaguetteAttack','Evilbaker2_BasicAttack1.png'))
]

#todo: hpBarInTheCorner, new models for the character, new background image, refractor code into different files/modules

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

        enemy1 = Enemy(750,550,self.gameWindow)
        enemy2 = Enemy(850, 550, self.gameWindow)
        enemyGroup = pygame.sprite.Group()
        enemyGroup.add(enemy1)
        enemyGroup.add(enemy2)


        while run:
            clock.tick(self.tickRate)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            keysPressed = pygame.key.get_pressed()

            pygame.display.update()
            self.drawWindow()

            #MainHero handling part
            heroGroup.update()
            heroGroup.draw(self.gameWindow)

            self.handleHeroAttacks(hero1,keysPressed)


            #Enemy handling part
            enemyGroup.update()
            self.spawnSomeMobs(enemyGroup)
            enemyGroup.draw(self.gameWindow)



            #Projectile handling part
            heroProjGroup.update()
            heroProjGroup.draw(self.gameWindow)
            self.handleHeroProj(hero1,heroProjGroup)
            self.handleProjCollision(heroProjGroup,enemyGroup)


    def drawWindow(self):
        self.gameWindow.fill(WHITE)
        self.drawBackground()


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

    def handleProjCollision(self,projGroup,targetGroup):
        targetsHit = pygame.sprite.groupcollide(projGroup,targetGroup,False,False)
        for proj in targetsHit.keys():
            for tar in targetsHit.values():
                for i in tar:
                    i.currentHp -= proj.damage
                    proj.kill()

    def spawnSomeMobs(self,enemyGroup):
        if len(enemyGroup) <=2:
            for i in range(2):
                enemy = Enemy(850-r.randint(50,100), 550-r.randint(50,100), self.gameWindow)
                enemyGroup.add(enemy)


class MainHero(pygame.sprite.DirtySprite):
    def __init__(self, x,y,window, img = MAIN_HERO_IMAGE ):
        super().__init__()
        self.window = window
        #Hero related images and general info:
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]

        #Hero general attributes:
        self.maxHp = 100
        self.baseMovementSpeed = 6
        self.baseHpBarHeight = 10
        self.baseHpBarWidth = 50
        self.projectileSpawnCords = [0,0]
        self.hostile = False


        #Hero weapon related stuff:
        self.weaponXoffset = 66
        self.weaponYoffset = 56
        self.weaponImg = FIREMAGE_STAFF_IMAGE
        self.weaponGroup = pygame.sprite.Group()
        self.weapon = None
        self.spawnWeapon()

        #Hero projectile related stuff:
        self.projectileList = []
        self.projectileImg = FIREBALL
        #Hero active atributes:
        self.currentHp = self.maxHp
        self.movementSpeed = self.baseMovementSpeed
        self.visible = True
        self.gcd = False
        self.attackFrame = 0
        self.currentAttack = 0



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
       # sound = pygame.image.load(os.path.join('Assets','sound.mp4'))
        self.currentAttack = 1
        self.projectileSpawnCords = [self.rect.x+180, self.rect.y+50]
        projImage = self.projectileImg
        projImage = pygame.transform.scale(projImage,(32,32))
        t = None

        if self.attackFrame == 7:
            proj = Projectile(self.window, self.weapon.weaponProjectileSpawnCords[0], self.weapon.weaponProjectileSpawnCords[1], projImage)
            self.projectileList.append(proj)
            t = proj

        if self.attackFrame > len(MAINHERO_BASICRANGEATTACK)-1:
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

        if keysPressed[pygame.K_a]:
            self.rect.x -= self.movementSpeed
        if keysPressed[pygame.K_s]:
            self.rect.y += self.movementSpeed
        if keysPressed[pygame.K_w]:
            self.rect.y -= self.movementSpeed
        if keysPressed[pygame.K_d]:
            self.rect.x += self.movementSpeed

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

class Enemy(pygame.sprite.DirtySprite):
    def __init__(self, x,y,window ):
        super().__init__()
        self.window = window
        #Hero related images and general info:
        self.image = EVILBAKER_CHARACTER_IMAGE
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]

        #Hero general attributes:
        self.maxHp = 100
        self.baseMovementSpeed = 6
        self.baseHpBarHeight = 10
        self.baseHpBarWidth = 50
        self.projectileSpawnCords = [0,0]
        self.hostile = True

        #Hero active atributes:
        self.currentHp = self.maxHp
        self.movementSpeed = self.baseMovementSpeed
        self.visible = True
        self.gcd = False
        self.attackFrame = 0
        self.currentAttack = 0
        self.projectileList = []
        self.randomMovement = True

    def update(self):
        #self.rect.center = pygame.mouse.get_pos()
        #keysPressed = pygame.key.get_pressed()
        #self.handleHeroMovement(keysPressed)
        #self.handleHeroAttacks(keysPressed)
        self.drawHpBar()
        if self.currentHp == 0:
            self.kill()

        if self.randomMovement == True:
            self.randomMove()

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
    def __init__(self,window, x,y,image,velocity = 12):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

        self.velocity = velocity
        self.window = window
        self.damage = 10

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
    gameName = "ExileOfPath by CCCC"
    WIDTH = 1280
    HEIGHT = 720
    TICKRATE = 60
    game = Game(gameName, TICKRATE, WIDTH, HEIGHT)
    game.mainLoop()

if __name__ == '__main__':
    main()

