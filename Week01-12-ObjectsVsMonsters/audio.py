import pygame.mixer as mixer
import os.path as path

mixer.init()

SFX_PATH = path.join(path.dirname(__file__),'assets','sfx')

SFX = {'microwave'   : mixer.Sound(path.join(SFX_PATH, 'microwave.mp3')),
       'toaster'     : mixer.Sound(path.join(SFX_PATH, 'toaster.mp3')),
       'blender'     : mixer.Sound(path.join(SFX_PATH, 'blender.mp3')),
       'error'       : mixer.Sound(path.join(SFX_PATH, 'error.mp3')),
       'energy_gain' : mixer.Sound(path.join(SFX_PATH, 'energy_gain.mp3')),
       'deploy'      : mixer.Sound(path.join(SFX_PATH, 'deploy.mp3')),
       'chomp'       : mixer.Sound(path.join(SFX_PATH, 'chomp.mp3')),
       'growl'       : mixer.Sound(path.join(SFX_PATH, 'growl.mp3')),
       'impact'      : mixer.Sound(path.join(SFX_PATH, 'impact.mp3')),
       'freeze'      : mixer.Sound(path.join(SFX_PATH, 'freeze.mp3')),
       'explosion'   : mixer.Sound(path.join(SFX_PATH, 'explosion.mp3')),
      }

SFX['toaster'].set_volume(0.10)
SFX['blender'].set_volume(0.10)
SFX['energy_gain'].set_volume(0.25)
SFX['deploy'].set_volume(0.1)
SFX['growl'].set_volume(0.25)

mixer.music.load(path.join(SFX_PATH,'music.mp3'))