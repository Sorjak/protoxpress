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

vape_0 = pwmio.PWMOut(board.NEOPIXEL0)
vape_1 = pwmio.PWMOut(board.NEOPIXEL1)
vape_2 = pwmio.PWMOut(board.NEOPIXEL2)
vape_3 = pwmio.PWMOut(board.NEOPIXEL3)
vape_4 = pwmio.PWMOut(board.NEOPIXEL4)
vape_5 = pwmio.PWMOut(board.NEOPIXEL5)
all_vapes = [vape_0, vape_1, vape_2, vape_3, vape_4, vape_5]

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

def get_input_values() -> list[bool]:
    return [x.value for x in inputs]

def get_input_value(values: list[bool]) -> int:
    val = 0
    for idx, value in enumerate(values):
        if value:
            val = val ^ (2 ** idx)

    return val


def handle_vapes(scene, counter):
    for v in all_vapes:
        if counter < 500:
            turn_vape_on(v)
        else:
            turn_vape_off(v)

def turn_vape_on(vape):
    vape.duty_cycle = max_vape_power

def turn_vape_off(vape):
    vape.duty_cycle = 0

print(f'starting vape program')
loop_counter = 0
vape_counter = 0
scene = 'none'
old_scene = 'none'
while True:
    board_pixel[0] = (0, 0, 0)
    values = get_input_values()
    if any(values):
        input_val = get_input_value(values)
        # print(f'Values {values} -> decimal {input_val}')

        scene = scenes.get(input_val)
        print(f'changing to scene {scene}')

        color = color_ref.get(scene)
        board_pixel[0] = color
        old_scene = scene
        
    board_pixel.show()
    loop_counter += 1
    loop_counter = loop_counter % 1000

    if scene != 'none':
        handle_vapes(scene, loop_counter)

    if loop_counter == 0:
        print(f'new loop, last scene was: {old_scene}')
