import math

import pwmio
import digitalio
import time
import board
import neopixel

first_input = digitalio.DigitalInOut(board.A0)
second_input = digitalio.DigitalInOut(board.A1)
third_input = digitalio.DigitalInOut(board.A2)
inputs = [third_input, second_input, first_input]

# Vapes should be connected as follows:
# - All inside vapes on the first three pins
# - All outside vapes on the next three pins
vape_0 = pwmio.PWMOut(board.NEOPIXEL0) # I1
vape_1 = pwmio.PWMOut(board.NEOPIXEL1) # I2
vape_2 = pwmio.PWMOut(board.NEOPIXEL2) # I3
vape_3 = pwmio.PWMOut(board.NEOPIXEL3) # O1
vape_4 = pwmio.PWMOut(board.NEOPIXEL4) # O2
vape_5 = pwmio.PWMOut(board.NEOPIXEL5) # O3
all_vapes = [vape_0, vape_1, vape_2, vape_3, vape_4, vape_5]
inside_vapes = [vape_0, vape_1, vape_2]
outside_vapes = [vape_3, vape_4, vape_5]

for ipt in inputs:
    ipt.direction = digitalio.Direction.INPUT
    ipt.pull = digitalio.Pull.DOWN

board_pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=1.0)

max_vape_power = 2**16 - 1

scenes = {
    0: "none",
    1: "abort",
    2: "test",
    3: "init",
    4: "happy",
    5: "sad",
    6: "emergency",
    7: "photo"
}

color_ref = {
    "none":   (0, 0, 0),        # 000
    "abort": (0, 0, 255),      # 001
    "test": (0, 255, 0),      # 010
    "init": (0, 255, 255),    # 011
    "happy": (255, 0, 0),      # 100
    "sad": (255, 0, 255),    # 101
    "emergency": (255, 255, 0),    # 110
    "photo": (255, 255, 255)   # 111
}

vape_scenes = {
    'test': {
        'duration': 1200,
        'in': [
            {'s': 0, 'e': 200},
            {'s': 600, 'e': 800},
        ],
        'out': [
            {'s': 300, 'e': 500},
            {'s': 900, 'e': 1100},
        ],
    },
    'init': {
        'duration': 1100,
        'in': [
            {'s': 0, 'e': 1000},
        ],
        'out': [],     
    }
}

def get_input_values() -> list[bool]:
    return [x.value for x in inputs]

def get_input_value(values: list[bool]) -> int:
    val = 0
    for idx, value in enumerate(values):
        if value:
            val = val ^ (2 ** idx)

    return val

def should_be_on(list_of_configs, counter):
    should_it = False
    for item in list_of_configs:
        start = item.get('s')
        end = item.get('e')
        if counter >= start and counter <= end:
            should_it = True
            break

    return should_it

def handle_vapes(config, counter):
    duration = config.get('duration') or 0
    inside_config = config.get('in', [])
    outside_config = config.get('out', [])

    in_is_on = should_be_on(inside_config, counter)
    for v in inside_vapes:
        if in_is_on:
            print(f'turning inside vapes on {counter} / {duration}')
            turn_vape_on(v)
        else:
            turn_vape_off(v)

    out_is_on = should_be_on(outside_config, counter)
    for v in outside_vapes:
        if out_is_on:
            print(f'turning outside vapes on {counter} / {duration}')
            turn_vape_on(v)
        else:
            turn_vape_off(v)

    counter += 1
    if counter > duration:
        counter = 0

    return counter

def turn_vape_on(vape):
    vape.duty_cycle = max_vape_power

def turn_vape_off(vape):
    vape.duty_cycle = 0

print(f'starting vape program')
vape_counter = 0
scene = 'none'
old_scene = 'none'
while True:
    board_pixel[0] = (0, 0, 0)
    values = get_input_values()
    if any(values):
        input_val = get_input_value(values)

        scene = scenes.get(input_val)
        print(f'changing to scene {scene}')

        color = color_ref.get(scene)
        board_pixel[0] = color
        old_scene = scene
        
    board_pixel.show()

    if scene != 'none':
        scene_config = vape_scenes.get(scene) or {}
        vape_counter = handle_vapes(scene_config, vape_counter)
        if vape_counter <= 0:
            vape_counter = 0
            scene = 'none'


