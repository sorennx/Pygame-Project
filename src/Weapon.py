import pygame
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
