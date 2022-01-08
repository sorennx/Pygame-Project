import pygame
import os

#initialising IS_MODULE_SDK
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
EVILBAKER_CHARACTER_IMAGE = pygame.image.load(os.path.join('Assets','Evilbaker_Character.png'))
EVILBAKER_CHARACTER_IMAGE = pygame.transform.scale(EVILBAKER_CHARACTER_IMAGE,(150,150))

HP_BAR_FULL = pygame.image.load(os.path.join('Assets','HP_Bar_Full.png'))
HP_BAR_80 = pygame.image.load(os.path.join('Assets','HP_BAR_80.png'))
HP_BAR_60 = pygame.image.load(os.path.join('Assets','HP_BAR_60.png'))
HP_BAR_40 = pygame.image.load(os.path.join('Assets','HP_BAR_40.png'))
HP_BAR_20 = pygame.image.load(os.path.join('Assets','HP_BAR_20.png'))
#Characters after scaling
#BOB_CHARACTER = pygame.transform.scale(BOB_CHARACTER_IMAGE, (150,150))
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)

#todo: hpBarAboveCharacter, hpBarInTheCorner, new models for the character, new background image, refractor code into different files/modules

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
        self.createCharacters()
        self.createEnemies()
        self.healthFont = pygame.font.SysFont('verdana', 14)

    def drawBackground(self, stage=0):
        if stage == 0:
            self.gameWindow.blit(BACKGROUND,(0,0))

    def getGameWindow(self):
        window = pygame.display.set_mode((self.width, self.height))  # window
        pygame.display.set_caption(self.gameName)

        return window

    def createCharacter(self):
        name = "Bob"
        healthPoints = 100
        attackDamage = 10
        characterImage = JOHN_CHARACTER_IMAGE
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

    def createEnemies(self, n=1):
        for i in range(n):
            self.createEnemy()

    def drawCharacterHp(self, char):
        charHptext = self.healthFont.render(str(char.currentHp), True, BLACK)
        self.gameWindow.blit(charHptext,(char.charPos.x+char.characterWidth/2-20, char.charPos.y-10))
        pygame.display.update()

    def mainLoop(self):
        run = True
        clock = pygame.time.Clock()
        bob1 = self.characterList[0]

        evilbaker1 = self.enemyList[0]
        while run:
            clock.tick(self.tickRate)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            self.drawWindow(bob1,evilbaker1)
            self.updateCharacterHpBar(bob1)
            self.drawCharacterHp(bob1) #move those methods drawing characters to the class of the object ? add property so that when a character moves, hp moves too ?
            self.drawCharacterHp(evilbaker1)
            bob1.currentHp = 87
            #self.characterList[0].charPos.x += 1
            keys_pressed = pygame.key.get_pressed()

            self.handleMovement(keys_pressed,bob1)

    def updateCharacterHpBar(self,char):
        char.hpBarAboveCharacter.x = char.charPos.x+char.characterWidth/2-30
        char.hpBarAboveCharacter.y = char.charPos.y-10
        if char.currentHp/char.maxHp >= 1:
            self.gameWindow.blit(HP_BAR_FULL,(char.hpBarAboveCharacter.x, char.hpBarAboveCharacter.y))
        elif char.currentHp/char.maxHp >= 0.8:
            self.gameWindow.blit(HP_BAR_80, (char.hpBarAboveCharacter.x, char.hpBarAboveCharacter.y))
        elif char.currentHp/char.maxHp >= 0.6:
            self.gameWindow.blit(HP_BAR_60, (char.hpBarAboveCharacter.x, char.hpBarAboveCharacter.y))
        elif char.currentHp/char.maxHp >= 0.4:
            self.gameWindow.blit(HP_BAR_40, (char.hpBarAboveCharacter.x, char.hpBarAboveCharacter.y))
        elif char.currentHp/char.maxHp >= 0.2:
            self.gameWindow.blit(HP_BAR_20, (char.hpBarAboveCharacter.x, char.hpBarAboveCharacter.y))
        pygame.display.update()

    def drawWindow(self, char1, enemy1):
        self.gameWindow.fill(WHITE)
        self.drawBackground()
        #draw characters using loop, ideally
        self.gameWindow.blit(enemy1.characterImage, (enemy1.charPos.x, enemy1.charPos.y))

        self.gameWindow.blit(char1.characterImage, (char1.charPos.x, char1.charPos.y))

        pygame.display.update()

    def handleMovement(self,keysPressed, character):
        if keysPressed[pygame.K_a]:
            character.charPos.x -= character.characterVelocity
        if keysPressed[pygame.K_s]:
            character.charPos.y += character.characterVelocity
        if keysPressed[pygame.K_w]:
            character.charPos.y -= character.characterVelocity
        if keysPressed[pygame.K_d]:
            character.charPos.x += character.characterVelocity

class Character(object):
    def __init__(self, name, healthPoints, attackDamage, characterImage):
        self.name = name
        self.maxHp = healthPoints
        self.currentHp = self.maxHp
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
        self.characterWidth = 150
        self.characterHeight = 150
        self.xStartCoords = 700
        self.yStartCoords = 200
        self.characterVelocity = 5
        self.charPos = pygame.Rect(self.xStartCoords, self.yStartCoords, self.characterWidth, self.characterHeight)

class Boss(Enemy):
    pass


def main():
    gameName = "ExileOfPath"
    WIDTH = 900
    HEIGHT = 500
    TICKRATE = 60
    game = Game(gameName, TICKRATE, WIDTH, HEIGHT)
    game.mainLoop()

if __name__ == '__main__':
    main()

