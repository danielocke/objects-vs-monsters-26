import pygame
import random

from models import *
from utils import *
from fonts import FONTS, COLOURS
from audio import SFX
from grid  import Grid

class Game:
    def __init__(self):

        # pygame setup:
        pygame.init()
        # 16:9 aspect ratio
        self.width  = 16 * 50 # 800
        self.height =  9 * 50 # 450
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Objects Vs Monsters')

        self.clock = pygame.time.Clock()
        
        # loading assets:
        self.background = load_sprite('bg2', alpha = False)
        self.hud = {'energy_back' :load_sprite('hud_energy_back'),
                    'energy_front':load_sprite('hud_energy_front'),
                   }   

        self.state = 'game'

        self.MAX_ENERGY = 100
        self.energy     = 10
        self.ENERGY_COOLDOWN = 500
        self.energy_cd = self.ENERGY_COOLDOWN

        GRID_WIDTH  = 9
        GRID_HEIGHT = 5
        
        self.grid = Grid(GRID_WIDTH, GRID_HEIGHT, self.width)
    
    def main_loop(self):
        self.grid.deploy_monster(1,'fortified')
        self.grid.deploy_monster(2,'normal')
        self.grid._deploy_unit(0, 0, 'microwave')
        self.grid._deploy_unit(2, 2, 'blender')
        while True:
            self._process_input()
            self._process_game_logic()
            self._draw()
            self.clock.tick(60)

    def _process_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

    def _process_game_logic(self):
        if self.state == 'game':
            self.energy_cd -= 1

            if self.energy_cd < 1:
                self.energy += 5
                self.energy_cd = random.randint(self.ENERGY_COOLDOWN - 100, self.ENERGY_COOLDOWN + 100)
                SFX['energy_gain'].play()

            energy_mod = self.grid.update()

            self.energy += energy_mod
            
            if self.energy > self.MAX_ENERGY:
                self.energy = self.MAX_ENERGY

    def _draw(self):
        self.screen.blit(self.background,(0,0))

        self.grid.draw(self.screen)
        # Drawing HUD
        self.screen.blit(self.hud['energy_back'], (0,0))

        X_OFFSET = 7
        energy_bar = pygame.Surface(((self.energy/self.MAX_ENERGY) * (self.width - X_OFFSET),40))
        energy_bar.set_alpha(200)
        energy_bar.fill(COLOURS['purple'])
        self.screen.blit(energy_bar, (X_OFFSET, 410))

        self.screen.blit(self.hud['energy_front'], (0,0))

        write(self.screen, str(self.energy), (20, 412), FONTS['small'], COLOURS['white_purple'])

        pygame.display.update()