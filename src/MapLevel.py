from Background import *

class MapLevel:
    def __init__(self,areaLevel,enemyLevel,length,backgroundImg,window,hero):
        self.areaLevel = areaLevel
        self.enemyLevel = enemyLevel
        self.levelLength = length
        self.backgroundImg = backgroundImg
        self.window = window
        self.hero = hero
        self.backgroundList = []
        self.createLevel()
        hero.mapLevelLength = length

    def createLevel(self):

        for i in range(self.levelLength):
            t = Background(self.backgroundImg,self.window,self.hero)
            t.rect.x = t.image.get_width()*i
            self.backgroundList.append(t)

    def moveAllBackgrounds(self):
        for i in range(len(self.backgroundList)):
            if self.hero.movingForward:
                self.backgroundList[i].rect.x -= self.hero.movementSpeed
            if self.hero.movingBackward:
                self.backgroundList[i].rect.x += self.hero.movementSpeed
