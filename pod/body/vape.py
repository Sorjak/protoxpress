import math

import pwmio
import digitalio
import time
import board
import neopixel

first_input = digitalio.DigitalInOut(board.A0)
second_input = digitalio.DigitalInOut(board.A1)
third_input = digitalio.DigitalInOut(board.A2)
inputs = [first_input, second_input, third_input]

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
    "none": (0, 0, 0),   # 00
    "scene1": (0, 255, 0), # 01
    "scene2": (0, 0, 255), # 10
    "scene3": (255, 0, 0)  # 11
}

def get_input_values() -> list[bool]:
    return [x.value for x in inputs]

def get_scene_from_input_values(values: list[bool]) -> str:
    scene_val = 0
    for idx, value in enumerate(values):
        if value:
            scene_val = scene_val ^ (2 ** idx)

    return scenes.get(scene_val, "none")


print(f'starting loop')
loop_counter = 0
scene = 'none'
while True:
    board_pixel[0] = (0, 0, 0)
    values = get_input_values()
    if any(values):
        print(values)

    scene = get_scene_from_input_values(values)
    
    if scene != 'none':
        print(f'changing to scene {scene}')
        color = color_ref.get(scene)
        board_pixel[0] = color
        
    board_pixel.show()
    loop_counter += 1
    loop_counter = loop_counter % 1000

    if loop_counter == 0:
        print(f'new loop, current scene: {scene}')

