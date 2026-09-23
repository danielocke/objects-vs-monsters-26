from pygame.math import Vector2
from utils import *
from audio import SFX
from fonts import FONTS,COLOURS

class GameObject:
    def __init__(self, position, sprite_name, velocity = Vector2(0), scale = 1, health = 0):
        self.pos    = Vector2(position)
        self.sprite = load_sprite(sprite_name, scale)
        self.width  = self.sprite.get_width()
        self.height = self.sprite.get_height()
        self.vel    = Vector2(velocity)
        self.scale  = scale
        self.health = health

    def draw(self, surface):
        blit_pos = self.pos - Vector2(self.width/2, self.height/2)
        surface.blit(self.sprite, blit_pos)
    
    def _move(self):
        self.pos = self.pos + self.vel
    
    def update(self):
        self._move()

    def take_damage(self, amt):
        self.health -= amt

class Unit(GameObject):
    def __init__(self, position, sprite_name, scale=1, health = 100, attack_cooldown = 120):
        super().__init__(position, sprite_name, scale=scale, health=health)
        self.ATTACK_COOLDOWN = attack_cooldown
        self.HOP_COOLDOWN = 180
        self.atk_cd = self.ATTACK_COOLDOWN
        self.hop_cd = self.HOP_COOLDOWN
        