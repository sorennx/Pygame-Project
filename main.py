import pygame
import os

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

#Characters after scaling
#BOB_CHARACTER = pygame.transform.scale(BOB_CHARACTER_IMAGE, (150,150))

class Game(object):
    def __init__(self, gameName, tickRate,width, height):
        self.gameName = gameName
        self.tickRate = tickRate
        self.width = width
        self.height = height
        self.gameWindow = self.getGameWindow()
        self.characterList = []
        self.characterCount = 0
        self.createCharacters()

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

    def createCharacters(self, n=2):
        for i in range(n):
            self.createCharacter()

    def mainLoop(self):
        run = True
        clock = pygame.time.Clock()
        bob1 = self.characterList[0]

        while run:
            clock.tick(self.tickRate)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            self.drawWindow(bob1)
            #self.characterList[0].charPos.x += 1
            keys_pressed = pygame.key.get_pressed()

            self.handleMovement(keys_pressed,bob1)

    def drawWindow(self, char1):
        self.gameWindow.fill(WHITE)
        self.drawBackground()

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
        self.hp = healthPoints
        self.ad = attackDamage
        self.characterImage = characterImage
        self.characterWidth = 150
        self.characterHeight = 150
        self.xStartCoords = 0
        self.yStartCoords = 200
        self.characterVelocity = 5
        self.charPos = pygame.Rect(self.xStartCoords, self.yStartCoords, self.characterWidth, self.characterHeight)



def main():
    gameName = "ExileOfPath"
    WIDTH = 900
    HEIGHT = 500
    TICKRATE = 60
    game = Game(gameName, TICKRATE, WIDTH, HEIGHT)
    game.mainLoop()

if __name__ == '__main__':
    main()

