import time

import click

from app.lib import GPIO, moods

@click.group()
def cli():
    pass

@cli.command()
@click.argument('mood')
def set_mood(mood):
    pin = int(moods.get(mood))
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(pin, GPIO.LOW)


if __name__ == '__main__':
    cli()