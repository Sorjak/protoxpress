import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

moods = {
    'angry': 23, 
    'happy': 24, 
    'stasis': 22, 
    'idle': 27
}

for pin in moods.values():
    GPIO.setup(pin, GPIO.OUT)