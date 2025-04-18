import time
import board

from digitalio import DigitalInOut, Direction

from nfc import NFCReader
nfc = NFCReader()

idle_out = DigitalInOut(board.A0)
idle_out.direction = Direction.OUTPUT

happy_out = DigitalInOut(board.A1)
happy_out.direction = Direction.OUTPUT

angry_out = DigitalInOut(board.A2)
angry_out.direction = Direction.OUTPUT

input_map = {
    'idle': idle_out,
    'happy': happy_out,
    'angry': angry_out
}

def send_input(data):
    output = input_map.get(data)
    if not output:
        print('unknown input')
        return

    output.value = True
    time.sleep(1)
    output.value = False

while True:
    now = time.monotonic()
    if data := nfc.scan_for_card():
        send_input(data)
