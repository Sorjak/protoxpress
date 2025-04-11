import math

import pwmio
import digitalio
import time
import board
import neopixel

from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle

from adafruit_led_animation.group import AnimationGroup
from adafruit_led_animation import color

from rainbowio import colorwheel

first_input = digitalio.DigitalInOut(board.A0)
second_input = digitalio.DigitalInOut(board.A1)
third_input = digitalio.DigitalInOut(board.A2)
inputs = [third_input, second_input, first_input]

for ipt in inputs:
    ipt.direction = digitalio.Direction.INPUT
    ipt.pull = digitalio.Pull.DOWN

board_pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=1.0)

num_pixels = 320 * 1
strand0 = neopixel.NeoPixel(board.NEOPIXEL0, num_pixels, brightness=1.0)
strand1 = neopixel.NeoPixel(board.NEOPIXEL1, num_pixels * 2, brightness=1.0)
strand2 = neopixel.NeoPixel(board.NEOPIXEL2, num_pixels * 2, brightness=0.8)


all_strands = [strand0, strand1, strand2]

ag = AnimationGroup(
    Comet(strand0, speed=0.005, color=color.PURPLE, tail_length=20, bounce=True),
    Comet(strand1, speed=0.005, color=color.BLUE, tail_length=20, bounce=True),
    # Comet(strand2, speed=0.005, color=color.GREEN, tail_length=20, bounce=True)
    RainbowSparkle(strand2, speed=0.1, num_sparkles=15)
    # Solid(strand2, color=color.WHITE)
)


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

def set_pixels(color):
    print(f'setting strand to {color}')
    for strand in all_strands:
        strand.fill(color)
        strand.show()


print(f'starting lights program')
loop_counter = 0
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
        set_pixels(color)
        old_scene = scene

    board_pixel.show()

    loop_counter += 1
    loop_counter = loop_counter % 1000

    if loop_counter == 0:
        print(f'new loop, last scene was: {old_scene}')

    ag.animate()
