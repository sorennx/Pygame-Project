from Projectile import *
import pygame
import os

#damage = addedDamage + (baseDamage + (modifier * hero.spellpower))

class Beam(pygame.sprite.Sprite):
    def __init__(self, window, hero):
        super().__init__()
        self.window = window
        self.hero = hero

    def update(self):
        pass

class FireBeam(Beam):
    def __init__(self, window, hero):
        super().__init__(window, hero)
        self.window = window
        self.hero = hero
        self.image = pygame.image.load(os.path.join('./assets/Spells/FireBeam','FireBeam.png'))
        self.rect = self.image.get_rect()
        self.rect.x = self.hero.weaponXoffset + self.hero.rect.x
        self.rect.y = self.hero.weaponYoffset + self.hero.rect.y
        self.attackFrames = 60 #the frames/time attack takes to cast
        self.baseDamage = 5
        self.damage = self.baseDamage + (0.1 * self.hero.baseSpellPower)

    def update(self):
        self.rect.x = self.hero.weaponXoffset + self.hero.rect.x + 64
        self.rect.y = self.hero.weaponYoffset + self.hero.rect.y

class xBall(pygame.sprite.Sprite):
    def __init__(self,window,hero):
        super().__init__()
        self.window = window
        self.hero = hero

    def update(self):
        pass

class Fireball(xBall):
    def __init__(self,window,hero):
        super().__init__(window,hero)
        self.window = window
        self.hero = hero
        self.image = pygame.image.load(os.path.join('./assets/Projectiles/Fireball','Fireball1.png'))
        self.rect = self.image.get_rect()
        self.rect.x = self.hero.weapon.rect.x + self.hero.weaponXoffset
        self.rect.y = self.hero.weaponYoffset + self.hero.rect.y
        self.xCord = hero.xCord
        self.yCord = hero.yCord
        self.attackFrames = 15
        self.baseDamage = 5
        self.baseVelocity = 5
        self.damage = self.baseDamage + (0.2 * self.hero.baseSpellPower)
        self.velocity = self.baseVelocity + 3
        self.collided = False

        self.lifeSteal = False
        self.lifeStealPower = 0
        if self.hero.lifeSteal:
            self.lifeSteal = True
            self.lifeStealPower += self.hero.lifeStealPower


    def update(self):
        if self.collided:
            self.kill() #without this fireballs can 'pierce' - tghey wont disappear after hitting an enemy
        if self.hero.movingBackward:  # apparently this part is very important and projetiles will disappear if they go out of the view
            self.rect.x += self.hero.movementSpeed
            self.xCord += self.hero.movementSpeed
        if self.hero.movingForward:
            self.rect.x -= self.hero.movementSpeed
            self.xCord -= self.hero.movementSpeed

        if self.xCord < self.hero.mapLevelLength * 1280:
            self.rect.x += self.velocity
            self.xCord += self.velocity

        else:
            self.kill()
