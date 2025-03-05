import time

import click

from app.lib import GPIO, set_scene

@click.group()
def cli():
    pass

@cli.command()
@click.argument('mood')
def set_mood(mood):
    try:
        set_scene(mood)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    cli()
