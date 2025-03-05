import time

import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

scenes = {
    'angry': 23, 
    'happy': 24, 
    'stasis': 22, 
    'idle': 27
}

def init_board():
    for pin in scenes.values():
        GPIO.setup(pin, GPIO.OUT)


def set_scene(scene):
    scene_pin = int(scenes.get(scene, -1))
    if scene_pin < 0:
        raise Exception(f'Invalid scene provided: {scene}')

    GPIO.output(scene_pin, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(scene_pin, GPIO.LOW)
