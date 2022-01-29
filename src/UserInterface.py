import pygame
import os
pygame.font.init()
FONT = pygame.font.SysFont('Verdana',12)
HP_BAR = pygame.image.load(os.path.join('./assets/UI/LifeBar', 'LifeBar.png'))
#HP_BAR = pygame.transform.scale(HP_BAR,(200,40))
#CHAR_SHEET_IMG = pygame.image.load(os.path.join('./assets/UI/CharacterSheet', 'CharacterSheet.png'))


class HpBar(pygame.sprite.DirtySprite):
    def __init__(self,hero,window):
        super().__init__()
        self.window = window
        self.hero = hero
        self.image = HP_BAR
        self.rect = self.image.get_rect()
        self.rect.y = self.window.get_height() - self.image.get_height()
        self.rect.x = 0



    def update(self):

        pygame.draw.rect(self.window, (180,0,0), (self.rect.x-2, self.rect.y, self.image.get_width()*self.hero.currentHp/self.hero.maxHp, self.image.get_height()))


class CharacterSheet(pygame.sprite.Sprite):
    def __init__(self,window,hero):
        super().__init__()
        self.isOpen = False
        self.window = window
        self.hero = hero
        self.fontsize = 24
        self.font = pygame.font.Font(os.path.join('./assets/Fonts','Fontin-Regular.ttf'),self.fontsize) #Poe font - Fontin
        self.image = pygame.image.load(os.path.join('./assets/UI/CharacterSheet', 'CharacterSheet.png'))
        self.rect = self.image.get_rect()

    def drawCharacterSheet(self):
        charName = self.font.render(f'{self.hero.characterName}', True, "#101010")
        charNameRect = charName.get_rect()
        charNameRect.x = self.rect.x+25+12
        charNameRect.y = self.rect.y + 35
        self.image.blit(charName, (charNameRect.x, charNameRect.y))

        maxHp = self.font.render(f'Max life: {self.hero.maxHp}',True,"#101010")
        maxHpRect = maxHp.get_rect()
        maxHpRect.x = self.rect.x+30
        maxHpRect.y = self.rect.y+120
        self.image.blit(maxHp, (maxHpRect.x,maxHpRect.y))

        spellPower = self.font.render(f'Spell power: {self.hero.baseSpellPower}', True, "#101010")
        spellPowerRect = maxHp.get_rect()
        spellPowerRect.x = self.rect.x+30
        spellPowerRect.y = self.rect.y + 120 + self.fontsize
        self.image.blit(spellPower, (spellPowerRect.x, spellPowerRect.y))

        movementSpeed = self.font.render(f'Movement speed: {self.hero.movementSpeed}', True, "#101010")
        movementSpeedRect = movementSpeed.get_rect()
        movementSpeedRect.x = self.rect.x+30
        movementSpeedRect.y = self.rect.y + 120 + self.fontsize*2
        self.image.blit(movementSpeed, (movementSpeedRect.x, movementSpeedRect.y))

    def update(self):
        self.drawCharacterSheet()

class Inventory():
    pass

class SkillWindow():
    pass
