import pygame
import os
from Projectile import *
from Weapon import *
from UserInterface import *
from Abilities import *

MAIN_HERO_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('./assets/mainHero', 'BaseMageImage.png')), (200, 200))
FIREMAGE_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('./assets/mainHero/RedMage', 'FireMage1.png')), (108, 180))
FIREMAGE_STAFF_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('./assets/mainHero/RedMage', 'FireMageStaff1.png')), (72, 128))


FROSTBALL = pygame.image.load(os.path.join('./assets/Projectiles/Frostball', 'Frostball1.png'))
FIREBALL = pygame.image.load(os.path.join('./assets/Projectiles/Fireball', 'Fireball1.png'))

class MainHero(pygame.sprite.DirtySprite):
    def __init__(self, x,y,window,game, img = MAIN_HERO_IMAGE ):
        super().__init__()
        self.game = game
        self.window = window
        self.events = []
        self.keysPressed = pygame.key.get_pressed()
        #Hero related images and general info:
        self.characterName = 'Combustador'
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

        #Hero UI:
        self.charSheetWindowGroup = pygame.sprite.Group()
        self.charSheetWindow = CharacterSheetWindow(self.window, self)
        self.charSheetWindowGroup.add(self.charSheetWindow)

        self.inventoryWindowGroup = pygame.sprite.Group()
        self.inventoryWindow = InventoryWindow(self.window, self)
        self.inventoryWindowGroup.add(self.inventoryWindow)

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

        #beams and projectiles
        self.beamList = []
        self.beamGroup = pygame.sprite.Group()

        self.projectileList = []
        self.projectileGroup = pygame.sprite.Group()

        #Hero active atributes:
        self.currentHp = self.maxHp - 70
        self.movementSpeed = self.baseMovementSpeed

        self.gcd = False #if set to False - hero is not attacking, True - hero is currently attacking
        self.attackFrame = 0
        self.currentAttack = 0
        self.movingForward = False
        self.movingBackward = False

        #Stat lists:
        self.baseStatList = [self.maxHp,self.baseMovementSpeed,self.baseSpellPower]

    def update(self):
        #print(self.xCord)
        #self.rect.center = pygame.mouse.get_pos()

        #keysPressed = pygame.key.get_pressed()
        #self.handleHeroMovement(keysPressed)
        self.handleKeyPresses()
        self.drawWeapon()
        #self.handleHeroAttacks(keysPressed)
        self.drawHpBar()
        self.drawProjectiles()



    def drawHpBar(self):
        pygame.draw.rect(self.window,(0,0,0),(self.rect.center[0]-(self.baseHpBarWidth/2)-1,self.rect.y-1,self.baseHpBarWidth+2,self.baseHpBarHeight+2), border_radius=0) #black border around hp bar
        pygame.draw.rect(self.window,(255,0,0),(self.rect.center[0]-(self.baseHpBarWidth/2),self.rect.y,self.baseHpBarWidth,self.baseHpBarHeight), border_radius=0) #red hp bar
        pygame.draw.rect(self.window,(0,167,0),(self.rect.center[0]-(self.baseHpBarWidth/2),self.rect.y,self.baseHpBarWidth*(self.currentHp/self.maxHp),10),border_radius = 0) #green hp bar

    def fireBeam(self):
        fBeam = FireBeam(self.window, self)
        self.currentAttack = 2 #id of a attack/ability
        if self.attackFrame > fBeam.attackFrames: # reseetting the value of attack frame it's higher than this spell's attackFrames, this could cause weird animations later on
            self.attackFrame = 0

        if self.attackFrame == fBeam.attackFrames:

            if len(self.beamGroup) == 0: #making sure that we have only one beam at the time
                self.beamList.append(fBeam)
                self.beamGroup.add(fBeam)
                self.gcd = True

            self.beamGroup.update() #updating the beam and drawing it
            self.beamGroup.draw(self.window)

        if self.attackFrame > fBeam.attackFrames-1: #keeping the staff at the same, tilted possition, is it necessary?
            self.gcd = False
            self.attackFrame = fBeam.attackFrames

        if self.attackFrame < fBeam.attackFrames: #rotating the staff till it's tilted in the positon we want it to be. 10/fBeam.attackFrames slows down the animation
            self.weapon.image = pygame.transform.rotate(self.weaponImg, -1 * self.attackFrame * 10/fBeam.attackFrames)  # part responsbile for rotating/moving the staff accordingly to the current frame of the attack
            x, y = self.weapon.rect.center
            self.weapon.rect = self.weapon.image.get_rect()
            self.weapon.rect.center = [x, y]
            self.attackFrame += 1

    def fireball(self):
        fireball = Fireball(self.window,self)
        self.currentAttack = 1
        if self.attackFrame > fireball.attackFrames:
            self.attackFrame = 0

        if self.attackFrame == fireball.attackFrames//2:
            self.projectileList.append(fireball)
            self.projectileGroup.add(fireball)
            self.gcd = True



        if self.attackFrame >= fireball.attackFrames:
            self.gcd = False
            self.attackFrame = 0
            self.currentAttack = 0

        self.weapon.image = pygame.transform.rotate(self.weaponImg,-1 * self.attackFrame)  # part responsbile for rotating/moving the staff accordingly to the current frame of the attack
        x, y = self.weapon.rect.center
        self.weapon.rect = self.weapon.image.get_rect()
        self.weapon.rect.center = [x, y]

        self.attackFrame += 1

    def basicRangeAttack(self): #todo: attacks as seperate class
        sound = pygame.mixer.Sound(os.path.join('./assets/Sounds/AttackSounds/Fireball', 'FireballSound.wav'))
        sound.set_volume(0.3)
        attackFrames = 15
        self.currentAttack = 1

        if self.attackFrame > attackFrames: # reseetting the value of attack frame it's higher than this spell's attackFrames, this could cause weird animations later on
            self.attackFrame = 0


        self.projectileSpawnCords = [self.rect.x+180, self.rect.y+50]
        projImage = self.projectileImg
        projImage = pygame.transform.scale(projImage,(32,32))


        # if self.attackFrame == 1:
        #     sound.play()

        if self.attackFrame == 7: #spawning projectile at 7th frame of the attack - when staff is in the right position
            proj = Projectile(self.window, self.weapon.weaponProjectileSpawnCords[0], self.weapon.weaponProjectileSpawnCords[1], projImage, self)
            self.projectileList.append(proj)

        if self.attackFrame > attackFrames-1: #resetting back to frame 0 - so that the staff position goes back to default position
            self.attackFrame = 0
            self.currentAttack = 0
            self.gcd = False


        self.weapon.image = pygame.transform.rotate(self.weaponImg, -1*self.attackFrame) #part responsbile for rotating/moving the staff accordingly to the current frame of the attack
        x,y = self.weapon.rect.center
        self.weapon.rect = self.weapon.image.get_rect()
        self.weapon.rect.center = [x,y]
        self.attackFrame += 1

    def handleKeyPresses(self):
        keysPressed = pygame.key.get_pressed()

        self.handleHeroMovement(keysPressed)
        self.handleUIKeybinds(keysPressed)
        self.handleAbilities(keysPressed)

    def resetWeaponAnimation(self):
        self.attackFrame = 0
        self.weapon.image = pygame.transform.rotate(self.weaponImg, -1 * self.attackFrame)
        self.beamGroup.empty()

    def handleUIKeybinds(self,keysPressed):

        for event in self.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.charSheetWindow.isOpen = False
                    self.inventoryWindow.isOpen = False

                if event.key == pygame.K_c:
                    if self.charSheetWindow.isOpen == False:
                        self.charSheetWindow.isOpen = True
                    elif self.charSheetWindow.isOpen == True:
                        self.charSheetWindow.isOpen = False
                if event.key == pygame.K_i:
                    if self.inventoryWindow.isOpen ==False:
                        self.inventoryWindow.isOpen = True
                    elif self.inventoryWindow.isOpen ==True:
                        self.inventoryWindow.isOpen = False

        if self.charSheetWindow.isOpen:
            self.charSheetWindowGroup.update()
            self.charSheetWindowGroup.draw(self.window)

        if self.inventoryWindow.isOpen:
            self.inventoryWindowGroup.update()
            self.inventoryWindowGroup.draw(self.window)


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

    def handleAbilities(self,keysPressed):
        if self.gcd == False:
            if keysPressed[pygame.K_x]:
                #self.resetWeaponAnimation()
                #self.basicRangeAttack()
                self.fireball()
                self.gcd = True

            elif keysPressed[pygame.K_z]:
                self.fireBeam()
                self.gcd = True
            else:
                self.resetWeaponAnimation()

        if self.gcd == True:
            if self.currentAttack == 1:
                #self.basicRangeAttack()
                self.fireball()
            elif self.currentAttack == 2:
                self.fireBeam()

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

    def drawProjectiles(self):
        self.projectileGroup.update()
        self.projectileGroup.draw(self.window)
