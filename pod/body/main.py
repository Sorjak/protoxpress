import board
import neopixel

from inputs import get_input_values, get_input_value
from scenes import get_scene_from_input, get_scene_color

# In order for imports to work correctly, the microcontroller should
# have these three files in the lib directory:
# inputs.py
# scenes.py
# either vape.py or light.py

# Get the library for this controller, 
# uncomment or comment as needed per board

# from light import LightController as Ctrl
from vape import VapeController as Ctrl

# Instantiate controller
ctrl = Ctrl()

# Setup pins
board_pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=1.0)


# Main loop begin
print(f'starting {ctrl.name}')
scene = 'none'
while True:
    board_pixel[0] = (0, 0, 0)

    # Poll the inputs for any changes
    values = get_input_values()
    
    # If changes were detected, try to change the scene
    if any(values):
        try:
            input_val = get_input_value(values)
            scene = get_scene_from_input(input_val)

            ctrl.set_scene(scene)

            # Debug inputs by changing the board pixel color
            color = get_scene_color(scene)
            board_pixel[0] = color
        except Exception as e:
            print(e)
            continue
        
    board_pixel.show()

    # Call more specific code to actually run the scene
    ctrl.update()
    ctrl.post_update()
