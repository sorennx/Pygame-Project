import pygame
from GameEvents import *

class Item(pygame.sprite.Sprite):
    def __init__(self,name,img,x,y,gameEvents,hero, spellPower,attackDamage,attackSpeed,castSpeed):
        super().__init__()
        self.events = gameEvents.events
        self.hero = hero

        self.name = name
        self.image = img
        self.backUpImg = img
        self.icon = pygame.transform.scale(self.image,(30,30)) #make it tad bit smaller so that a frame can be added

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        #Stuff used to being moved:
        self.isPickedUp = False

        #inventory related stuff:
        self.isInInventory = False
        self.socketIJ = None
        #Atributes
        self.spellPower = spellPower
        self.castSpeed = castSpeed

        self.attackDamage = attackDamage
        self.attackSpeed = attackSpeed

    def minimizeImg(self,tempxy):
        self.image = self.icon
        self.rect = self.image.get_rect()
        self.rect.center = tempxy

    def maximizeImg(self,tempxy):
        self.image = self.backUpImg
        self.rect = self.image.get_rect()
        self.rect.center = tempxy

    def update(self):
        tempxy = self.rect.center

        #Adjust location on the screen if hero is moving
        if not self.isPickedUp:
            if self.hero.movingBackward:
                self.rect.x += self.hero.movementSpeed
            if self.hero.movingForward:
                self.rect.x -= self.hero.movementSpeed

        if self.isPickedUp:
            self.minimizeImg(tempxy)
        if not self.isPickedUp:
            self.maximizeImg(tempxy)

        if self.isPickedUp and self.hero.inventoryWindow.isOpen:
            #print(self.rect.x,self.rect.y)
            self.socketIJ = itemCollision.checkItemAndSocketCollision(self, self.hero.inventoryWindow.inventorySlotGroup)
            self.putItemInSocket()

        for event in self.hero.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if x in range(self.rect.x, self.rect.x + self.image.get_width()) and y in range(self.rect.y, self.rect.y + self.image.get_height()):
                    #print(f"Clicking on an item!")
                    self.isPickedUp = True

            self.pickUpItem(event)
            self.putDownItem(event)

    def pickUpItem(self,event):
        if self.isPickedUp == True:
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                self.rect.center = [x,y]

    def putDownItem(self,event):
        if self.isPickedUp == True:
            if event.type == pygame.MOUSEBUTTONUP:
                self.isPickedUp = False
                x, y = event.pos
                self.rect.center = [x,y]

    def putItemInSocket(self):
        if self.isInInventory == False:
            for socket in self.hero.inventoryWindow.inventorySlotGroup:
                if socket.ij == self.socketIJ:
                    socket.item = self
                    self.isInInventory = True
                    print(socket.item)

class QuestItem(Item):
    pass


class NormalItem(Item):
    pass


class MagicItem(Item):
    pass


class RareItem(Item):
    pass


class LegendaryItem(Item):
    pass


class Currency:
    pass