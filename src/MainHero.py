import pygame
import os
from Projectile import *
from Weapon import *

MAIN_HERO_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('./assets/mainHero', 'BaseMageImage.png')), (200, 200))
FIREMAGE_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('./assets/mainHero/RedMage', 'FireMage1.png')), (108, 180))
FIREMAGE_STAFF_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('./assets/mainHero/RedMage', 'FireMageStaff1.png')), (72, 128))


FROSTBALL = pygame.image.load(os.path.join('./assets/Projectiles/Frostball', 'Frostball1.png'))
FIREBALL = pygame.image.load(os.path.join('./assets/Projectiles/Fireball', 'Fireball1.png'))

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
        self.mapLevelLength = 0

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
        self.movementSpeed = self.baseMovementSpeed + 10
        self.visible = True
        self.gcd = False
        self.attackFrame = 0
        self.currentAttack = 0
        self.movingForward = False
        self.movingBackward = False


    def update(self):
        #print(self.xCord)
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
        sound = pygame.mixer.Sound(os.path.join('./assets/Sounds/AttackSounds/Fireball', 'FireballSound.wav'))
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