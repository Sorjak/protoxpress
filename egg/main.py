import math

import pwmio
import time
import board
import neopixel
import digitalio


# On CircuitPlayground Express, and boards with built in status NeoPixel -> board.NEOPIXEL
# Otherwise choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D1
pixel_pin = board.NEOPIXEL0

vape_pin_1 = board.NEOPIXEL1
vape_pin_2 = board.NEOPIXEL2
vape_pin_3 = board.NEOPIXEL3
vape_pin_4 = board.NEOPIXEL4
vape_pin_5 = board.NEOPIXEL5
vape_pin_6 = board.NEOPIXEL6
vape_pin_7 = board.NEOPIXEL7

input_pin_0 = board.A0
input_pin_1 = board.A1
input_pin_2 = board.A2
input_pin_3 = board.A3


stasis_input = digitalio.DigitalInOut(input_pin_0)
stasis_input.direction = digitalio.Direction.INPUT
stasis_input.pull = digitalio.Pull.DOWN

idle_input = digitalio.DigitalInOut(input_pin_1)
idle_input.direction = digitalio.Direction.INPUT
idle_input.pull = digitalio.Pull.DOWN

angry_input = digitalio.DigitalInOut(input_pin_2)
angry_input.direction = digitalio.Direction.INPUT
angry_input.pull = digitalio.Pull.DOWN

happy_input = digitalio.DigitalInOut(input_pin_3)
happy_input.direction = digitalio.Direction.INPUT
happy_input.pull = digitalio.Pull.DOWN


all_inputs = [stasis_input, idle_input, angry_input, happy_input]

# The number of NeoPixels
num_pixels = 72

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB
BLACK = (0, 0, 0)

board_pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=1.0)

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)

vape_1 = pwmio.PWMOut(vape_pin_1)
vape_2 = pwmio.PWMOut(vape_pin_2)
vape_3 = pwmio.PWMOut(vape_pin_3)
# vape_4 = pwmio.PWMOut(vape_pin_4)
# vape_5 = pwmio.PWMOut(vape_pin_5)
# vape_6 = pwmio.PWMOut(vape_pin_6)
# vape_7 = pwmio.PWMOut(vape_pin_7)

vapes = [vape_1, vape_2, vape_3] #, vape_4, vape_5, vape_6, vape_7]

max_vape_power = 2**16 - 1

last_vape_toggle_time = time.time()
vape_counter = 0

last_heartbeat = time.time()
hb_counter = 0
second_beat = False

# heartbeat data
hb_stasis_data = {
    'color': (0.01, 0.01, 0.9),
    'counter_start': 300,
    'second_beat_start': 100,
    'second_beat_end': 105,
    'drop_rate': 1.2,
    'beat_interval': 30, # seconds
    'last_heartbeat': time.time()
}

hb_idle_data = {
    'color': (0.02, 0.9, 0.02),
    'counter_start': 300, 
    'second_beat_start': 120,
    'second_beat_end': 130,
    'drop_rate': 3,
    'beat_interval': 6, # seconds
    'last_heartbeat': time.time()
}

hb_angry_data = {
    'color': (0.9, 0.02, 0.02),
    'counter_start': 100,
    'second_beat_start': 60,
    'second_beat_end': 65,
    'drop_rate': 1,
    'beat_interval': 0.8, # seconds
    'last_heartbeat': time.time()
}

hb_happy_data = {}

heartbeat_data_map = {
    'stasis': hb_stasis_data,
    'idle': hb_idle_data,
    'angry': hb_angry_data,
    'happy': hb_happy_data, 
}

# vape data
vape_stasis_data = {}
vape_idle_data = {
    'total_time': 10000,
    'rate': 1,
    'vape_1_start': 50,
    'vape_1_end': 150,
    'vape_2_start': 2000,
    'vape_2_end': 2100,
    'vape_3_start': 7050,
    'vape_3_end': 7150
}
vape_angry_data = {
    'total_time': 500,
    'rate': 1,
    'vape_1_start': 50,
    'vape_1_end': 150,
    'vape_2_start': 150,
    'vape_2_end': 250,
    'vape_3_start': 250,
    'vape_3_end': 350
}
vape_happy_data = {
    'total_time': 1000,
    'rate': 1,
    'vape_1_start': 50,
    'vape_1_end': 200,
    'vape_2_start': 50,
    'vape_2_end': 200,
    'vape_3_start': 50,
    'vape_3_end': 200
}

