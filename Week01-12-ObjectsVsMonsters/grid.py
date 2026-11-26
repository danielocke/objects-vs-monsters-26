from models import *
from units  import *
from effects import *
from monsters import *
from pygame.math import Vector2

TILE_RADIUS = 25

class Grid:
    def __init__(self, num_cols, num_rows, summon_x):
        self.tiles = [[None for _ in range(num_cols)] for _ in range(num_rows)]

        self.TILE_COORDS = [[(118 + 70*i,105) for i in range(num_cols)],
                            [(102 + 74*i,160) for i in range(num_cols)],
                            [(86  + 78*i,220) for i in range(num_cols)],
                            [(68  + 83*i,285) for i in range(num_cols)],
                            [(52  + 87*i,355) for i in range(num_cols)]
                            ]

        self.monsters = [set() for _ in range(num_rows)]
        self.projectiles = set()
        self.num_rows = num_rows
        self.num_cols = num_cols
        
        self.summon_x = summon_x

        self.tile_effects = [[None for _ in range(num_cols)] for _ in range(num_rows)]

    def update(self):
        energy_mods = 0
        dead_objs = set()
        for row in range(self.num_rows):

            for col in range(self.num_cols):
                if not self._is_empty(row, col):
                    energy_mod = self.tiles[row][col].update(self.monsters[row])

                    if energy_mod:
                        energy_mods += energy_mod

                    if self.tiles[row][col].health < 1:
                        self.tiles[row][col] = None

                if self.tile_effects[row][col]:
                    self.tile_effects[row][col].update()

                    if self.tile_effects[row][col].lifespan <= 0:
                        self.tile_effects[row][col] = None

                    

            for monster in self.monsters[row]:
                monster.update(self.tiles[row], self.TILE_COORDS[row], self.tile_effects[row])
                if monster.health < 1:
                    dead_objs.add(monster)

        for proj in self.projectiles:
            proj.update()
            if proj.elapsed >= proj.lifespan:
                dead_objs.add(proj)

        for row in self.monsters:
            row -= dead_objs

        self.projectiles -= dead_objs
        
        return energy_mods        

    def _is_empty(self, row, col):
        return self.tiles[row][col] == None

    def draw(self, screen):
        for row in self.tiles:
            for tile in row:
                if tile:
                    tile.draw(screen)

        for row in self.monsters:
            for monster in row:
                monster.draw(screen)

        for proj in self.projectiles:
            proj.draw(screen)

        for row in self.tile_effects:
            for effect in row:
                if effect:
                    effect.draw(screen)
    def _in_tile(self, pos, row, col):

        scale = 1 + 0.1 * row

        return Vector2(pos).distance_to(self.TILE_COORDS[row][col]) < TILE_RADIUS * scale

    def _deploy_unit(self, row, col, unit_type:str):
        
        scale = 1 + 0.1 * row
        
        if unit_type == 'microwave':
            self.tiles[row][col] = Microwave(self.TILE_COORDS[row][col], scale = scale)
        if unit_type == 'fridge':
            self.tiles[row][col] = Fridge(self.TILE_COORDS[row][col], self.apply_tile_effect, scale = 1.1*scale, grid_coordinate = (row, col))
        if unit_type == 'blender':
            self.tiles[row][col] = Blender(self.TILE_COORDS[row][col], self.projectiles.update, scale = scale)
        if unit_type == 'toaster':
            self.tiles[row][col] = Toaster(self.TILE_COORDS[row][col], self.projectiles.update, scale = scale)

        SFX['deploy'].play()

    def deploy_monster(self, row, monster_type:str):
        
        scale = 1 + 0.1 * row

        if monster_type == 'fortified':
            self.monsters[row].add(Monster((self.summon_x, self.TILE_COORDS[row][0][1]),
                                           scale = scale,
                                           health = 200,
                                           sprites=('fortified_monster_a',
                                                    'fortified_monster_b',
                                                    'fortified_monster_eat')
                                           )
                                  )
        if monster_type == 'explosive':
            self.monsters[row].add(ExplosiveMonster((self.summon_x, self.TILE_COORDS[row][0][1]), scale = scale, create_effect_callback = self.apply_tile_effect, row=row))
        else: 
            self.monsters[row].add(Monster((self.summon_x, self.TILE_COORDS[row][0][1]),
                                           scale = scale
                                          )
                                  )
    def on_click(self, mouse_pos):
        for row in range(len(self.tiles)):
            for unit in self.tiles[row]:
                if unit and unit.clicked(mouse_pos):
                    return unit.on_click(self.monsters[row])

    def play_card(self, card):
        for row in range(len(self.TILE_COORDS)):
            
            for col in range(len(self.TILE_COORDS[row])):
                if self._in_tile(card.pos, row, col) and self._is_empty(row, col):        
                    self._deploy_unit(row, col, card.card_type)
                    return True

        return False

    def apply_tile_effect(self, targets, effect_range, effect_type, lifespan = 60*10):
        tiles = set()
        if effect_range == 'row':
            for row in targets:
                for col in range(self.num_cols):
                    tiles.add((row,col))

        elif effect_range == 'col':
            for col in targets:
                for row in range(self.num_rows):
                    tiles.add((row,col))
        
        elif effect_range == 'tile':
            tiles = set(targets)

        if effect_type == 'ice':
            for target in tiles:
                scale = 1 + 0.1 * target[0]
                self.tile_effects[target[0]][target[1]] = IceEffect(self.TILE_COORDS[target[0]][target[1]],
                                                                    scale = scale,
                                                                    wave_start=target[1],
                                                                    lifespan=lifespan)
        if effect_type == 'explosion':
            for target in tiles:
                for row in range(target[0] - 1, target[0]+2):
                    for col in range(target[1] - 1, target[1]+2):
                        if 0 <= row < self.num_rows and 0 <= col < self.num_cols:
                            self.tiles[row][col] = None

                scale = 1 + 0.1 * target[0]
                SFX['explosion'].play()
                self.tile_effects[target[0]][target[1]] = ExplosionEffect(self.TILE_COORDS[target[0]][target[1]],
                                                                          scale = scale,
                                                                          lifespan=lifespan)
    def game_over(self):
        for row in self.monsters:
            for monster in row:
                if monster.pos[0] < 0:
                    return True
        
        return False