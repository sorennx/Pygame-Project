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

        self.baseDamage = 5
        self.damage = self.baseDamage + (0.1 * self.hero.baseSpellPower)

    def update(self):
        self.rect.x = self.hero.weaponXoffset + self.hero.rect.x + 64
        self.rect.y = self.hero.weaponYoffset + self.hero.rect.y