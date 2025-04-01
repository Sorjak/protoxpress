import time

import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# These are the inputs that can be set on the SCORPIO microcontrollers.
# Each input specifies a scene controlling lights, sound, and smoke, which are
# sent to the microcontroller via 3 digital pins.
# I have implemented this as a boolean array for make the GPIO code easier.
actions = {
    'null': [False, False, False],      # 000 - 0
    'abort': [False, False, True],      # 001 - 1
    'test': [False, True, False],       # 010 - 2
    'init': [False, True, True],        # 011 - 3
    'happy': [True, False, False],      # 100 - 4
    'sad': [True, False, True],         # 101 - 5
    'emergency': [True, True, False],   # 110 - 6
    'photo': [True, True, True],        # 111 - 7
}

# Physical pins on the rpi that correspond to different SCORPIO microcontrollers.
mc_pin_map = {
    'vape_left':    [4, 17, 27],
    'vape_right':   [22, 23, 24],
    'lights1':      [5, 6, 13]
}

def init_board():
    for pins in mc_pin_map.values():
        for pin in pins:
            GPIO.setup(pin, GPIO.OUT)

def get_action_pin_states(action: str) -> int:
    pin_states = actions.get(action, [])
    if not pin_states:
        raise Exception(f'Invalid scene provided: {action}')
    
    return pin_states

def set_pins_to_states(pins: list[int], desired_state: list[str]):
    for i in range(len(pins)):
        to_set = GPIO.HIGH if desired_state[i] else GPIO.LOW
        GPIO.output(pins[i], to_set)

def set_action(action: str):
    pin_states = get_action_pin_states(action)

    # Set the appropriate pins using the action table
    for mc, pins in mc_pin_map.items():
        print(f'setting pins for {mc} ({pins}) to {pin_states}')
        set_pins_to_states(pins, pin_states)
        
    time.sleep(1)

    # Reset all pins
    for mc, pins in mc_pin_map.items():
        print(f'resetting pins for {mc} ({pins})')
        set_pins_to_states(pins, [False, False, False])
