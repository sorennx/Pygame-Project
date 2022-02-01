#todo: onHitEvent, onCollisionEvent etc
import pygame

class GameEventsList:
    def __init__(self):
        self.events = []


    def updateAllObjects(self):
        pass

class itemCollision:
    @classmethod
    def checkItemAndSocketCollision(cls,item,socketGroup):
        # socketsHit = pygame.sprite.spritecollide(item,socketGroup,False)
        # for socket in socketsHit:
        #     print(">", socket.ij, socket.rect.x, socket.rect.y)
        #print(item.rect.x+item.image.get_width()-item.rect.x)
        for socket in socketGroup:
            if socket.rect.x + item.hero.inventoryWindow.rect.x in range(item.rect.x, item.rect.x+item.image.get_width())\
                    and socket.rect.y + item.hero.inventoryWindow.rect.y in range(item.rect.y, item.rect.y+item.image.get_height()):
                print(socket.rect.x + item.hero.inventoryWindow.rect.x)

class ProjectileCollision:
    @classmethod
    def checkProjCollision(cls, projGroup, targetGroup):

        targetsHit = pygame.sprite.groupcollide(projGroup, targetGroup, False, False)
        for proj in targetsHit.keys():
            for tar in targetsHit.values():
                for i in tar:
                    i.currentHp -= (proj.damage)
                    proj.collided = True
                    if proj.lifeSteal and proj.hero.currentHp < proj.hero.maxHp:
                        proj.hero.currentHp += (proj.damage * proj.lifeStealPower)

class BeamCollision:
    @classmethod
    def checkBeamCollision(cls, beamGroup, targetGroup):
        targetsHit = pygame.sprite.groupcollide(beamGroup, targetGroup, False, False)
        for beam in targetsHit.keys():
            for tar in targetsHit.values():
                for i in tar:
                    i.currentHp -= (beam.damage)
                    # if beam.lifeSteal and beam.hero.currentHp < beam.hero.maxHp:
                    #     beam.hero.currentHp += (proj.damage * hero.currentSpellPower) * hero.lifeStealPower
