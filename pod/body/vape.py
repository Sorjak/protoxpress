import math
import time

import pwmio
import board

from scenes import BaseController

MAX_POWER = 2**16 - 1

class VapeController(BaseController):
    name = 'VapeController'

    all_vapes = []
    inside_vapes = []
    outside_vapes = []
    scene_counter = 0
    max_duration = 0

    config = {
        'abort': {
            'duration': 100,
        },
        'test': {
            'duration': 1200, # how many loops should this scene last?
            'in': [
                {'s': 0, 'e': 200}, # At what points in the above duration should this vape be on?
                {'s': 600, 'e': 800},
            ],
            'out': [
                {'s': 300, 'e': 500}, # same as above, but only for outer vapes
                {'s': 900, 'e': 1100},
            ],
        },
        'init': {
            'duration': 1100,
            'in': [
                {'s': 0, 'e': 400},
                {'s': 600, 'e': 1000},
            ],
            'out': [],
        },
        'happy': {
            'duration': 1200,
            'in': [],
            'out': [
                {'s': 300, 'e': 500},
                {'s': 900, 'e': 1100},
            ],
        },
        'sad': {
            'duration': 1200,
            'in': [],
            'out': [
                {'s': 300, 'e': 500},
                {'s': 900, 'e': 1100},
            ],
        },
        'emergency': {
            'duration': 1200,
            'in': [],
            'out': [
                {'s': 300, 'e': 500},
                {'s': 900, 'e': 1100},
            ],
        },
        'photo': {},
    }

    def __init__(self):
        """ Setup hardware pins, map them to variables.
        
            Vapes should be connected as follows:
                - All inside vapes on the first three pins
                - All outside vapes on the next three pins
        """
        vape_0 = pwmio.PWMOut(board.NEOPIXEL0) # I1
        vape_1 = pwmio.PWMOut(board.NEOPIXEL1) # I2
        vape_2 = pwmio.PWMOut(board.NEOPIXEL2) # I3
        vape_3 = pwmio.PWMOut(board.NEOPIXEL3) # O1
        vape_4 = pwmio.PWMOut(board.NEOPIXEL4) # O2
        vape_5 = pwmio.PWMOut(board.NEOPIXEL5) # O3

        self.all_vapes = [vape_0, vape_1, vape_2, vape_3, vape_4, vape_5]
        self.inside_vapes = [vape_0, vape_1, vape_2]
        self.outside_vapes = [vape_3, vape_4, vape_5]

    def should_be_on(self, list_of_configs):
        """ Look at the list of start and end objects,
            and determine if the running counter lies between
            them. If so, return true
        """
        should_it = False
        for item in list_of_configs:
            start = item.get('s')
            end = item.get('e')
            if self.scene_counter >= start and self.scene_counter <= end:
                should_it = True
                break

        return should_it

    def toggle_vapes_in_scene(self, config):
        """ Toggle each of the inside and outside vapes
            depending on the provided config, which describes a scene.
        """
        inside_config = config.get('in', [])
        outside_config = config.get('out', [])

        in_is_on = self.should_be_on(inside_config)
        for vape in self.inside_vapes:
            vape.duty_cycle = MAX_POWER if in_is_on else 0

        out_is_on = self.should_be_on(outside_config)
        for vape in self.outside_vapes:
            vape.duty_cycle = MAX_POWER if out_is_on else 0

    def reset_all_vapes(self):
        # Turn off all vapes
        for vape in self.all_vapes:
            vape.duty_cycle = 0

    def init_scene(self):
        print(f'Starting scene {self.current_scene}')
        super().init_scene()

        self.scene_counter = 0
        
    def exit_scene(self):
        print(f'Exiting scene {self.current_scene}')
        super().exit_scene()

        # Clean up after previous scene
        self.reset_all_vapes()
        
    # entry point from main
    def update(self):
        if not self.current_config:
            return

        self.toggle_vapes_in_scene(self.current_config)

    def post_update(self):
        if not self.current_config:
            return

        if self.scene_duration == -1:
            return

        self.scene_counter += 1
        if self.scene_counter > self.scene_duration:
            self.exit_scene()

