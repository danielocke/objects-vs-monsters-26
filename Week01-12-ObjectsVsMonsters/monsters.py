from pygame.math import Vector2
from utils import *
from audio import SFX
from fonts import FONTS,COLOURS
from models import Monster
import numpy as np

class ExplosiveMonster(Monster):

    def __init__(self, position, scale, create_effect_callback, row):
        sprites = ('explosive_monster_a', 'explosive_monster_b', 'explosive_monster_eat')
        super().__init__(position, scale, health = 1, speed = 2, move_cooldown = 3, strength = 1, sprites=sprites)
        self.explosion_sprite = load_sprite('explosion',scale = scale)
        self.create_effect_callback = create_effect_callback
        self.row = row

    def update(self, row, row_coords, tile_effects):
        if self.health < 1:
            dists = [self.pos.distance_to(coord) for coord in row_coords]
            col = np.argmin(dists)
            self.create_effect_callback([(self.row, col)], 'tile', 'explosion', lifespan = 60)
        return super().update(row, row_coords, tile_effects)

        
        