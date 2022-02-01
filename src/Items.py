import pygame
from GameEvents import *

class Item(pygame.sprite.Sprite):
    def __init__(self,name,img,x,y,gameEvents,hero, spellPower,attackDamage,attackSpeed,castSpeed):
        super().__init__()
        self.gameEvents = gameEvents
        self.events = self.gameEvents.events
        self.hero = hero

        self.name = name
        self.image = img
        self.backUpImg = img
        self.icon = pygame.transform.scale(self.image,(30,30)) #make it tad bit smaller so that a frame can be added
        self.description = "" #add this to the init method
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

        if self.isPickedUp:
            self.minimizeImg(tempxy)

        if not self.isPickedUp:
            self.maximizeImg(tempxy)

        if self.isPickedUp and self.hero.inventoryWindow.isOpen:
            #print(self.rect.x,self.rect.y)
            self.socketIJ = itemCollision.checkItemAndSocketCollision(self, self.hero.inventoryWindow.inventorySlotGroup)
            self.putItemInSocket(tempxy)

        for event in self.hero.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if x in range(self.rect.x, self.rect.x + self.image.get_width()) and y in range(self.rect.y, self.rect.y + self.image.get_height()):
                    #print(f"Clicking on an item!")
                    self.isPickedUp = True

            self.pickUpItem(event)
            self.putDownItem(event)

        # Adjust location on the screen if hero is moving
        if not self.isPickedUp and not self.isInInventory:
            if self.hero.movingBackward:
                self.rect.x += self.hero.movementSpeed
            if self.hero.movingForward:
                self.rect.x -= self.hero.movementSpeed

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

    def createCopy(self):
        copy = Item(self.name,self.image,self.rect.center[0],self.rect.center[1],self.gameEvents,self.hero,self.spellPower,self.attackDamage,self.attackSpeed,self.castSpeed)
        return copy

    def putItemInSocket(self,tempxy):
        if self.isInInventory == False:
            for socket in self.hero.inventoryWindow.inventorySlotGroup:
                if socket.ij == self.socketIJ and socket.isEmpty:
                    #print(f"Putting item in a socket: {socket.ij}")
                    copy = self.createCopy()
                    #copy.minimizeImg(tempxy)
                    socket.item = copy
                    copy.isInInventory = True
                    copy.isPickedUp = False
                    self.kill()

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