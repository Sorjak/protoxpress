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

for ipt in inputs:
    ipt.direction = digitalio.Direction.INPUT
    ipt.pull = digitalio.Pull.DOWN

board_pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=1.0)

scenes = {
    0: "none",
    1: "scene1",
    2: "scene2",
    3: "scene3",
    4: "scene4",
    5: "scene5",
    6: "scene6",
    7: "scene7"
}

color_ref = {
    "none":   (0, 0, 0),        # 000
    "scene1": (0, 0, 255),      # 001
    "scene2": (0, 255, 0),      # 010
    "scene3": (0, 255, 255),    # 011
    "scene4": (255, 0, 0),      # 100
    "scene5": (255, 0, 255),    # 101
    "scene6": (255, 255, 0),    # 110
    "scene7": (255, 255, 255)   # 111
}

def get_input_values() -> list[bool]:
    return [x.value for x in inputs]

def get_input_value(values: list[bool]) -> int:
    val = 0
    for idx, value in enumerate(values):
        if value:
            val = val ^ (2 ** idx)

    return val


print(f'starting vape program')
loop_counter = 0
scene = 'none'
old_scene = 'none'
while True:
    board_pixel[0] = (0, 0, 0)
    values = get_input_values()
    if any(values):
        input_val = get_input_value(values)
        print(f'Values {values} -> decimal {input_val}')

        scene = scenes.get(input_val)
        print(f'changing to scene {scene}')

        color = color_ref.get(scene)
        board_pixel[0] = color
        old_scene = scene
        
    board_pixel.show()
    loop_counter += 1
    loop_counter = loop_counter % 1000

    if loop_counter == 0:
        print(f'new loop, last scene was: {old_scene}')
