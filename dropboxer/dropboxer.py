import click

import handler

@click.group()
def cli():
    '''
    drp is a DropBoxer command.
    DropBoxer is a command line tool for Dropbox to ease upload, download of files and get public URLs.
    '''
    pass

@cli.command()
def up():
    pass

@cli.command()
def down():
    pass

@cli.command()
def ls():
    pass

@cli.command()
def tree():
    pass

@cli.command()
def cd():
    pass

@cli.command()
def mkdir():
    pass

@cli.command()
def rmdir():
    pass

@cli.command()
def rm():
    pass

@cli.command()
def share():
    pass

@cli.command()
def info():
    pass
