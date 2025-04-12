import digitalio
import board

first_input = digitalio.DigitalInOut(board.A0)
second_input = digitalio.DigitalInOut(board.A1)
third_input = digitalio.DigitalInOut(board.A2)
inputs = [third_input, second_input, first_input]

for ipt in inputs:
    ipt.direction = digitalio.Direction.INPUT
    ipt.pull = digitalio.Pull.DOWN

def get_input_values() -> list[bool]:
    return [x.value for x in inputs]

def get_input_value(values: list[bool]) -> int:
    val = 0
    for idx, value in enumerate(values):
        if value:
            val = val ^ (2 ** idx)

    return val

