import pygame
import os
import time
#initialising pygame modules
pygame.font.init()


#predifened RBG colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
#Images
BOB_CHARACTER_IMAGE = pygame.image.load(os.path.join('Assets', 'Bob_Character.png'))
JOHN_CHARACTER_IMAGE = pygame.image.load(os.path.join('Assets','John_Character.png'))
TEST_IMAGE = pygame.image.load(os.path.join('Assets','test.png'))
BACKGROUND = pygame.image.load(os.path.join('Assets','Background.png'))
EVILBAKER_CHARACTER_IMAGE = pygame.image.load(os.path.join('Assets','Evilbaker2_Character.png'))
EVILBAKER_CHARACTER_IMAGE = pygame.transform.scale(EVILBAKER_CHARACTER_IMAGE,(250,250))

HP_BAR_FULL = pygame.image.load(os.path.join('Assets','HP_Bar_Full.png'))
HP_BAR_80 = pygame.image.load(os.path.join('Assets','HP_BAR_80.png'))
HP_BAR_60 = pygame.image.load(os.path.join('Assets','HP_BAR_60.png'))
HP_BAR_40 = pygame.image.load(os.path.join('Assets','HP_BAR_40.png'))
HP_BAR_20 = pygame.image.load(os.path.join('Assets','HP_BAR_20.png'))
#Characters after scaling
#BOB_CHARACTER = pygame.transform.scale(BOB_CHARACTER_IMAGE, (150,150))
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)

#Attacks
EVILBAKER_BASIC_ATTACK_IMG1 = pygame.transform.scale(pygame.image.load(os.path.join('Assets/BaguetteAttack','Evilbaker2_BasicAttack1.png')),(250,250))
EVILBAKER_BASIC_ATTACK_IMG2 = pygame.transform.scale(pygame.image.load(os.path.join('Assets/BaguetteAttack','Evilbaker2_BasicAttack2.png')),(250,250))
EVILBAKER_BASIC_ATTACK_IMG3 = pygame.transform.scale(pygame.image.load(os.path.join('Assets/BaguetteAttack','Evilbaker2_BasicAttack3.png')),(250,250))
EVILBAKER_BASIC_ATTACK_IMG4 = pygame.transform.scale(pygame.image.load(os.path.join('Assets/BaguetteAttack','Evilbaker2_BasicAttack4.png')),(250,250))
EVILBAKER_BASIC_ATTACK_IMG5 = pygame.transform.scale(pygame.image.load(os.path.join('Assets/BaguetteAttack','Evilbaker2_BasicAttack5.png')),(250,250))
EVILBAKER_BASIC_ATTACK_IMG6 = pygame.transform.scale(pygame.image.load(os.path.join('Assets/BaguetteAttack','Evilbaker2_BasicAttack6.png')),(250,250))



EVILBAKER_BASIC_ATTACK_IMG_LIST = [
    pygame.image.load(os.path.join('Assets/BaguetteAttack','Evilbaker2_BasicAttack1.png'))

]

#todo: align hpBarAboveCharacter with hptext, hpBarInTheCorner, new models for the character, new background image, refractor code into different files/modules