vape_data_map = {
    'stasis': vape_stasis_data,
    'idle': vape_idle_data,
    'angry': vape_angry_data,
    'happy': vape_happy_data, 
}

def set_pixels_color(color):
    for i in range(num_pixels):
        pixels[i] = color
    pixels.show()

def set_board_pixel_color(color):
    board_pixel[0] = color
    board_pixel.show()


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


def rainbow_cycle(interval, wait):
    interval = interval % 255

    for i in range(num_pixels):
        pixel_index = (i * 256 // num_pixels) + interval
        pixels[i] = wheel(pixel_index & 255)
    pixels.show()

    set_board_pixel_color(wheel(interval))

def heartbeat_cycle(t, second_beat, data):
    color = data.get('color')
    counter_start = data.get('counter_start')
    sb_start = data.get('second_beat_start')
    sb_end = data.get('second_beat_end')
    rate = data.get('drop_rate')

    if t > sb_start and t < sb_end and not second_beat:
        t = counter_start
        second_beat = True

    intensity = t / counter_start

    if color == 'rainbow':
        set_color = wheel(t)
    else:
        set_color = tuple([x * (intensity * 255) for x in color])

    set_pixels_color(set_color)
    set_board_pixel_color(set_color)

    return t - rate, second_beat

def set_all_vape_power(power):
    for vape in vapes:
        vape.duty_cycle = int(power)


def get_mode_from_inputs(start_mode):
    mode = start_mode
    if stasis_input.value:
        mode = 'stasis'
    elif idle_input.value:
        mode = 'idle'
    elif angry_input.value:
        mode = 'angry'
    elif happy_input.value:
        mode = 'happy'

    
    return mode

def handle_heartbeat(data, hb_counter, second_beat):
    if not data:
        return 0, False

    now = time.time()
    interval = data.get('beat_interval')
    counter_start = data.get('counter_start')
    last_heartbeat = data.get('last_heartbeat')

    if (now - last_heartbeat > interval):
        data['last_heartbeat'] = now
        hb_counter = counter_start
        second_beat = False

    return heartbeat_cycle(hb_counter, second_beat, data)


def handle_vapes(data, vape_counter):
    total_time = data.get('total_time', 500)
    rate = data.get('rate', 1)
    one_data = (data.get('vape_1_start'), data.get('vape_1_end'), vape_1)
    two_data = (data.get('vape_2_start'), data.get('vape_2_end'), vape_2)
    three_data = (data.get('vape_3_start'), data.get('vape_3_end'), vape_3)

    vape_list = [one_data, two_data, three_data]
    for i in range(3):
        start, end, vape = vape_list[i]
        if not start or not end:
            continue

        power = 0
        if vape_counter > start and vape_counter < end:
            power = max_vape_power

        vape.duty_cycle = power

        if power > 0:
            print(f'vape {i + 1} is running')

    return (vape_counter + rate) % total_time

def happy_mode_special(dt):
    rainbow_cycle(dt, 0.001)


old_mode = 'stasis'
loop_counter = 0
while True:
    now = time.time()
    mode = get_mode_from_inputs(old_mode)

    # If this is a mode transition, clear lights and vapes
    if mode != old_mode:
        print(f'setting mode to {mode}')
        set_pixels_color(BLACK)
        set_board_pixel_color(BLACK)
        set_all_vape_power(0)
        hb_counter = 0
        vape_counter = 0

    
    hb_data = heartbeat_data_map.get(mode)
    hb_counter, second_beat = handle_heartbeat(hb_data, hb_counter, second_beat)

    vape_data = vape_data_map.get(mode)
    vape_counter = handle_vapes(vape_data, vape_counter)


    # run special modes:
    if mode == 'happy':
        happy_mode_special(loop_counter)

    loop_counter = (loop_counter + 1) % 1000
    old_mode = mode
