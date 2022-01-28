import pygame
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