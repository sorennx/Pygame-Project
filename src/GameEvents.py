#todo: onHitEvent, onCollisionEvent etc
import pygame



class ProjectileCollision:
    @classmethod
    def checkProjCollision(cls, projGroup, targetGroup):

        targetsHit = pygame.sprite.groupcollide(projGroup, targetGroup, False, False)
        for proj in targetsHit.keys():
            for tar in targetsHit.values():
                for i in tar:
                    i.currentHp -= (proj.damage)
                    # if beam.lifeSteal and beam.hero.currentHp < beam.hero.maxHp:
                    #     beam.hero.currentHp += (proj.damage * hero.currentSpellPower) * hero.lifeStealPower
                    proj.colided = True

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
