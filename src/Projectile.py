import pygame


class Projectile(pygame.sprite.DirtySprite):
    def __init__(self,window, x,y,image,hero, velocity = 12):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.xCord = hero.xCord
        self.yCord = hero.yCord
        self.velocity = velocity
        self.window = window
        self.damage = 10
        self.hero = hero

        if self.hero.lifeSteal == True:
            self.lifeSteal = True

    def update(self):

        if self.hero.movingBackward: #apparently this part is very important and projetiles will disappear if they go out of the view
            self.rect.x += self.hero.movementSpeed
            self.xCord += self.hero.movementSpeed
        if self.hero.movingForward:
            self.rect.x -= self.hero.movementSpeed
            self.xCord -= self.hero.movementSpeed

        if self.xCord < self.hero.mapLevelLength*1280:
            self.rect.x += self.velocity
            self.xCord += self.velocity

        else:
            self.kill()