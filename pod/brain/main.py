import click

from app.lib import set_action

@click.group()
def cli():
    pass

@cli.command()
@click.argument('action')
def set_action(action):
    try:
        set_action(action)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    cli()
