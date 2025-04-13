import time
import board
import neopixel

from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.sparklepulse import SparklePulse
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.sparkle import Sparkle
from adafruit_led_animation.animation.rainbowchase import RainbowChase
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.animation.colorcycle import ColorCycle
from adafruit_led_animation.animation.rainbow import Rainbow

from adafruit_led_animation.sequence import AnimationSequence
from adafruit_led_animation.group import AnimationGroup
from adafruit_led_animation import color

from scenes import BaseController

PIXELS_PER_STRAND = 320

class LightController(BaseController):
    name = 'LightController'

    all_strands = []
    config = {}
    scene_start = 0
    max_duration = 0

    def __init__(self):
        left = neopixel.NeoPixel(board.NEOPIXEL0, PIXELS_PER_STRAND, brightness=0.8)
        right = neopixel.NeoPixel(board.NEOPIXEL1, PIXELS_PER_STRAND, brightness=0.8)
        photo = neopixel.NeoPixel(board.NEOPIXEL2, PIXELS_PER_STRAND * 2, brightness=0.8)

        self.all_strands = [left, right, photo]
        self.config = {
            'abort': {'duration': 1},
            'test': {
                'duration': 10, # seconds should this animation run for?
                'animation': AnimationGroup (
                    Comet(left, speed=0.001, color=color.PURPLE, tail_length=20, bounce=True),
                    Comet(right, speed=0.001, color=color.BLUE, tail_length=20, bounce=True),
                    RainbowSparkle(photo, speed=0.1, num_sparkles=15)
                ),
            },
            'init': {
                'duration': 15, 
                'animation': AnimationGroup (
                    RainbowComet(left, speed=0.001, tail_length=300, reverse=False),
                    RainbowComet(right, speed=0.001, tail_length=300, reverse=False),
                    Blink(photo, speed=0.01, color=color.GREEN)
                ),
            },
            'happy': {
                'duration': 30, 
                'animation': AnimationGroup (
                    RainbowChase(left, speed=0.01, size=100, spacing=30, reverse=False),
                    RainbowChase(right, speed=0.01, size=100, spacing=30, reverse=False),
                    RainbowSparkle(photo, speed=0.01, num_sparkles=15)
                ),
            },
            'sad': {
                'duration': 15,
                'animation': AnimationGroup (
                    RainbowChase(left, speed=0.01, size=100, spacing=30, reverse=True),
                    RainbowChase(right, speed=0.01, size=100, spacing=30, reverse=True),
                    Pulse(photo, speed=0.01, color=color.RED),
                ),
            },
            'emergency': {
                'duration': 15,
                'animation': AnimationGroup (
                    Blink(left, speed=0.001, color=color.RED),
                    Blink(right, speed=0.001, color=color.RED),
                    Pulse(photo, speed=0.001, color=color.RED),
                ),
            },
            'photo': {
                'duration': -1, 
                'animation': RainbowSparkle(photo, speed=0.1, num_sparkles=15)
            },
        }

    def set_pixels(self, new_color: tuple):
        for strand in self.all_strands:
            strand.fill(new_color)
            strand.show()

    def init_scene(self):
        super().init_scene()

        self.scene_start = time.monotonic()
        print(f'Starting scene {self.current_scene} at {self.scene_start}')

    def exit_scene(self):
        super().exit_scene()

        self.set_pixels(color.BLACK)
        print(f'Exiting scene {self.current_scene} at {self.scene_start}')
    
    def update(self):
        if not self.current_config:
            return

        if animation := self.current_config.get('animation'):
            animation.animate()

    def post_update(self):
        if not self.current_config:
            return

        now = time.monotonic()
        if self.scene_start + self.scene_duration < now:
            print(f'Exiting scene {self.current_scene} at {now}')
            self.exit_scene()

