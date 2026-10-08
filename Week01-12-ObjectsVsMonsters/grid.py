from models import *
from pygame.math import Vector2

TILE_RADIUS = 25

class Grid:
    def __init__(self, num_rows, num_cols, summon_x):
        self.tiles = [[None for _ in range(num_cols)] for _ in range(num_rows)]

        self.TILE_COORDS = [[(118 + 70*i,105) for i in range(num_cols)],
                            [(102 + 74*i,160) for i in range(num_cols)],
                            [(86  + 78*i,220) for i in range(num_cols)],
                            [(68  + 83*i,285) for i in range(num_cols)],
                            [(52  + 87*i,355) for i in range(num_cols)]
                            ]

        self.monsters = [set() for _ in range(num_rows)]

        self.num_rows = num_rows
        self.num_cols = num_cols

        self.summon_x = summon_x

    def update(self):
        energy_mods = 0
        dead_monsters = set()

        for row in range(self.num_rows):

            for col in range(self.num_cols):
                if not self._is_empty(row, col):
                    energy_mod = self.tiles[row][col].update(self.monsters[row])

                    if energy_mod:
                        energy_mods += energy_mod

                    if self.tiles[row][col].health < 1:
                        self.tiles[row][col] = None

            for monster in self.monsters[row]:
                monster.update(self.tiles[row], self.TILE_COORDS[row])
                if monster.health < 1:
                    dead_monsters.add(monster)

        for row in self.monsters:
            row -= dead_monsters

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

    def _in_tile(self, pos, row, col):

        scale = 1 + 0.1 * row

        return Vector2(pos).distance_to(self.TILE_COORDS[row][col]) < TILE_RADIUS * scale

    def _deploy_unit(self, row, col, unit_type:str):
        
        scale = 1 + 0.1 * row
        
        if unit_type == 'microwave':
            self.tiles[row][col] = Unit(self.TILE_COORDS[row][col], 'microwave', scale = scale)
        if unit_type == 'blender':
                self.tiles[row][col] = Unit(self.TILE_COORDS[row][col], 'blender', scale = scale)
        if unit_type == 'toaster':
                self.tiles[row][col] = Unit(self.TILE_COORDS[row][col], 'toaster', scale = scale)

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
        else: 
            self.monsters[row].add(Monster((self.summon_x, self.TILE_COORDS[row][0][1]),
                                           scale = scale
                                          )
                                  )