class Game(object):
    def __init__(self, gameName, tickRate,width, height):
        self.gameName = gameName
        self.tickRate = tickRate
        self.width = width
        self.height = height
        self.gameWindow = self.getGameWindow()
        self.characterList = []
        self.characterCount = 0
        self.enemyList = []
        self.enemyCount = 0
        self.healthFont = pygame.font.SysFont('verdana', 14)


    def drawBackground(self, stage=0):
        if stage == 0:
            self.gameWindow.blit(BACKGROUND,(0,0))

    def getGameWindow(self):
        window = pygame.display.set_mode((self.width, self.height))  # window
        pygame.display.set_caption(self.gameName)

        return window

    def createCharacter(self, image = JOHN_CHARACTER_IMAGE):
        name = "Bob"
        healthPoints = 100
        attackDamage = 10
        characterImage = image
        char = Character(name, healthPoints, attackDamage, characterImage)
        self.characterList.append(char)
        self.characterCount += 1

    def createEnemy(self):
        name = "Evil Baker"
        healthPoints = 100
        attackDamage = 10
        characterImage = EVILBAKER_CHARACTER_IMAGE
        enemy = Enemy(name, healthPoints, attackDamage, characterImage)
        self.enemyList.append(enemy)
        self.enemyCount += 1

    def createCharacters(self, n=1):
        for i in range(n):
            self.createCharacter()

    def updateAllCharacters(self):
        for i in self.characterList:
            i.updateChar(self.gameWindow)


        for j in self.enemyList:
            j.updateChar(self.gameWindow)

        pygame.display.update()

    def createEnemies(self, n=1):
        for i in range(n):
            self.createEnemy()

    def mainLoop(self):
        run = True
        clock = pygame.time.Clock()
        #Creating characters and enemies
        self.createCharacters()
        self.createEnemies()

        bob1 = self.characterList[0]
        kanye1 = self.enemyList[0]
        while run:
            clock.tick(self.tickRate)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            self.drawWindow()
            self.updateAllCharacters()


            keys_pressed = pygame.key.get_pressed()
            self.handleCharMovement(keys_pressed,bob1)
            self.handleEnemyMovement(keys_pressed,kanye1)
    def drawWindow(self):
        self.gameWindow.fill(WHITE)
        self.drawBackground()
        #pygame.display.update()

    def handleCharMovement(self,keysPressed, character):
        if keysPressed[pygame.K_a]:
            character.charPos.x -= character.characterVelocity
        if keysPressed[pygame.K_s]:
            character.charPos.y += character.characterVelocity
        if keysPressed[pygame.K_w]:
            character.charPos.y -= character.characterVelocity
        if keysPressed[pygame.K_d]:
            character.charPos.x += character.characterVelocity

    def handleEnemyMovement(self,keysPressed, character):
        if keysPressed[pygame.K_g]:
            character.charPos.x -= character.characterVelocity
        if keysPressed[pygame.K_h]:
            character.charPos.y += character.characterVelocity
        if keysPressed[pygame.K_y]:
            character.charPos.y -= character.characterVelocity
        if keysPressed[pygame.K_j]:
            character.charPos.x += character.characterVelocity
        if keysPressed[pygame.K_x]:
            character.visible = False
            character.performBasicAttack(self.gameWindow)
            character.visible = True
class Character(object):
    def __init__(self, name, healthPoints, attackDamage, characterImage):
        self.name = name
        self.maxHp = healthPoints
        self.currentHp = self.maxHp
        self.healthFont = pygame.font.SysFont('verdana', 14)
        self.characterHpBarImage = HP_BAR_FULL
        self.ad = attackDamage
        self.characterLevel = 1
        self.characterImage = characterImage
        self.characterWidth = 120
        self.characterHeight = 120
        self.xStartCoords = 0
        self.yStartCoords = 200
        self.characterVelocity = 5
        self.charPos = pygame.Rect(self.xStartCoords, self.yStartCoords, self.characterWidth, self.characterHeight)
        self.hpAboveCharacterHeight = 10
        self.hpAboveCharacterWidth = 50
        #self.hpAboveCharacter = pygame.Rect(self.charPos.x+10, self.charPos.y-10, self.hpAboveCharacterWidth,self.characterHeight)
        self.hpBarAboveCharacter = pygame.Rect(self.characterWidth/2, self.charPos.y-10, self.hpAboveCharacterWidth, self.hpAboveCharacterHeight)
        self.visible = True

    def updateChar(self, window):
        self.updateCharacterHpBar()
        self.drawCharacterHpText(window)
        self.drawAboveCharacterHpBar(window)

        if self.visible == True:
            self.drawCharacterImage(window)

    def drawCharacterImage(self,window):
        window.blit(self.characterImage, (self.charPos.x, self.charPos.y))

    def drawCharacterHpText(self, window):
        charHpText = self.healthFont.render(str(self.currentHp), True, BLACK)
        window.blit(charHpText, (self.hpBarAboveCharacter.x+5, self.hpBarAboveCharacter.y))

    def drawAboveCharacterHpBar(self,window):
        window.blit(self.characterHpBarImage,(self.hpBarAboveCharacter.x, self.hpBarAboveCharacter.y))

    def updateCharacterHpBar(self): #todo: change those ifs so that they are a property, draw hp bar based on the image of the class attribute instead
        self.hpBarAboveCharacter.x = self.charPos.x+self.characterWidth/2-30
        self.hpBarAboveCharacter.y = self.charPos.y-10
        if self.currentHp/self.maxHp >= 1:
            self.characterHpBarImage = HP_BAR_FULL

        elif self.currentHp/self.maxHp >= 0.8:
            self.characterHpBarImage = HP_BAR_80

        elif self.currentHp/self.maxHp >= 0.6:
            self.characterHpBarImage = HP_BAR_60

        elif self.currentHp/self.maxHp >= 0.4:
            self.characterHpBarImage = HP_BAR_40

        elif self.currentHp/self.maxHp >= 0.2:
            self.characterHpBarImage = HP_BAR_20


