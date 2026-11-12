from pygame.math import Vector2
from utils import *
from audio import SFX
from fonts import FONTS,COLOURS
from models import Unit, Projectile

class Blender(Unit):
    def __init__(self, position, add_proj_callback, scale=1):
        super().__init__(position, 'blender', add_proj_callback, scale, health = 75)
        self.strength = 15

    def _activate(self, monsters):
        
        in_range = (monster for monster in monsters if monster.pos[0] >= self.pos[0])
        
        closest = min(in_range, key = lambda x: x.pos[0], default = None)
        
        if closest:
            lifespan = (abs(closest.pos[0] - self.pos[0]) / 1000) * 90
            self.add_proj_callback({Goo(self.pos + (0,-20), closest, self.strength, self.scale, lifespan)})
            SFX['blender'].play()

class Goo(Projectile):
    def __init__(self, position, target, strength, scale=1, lifespan=30):
        super().__init__(position, 'goo', target, strength, scale, lifespan)

class Toaster(Unit):
    def __init__(self, position, add_proj_callback, scale=1):
        super().__init__(position, 'toaster', add_proj_callback, scale, health = 75)
        self.strength = 8

    def _activate(self, monsters):
        
        in_range = [monster for monster in monsters if monster.pos[0] >= self.pos[0]]
        
        if len(in_range) > 0:
            SFX['toaster'].play()

        projectiles = set()
        for monster in in_range:
            lifespan = (abs(monster.pos[0] - self.pos[0]) / 1000) * 90
            projectiles |= {Toast(self.pos, monster, self.strength, self.scale, lifespan)}

        self.add_proj_callback(projectiles)

class Toast(Projectile):
    def __init__(self, position, target, strength, scale=1, lifespan=30):
        super().__init__(position, 'toast', target, strength, scale, lifespan)

        self.gravity = 2
        self.vel = Vector2(self.vel[0], -(lifespan*self.gravity)/2)

    def update(self):
        self._move()
        self.elapsed += 1

        self.vel += Vector2(0, self.gravity)

        if self.elapsed >= self.lifespan:
            self.target.take_damage(self.strength)

class Microwave(Unit):
    def __init__(self, position, scale=1):
        super().__init__(position, 'microwave', scale = scale, health = 100, attack_cooldown=500)

        self.ready = False
        self.glow_level = 0
        self.MAX_GLOW   = 5
        self.glow = load_sprite('microwave_glow', scale)
        self.GLOW_COOLDOWN = 10
        self.glow_cd = self.GLOW_COOLDOWN
        self.energy_gain = 5

    def update(self, monsters):

        if not self.ready:
            return super().update(monsters)

        else: 
            self.glow_cd -= 1

            if self.glow_cd < 1:
                self.glow_cd = self.GLOW_COOLDOWN
                self.glow_level = (self.glow_level + 1) % self.MAX_GLOW

    def _activate(self, monsters):
        if not self.ready:
            self.ready = True
            SFX['microwave'].play()

    def on_click(self, monsters):
        if self.ready:
            self.ready = False
            self.glow_level = 0
            SFX['energy_gain'].play()
            return self.energy_gain # Gain 5 energy

    def draw(self, surface):
        blit_pos = self.pos - Vector2(self.width/2, self.height/2)
        surface.blit(self.sprite, blit_pos)
        
        for _ in range(self.glow_level):
            surface.blit(self.glow, blit_pos)


class Fridge(Unit):
    def __init__(self, position, create_effect_callback, grid_coordinate, scale=1):
        super().__init__(position, 'fridge', create_effect_callback = create_effect_callback, scale = scale, health = 5000, attack_cooldown=1000)
        self.ready = False
        self.glow_level = 0
        self.MAX_GLOW   = 5
        self.glow = load_sprite('fridge_glow', scale)
        self.GLOW_COOLDOWN = 10
        self.glow_cd = self.GLOW_COOLDOWN

    def update(self, monsters):
    
            if not self.ready:
                return super().update(monsters)
    
            else: 
                self.glow_cd -= 1
    
                if self.glow_cd < 1:
                    self.glow_cd = self.GLOW_COOLDOWN
                    self.glow_level = (self.glow_level + 1) % self.MAX_GLOW

    def _activate(self, monsters):
            if not self.ready:
                self.ready = True

    def on_click(self, monsters):
        if self.ready:
            self.ready = False
            self.glow_level = 0

    def draw(self, surface):
        blit_pos = self.pos - Vector2(self.width/2, self.height/2)
        surface.blit(self.sprite, blit_pos)
        
        for _ in range(self.glow_level):
            surface.blit(self.glow, blit_pos)