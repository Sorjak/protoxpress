import time

import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

scenes = {
    'angry': 22, 
    'happy': 27, 
    'stasis': 17, 
    'idle': 4
}

def init_board():
    for pin in scenes.values():
        GPIO.setup(pin, GPIO.OUT)

def get_scene_pin(scene: str) -> int:
    scene_pin = int(scenes.get(scene, -1))
    if scene_pin < 0:
        raise Exception(f'Invalid scene provided: {scene}')
    
    return scene_pin

def set_scene(scene: str):
    scene_pin = get_scene_pin(scene)
    GPIO.output(scene_pin, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(scene_pin, GPIO.LOW)

def set_scenes(scenes: list[str]):
    pins = []
    for scene in scenes:
        pins.append(get_scene_pin(scene))

    for pin in pins:
        GPIO.output(pin, GPIO.HIGH)
    
    time.sleep(1)

    for pin in pins:
        GPIO.output(pin, GPIO.LOW)