class Hero(Character):
    pass


class Enemy(object):
    def __init__(self,name,healthPoints,attackDamage,characterImage):
        self.name = name
        self.maxHp = healthPoints
        self.currentHp = self.maxHp
        self.characterLevel = 1
        self.ad = attackDamage
        self.characterImage = characterImage
        self.characterWidth = 250
        self.characterHeight = 250
        self.xStartCoords = 700
        self.yStartCoords = 200
        self.characterVelocity = 5
        self.healthFont = pygame.font.SysFont('verdana', 14)
        self.charPos = pygame.Rect(self.xStartCoords, self.yStartCoords, self.characterWidth, self.characterHeight)
        self.hpAboveCharacterHeight = 10
        self.hpAboveCharacterWidth = 50
        #self.hpAboveCharacter = pygame.Rect(self.charPos.x+10, self.charPos.y-10, self.hpAboveCharacterWidth,self.characterHeight)
        self.hpBarAboveCharacter = pygame.Rect(self.characterWidth/2, self.charPos.y-10, self.hpAboveCharacterWidth, self.hpAboveCharacterHeight)
        self.hostile = True
        self.visible = True
        self.gcdValue = 1
        self.gcd = False

        self.basicAttackImgList = [EVILBAKER_BASIC_ATTACK_IMG1,EVILBAKER_BASIC_ATTACK_IMG2,EVILBAKER_BASIC_ATTACK_IMG3,EVILBAKER_BASIC_ATTACK_IMG4,EVILBAKER_BASIC_ATTACK_IMG5,EVILBAKER_BASIC_ATTACK_IMG6]

    def updateChar(self, window):
        self.updateCharacterHpBar()
        self.drawCharacterHpText(window)
        self.drawAboveCharacterHpBar(window)

        if self.visible == True:
            self.drawCharacterImage(window)

    def drawCharacterImage(self, window):
        window.blit(self.characterImage, (self.charPos.x, self.charPos.y))

    def drawCharacterHpText(self, window):
        charHpText = self.healthFont.render(str(self.currentHp), True, BLACK)
        window.blit(charHpText, (self.hpBarAboveCharacter.x+5, self.hpBarAboveCharacter.y+50))

    def drawAboveCharacterHpBar(self, window):
        window.blit(self.characterHpBarImage, (self.hpBarAboveCharacter.x+5, self.hpBarAboveCharacter.y+50))

    def updateCharacterHpBar(self):  # todo: change those ifs so that they are a property, draw hp bar based on the image of the class attribute instead
        self.hpBarAboveCharacter.x = self.charPos.x + self.characterWidth / 2 - 30
        self.hpBarAboveCharacter.y = self.charPos.y - 10
        if self.currentHp / self.maxHp >= 1:
            self.characterHpBarImage = HP_BAR_FULL

        elif self.currentHp / self.maxHp >= 0.8:
            self.characterHpBarImage = HP_BAR_80

        elif self.currentHp / self.maxHp >= 0.6:
            self.characterHpBarImage = HP_BAR_60

        elif self.currentHp / self.maxHp >= 0.4:
            self.characterHpBarImage = HP_BAR_40

        elif self.currentHp / self.maxHp >= 0.2:
            self.characterHpBarImage = HP_BAR_20

    def performBasicAttack(self,window):
        if self.gcd == False:
            for i in self.basicAttackImgList:
                window.blit(i,(self.charPos.x, self.charPos.y))
                pygame.display.update()
            #self.gcd = True



class Boss(Enemy):
    pass


def main():
    gameName = "ExileOfPath by CCCC"
    WIDTH = 900
    HEIGHT = 500
    TICKRATE = 60
    game = Game(gameName, TICKRATE, WIDTH, HEIGHT)
    game.mainLoop()

if __name__ == '__main__':
    main()

