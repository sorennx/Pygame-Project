import pygame
import os
HP_BAR = pygame.image.load(os.path.join('./assets/HpBar', 'HpBar.png'))

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
