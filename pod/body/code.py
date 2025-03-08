import math

import pwmio
import digitalio
import time
import board
import neopixel

# On CircuitPlayground Express, and boards with built in status NeoPixel -> board.NEOPIXEL
# Otherwise choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D1
pixel_pin = board.NEOPIXEL0


first_input = digitalio.DigitalInOut(board.A0)
second_input = digitalio.DigitalInOut(board.A1)
inputs = [first_input, second_input]

for ipt in inputs:
    ipt.direction = digitalio.Direction.INPUT
    ipt.pull = digitalio.Pull.DOWN

board_pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=1.0)

color_ref = {
    0: (0, 0, 0),   # 00
    1: (0, 255, 0), # 01
    2: (0, 0, 255), # 10
    3: (255, 0, 0)  # 11
}

def get_input_values():
    return [x.value for x in inputs]

def get_color_for_input_values(values):   
    color_val = 0
    for idx, value in enumerate(values):
        if value:
            color_val = color_val ^ (2 ** idx)

    return color_ref.get(color_val)


print(f'starting loop')
loop_counter = 0
lowest_value = 65535
highest_value = 0
while True:
    board_pixel[0] = (0, 0, 0)
    values = get_input_values()
    color = get_color_for_input_values(values)
    if color != (0, 0, 0):
        print('signal detected')
        board_pixel[0] = color
        
    board_pixel.show()
    loop_counter += 1
    loop_counter = loop_counter % 1000

    if loop_counter == 0:
        print('new loop')

