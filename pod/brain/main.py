import time

import click

from app.lib import set_scene, set_scenes

@click.group()
def cli():
    pass

@cli.command()
@click.argument('scene')
def set_scene(scene):
    try:
        set_scene(scene)
    except Exception as e:
        print(e)


@cli.command()
@click.argument('scenes', nargs=-1)
def set_scenes(scenes):
    print(f'Setting scenes: {scenes}')
    try:
        set_scenes(scenes)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    cli()
