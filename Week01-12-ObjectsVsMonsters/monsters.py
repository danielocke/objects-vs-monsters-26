from pygame.math import Vector2
from utils import *
from audio import SFX
from fonts import FONTS,COLOURS
from models import Monster


class ExplosiveMonster(Monster):

    def __init__(self, position, scale):
            sprites = ('explosive_monster_a', 'explosive_monster_b', 'explosive_monster_eat')
            super().__init__(position, scale, health = 50, speed = 2, move_cooldown = 3, strength = 1, sprites=sprites)