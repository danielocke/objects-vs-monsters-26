import random
from audio import SFX

class Wave:
    def __init__(self, summon_points:int, monster_types:dict, min_cd:int, max_cd:int, guaranteed_monsters):
        self.summon_points = summon_points
        self.monster_types = monster_types
        self.MIN_CD = min_cd
        self.MAX_CD = max_cd
        self.deploy_cd = random.randint(self.MIN_CD, self.MAX_CD)

        self.monsters = list(guaranteed_monsters)

        self._generate_wave()

    def _generate_wave(self):

        options = list(self.monster_types.keys())

        while self.summon_points > 0:
            sel = random.choice(options)
            if self.monster_types[sel] <= self.summon_points:
                self.monsters.append(sel)
                self.summon_points -= self.monster_types[sel]

        random.shuffle(self.monsters)

    def update(self, grid) -> bool:
        if len(self.monsters) == 0:
            return True

        if self.deploy_cd < 1:
            self._deploy(grid)
            self.deploy_cd = random.randint(self.MIN_CD, self.MAX_CD)
        else:
            self.deploy_cd -= 1

        return False

    def _deploy(self, grid):
        row = random.randint(0, grid.num_rows - 1)
        monster = self.monsters.pop()
        
        grid.deploy_monster(row, monster)

        SFX['growl'].play()

class Level:
    def __init__(self, waves, initial_cd):
        self.waves = waves[1:]
        self.cur_wave = waves[0]
        self.initial_cd = initial_cd
        self.wave_complete = False
        self.level_complete = False

        