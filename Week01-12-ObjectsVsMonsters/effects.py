from pygame.math import Vector2

from models import GameObject

import math

class TileEffect(GameObject):
    def __init__(self, position, sprite_name, lifespan, scale=1):
        super().__init__(position, sprite_name, Vector2(0,0), scale, 0)
        self.lifespan  = lifespan


class IceEffect(TileEffect):
    def __init__(self, position, lifespan = 5*100, scale=1, wave_start = 0):
        super().__init__(position, 'ice_effect', lifespan, 1.25*scale)
        self.wave_time = wave_start
        self.y = self.pos[1]

    def update(self):
        self.wave_time += 1
        self.lifespan  -= 1
        self.pos = Vector2(self.pos[0], int(10*math.sin(0.1*self.wave_time)) + self.y)
