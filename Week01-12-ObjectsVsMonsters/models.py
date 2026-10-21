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

    def clicked(self, mouse_pos):
        hitbox = self.sprite.get_rect()
        hitbox.center = self.pos
        return hitbox.collidepoint(mouse_pos)

class Unit(GameObject):
    def __init__(self, position, sprite_name, add_proj_callback, scale=1, health = 100, attack_cooldown = 120):
        super().__init__(position, sprite_name, scale=scale, health=health)
        self.ATTACK_COOLDOWN = attack_cooldown
        self.HOP_COOLDOWN = 180
        self.atk_cd = self.ATTACK_COOLDOWN
        self.hop_cd = self.HOP_COOLDOWN
        self.hop_speed = 2
        self.add_proj_callback = add_proj_callback
    
    def update(self, monsters):
        super().update()

        self.atk_cd -= 1
        self.hop_cd -= 1

        if self.hop_cd == 0:
            self.vel = Vector2(0, -self.hop_speed)
        
        if self.hop_cd == -5:
            self.vel = Vector2(0, self.hop_speed)

        if self.hop_cd == -10:
            self.vel = Vector2(0, 0)
            self.hop_cd = self.HOP_COOLDOWN

        if self.atk_cd < 1:
            self.atk_cd = self.ATTACK_COOLDOWN
            return self._activate(monsters)

    def _activate(self, monsters):
        return

    def on_click(self):
        return

class Monster(GameObject):    
    def __init__(self, position, scale, health = 100, speed = 1, move_cooldown = 3, strength = 1,
                 sprites = ('monster_a', 'monster_b', 'monster_eat')):
        super().__init__(position, sprites[0], (-speed,0), scale, health)
        self.sprites = {
            'a'   : load_sprite(sprites[0], scale = scale),
            'b'   : load_sprite(sprites[1], scale = scale),
            'eat' : load_sprite(sprites[2], scale = scale),
        }
        self.strength = strength

        self.MOVE_COOLDOWN = move_cooldown
        self.POSE_COOLDOWN = 30
        self.move_cd = self.MOVE_COOLDOWN
        self.pose_cd = self.POSE_COOLDOWN
        self.EAT_RANGE = 25

        self.pose = 'a'
        self.state = 'move'

    def update(self, row, row_coords):
        eat_tile = None
        for tile in range(len(row)):
            if row[tile] and abs(row_coords[tile][0] - self.pos[0]) < self.scale * self.EAT_RANGE:
                self.state = 'eat'
                eat_tile = tile
                break
            else:
                self.state = 'move'

        self.move_cd -= 1
        self.pose_cd -= 1

        if self.state == 'move':
            
            if self.move_cd < 1:
                self.move_cd = self.MOVE_COOLDOWN
                self._move()

            if self.pose_cd < 1:
                self.pose = 'a' if self.pose == 'b' else 'b'
                self.sprite = self.sprites[self.pose]
                self.pose_cd = self.POSE_COOLDOWN

        if self.state == 'eat':
                    
            if self.move_cd < 1:
                self.move_cd = self.MOVE_COOLDOWN
                self._eat(row[eat_tile])

            if self.pose_cd < 1:
                self.pose = 'a' if self.pose == 'eat' else 'eat'
                self.sprite = self.sprites[self.pose]
                self.pose_cd = self.POSE_COOLDOWN

                if self.pose == 'eat':
                    SFX['chomp'].play()

    def _eat(self, unit:Unit):
        unit.take_damage(self.strength)

class Projectile(GameObject):
    def __init__(self, position, sprite_name, target, strength, scale=1, lifespan=30):

        velocity = (target.pos + target.vel * lifespan - position) / lifespan

        super().__init__(position, sprite_name, velocity, scale)

        self.target = target
        self.strength = strength
        self.lifespan = lifespan
        self.elapsed  = 0

    def update(self):
        super().update()
        self.elapsed += 1

        if self.elapsed >= self.lifespan:
            self.target.take_damage(self.strength)
            SFX['impact'].play()

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
        super().__init__(position, 'microwave', None, scale, health = 100, attack_cooldown=500)

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

    def on_click(self):
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

class Card(GameObject):
    def __init__(self, position, card_type, cost):
        super().__init__(position, 'card')
        self.card_type = card_type
        self.unit = load_sprite(card_type, scale=0.75)
        self.cost = cost
        self.start_pos = Vector2(position)
        self.selected = False

    def update(self, mouse_pos):
        if self.selected:
            self._move(mouse_pos)

    def _move(self, mouse_pos):
        self.pos = mouse_pos

    def reset(self):
        self.selected = False
        self.pos      = self.start_pos

    def draw(self, surface, energy):
        super().draw(surface)
        unit_pos = self.pos - Vector2(self.unit.get_width()/2, self.unit.get_height/2)
        text_pos = self.pos - Vector2(self.width/3, self.height/3)

        surface.blit(self.unit, unit_pos)
        if energy < self.cost:
            col = COLOURS['grey_purple']
        else:
            col = COLOURS['white_purple']

        write(surface, str(self.cost), text_pos, FONTS['tiny'], col, align = 'center')
