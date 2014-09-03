#!/usr/bin/env python
# Encoding: utf-8

import pprint
import os

import click
from click import echo
from handler import DrpHandler


@click.group()
def cli():
    '''drp is a command line tool for Dropbox to ease upload,
    download of files and get public URLs.
    '''
    pass


@cli.command()
def init():
    '''Initialize drp by getting Dropbox access token'''

    handler = DrpHandler(forceinit=True)


@cli.command()
@click.option('--path', '-p', default='/', type=click.Path(),
              help='Path where files will be uploaded')
@click.argument('files', nargs=-1)
def up(path, files):
    '''Recursively upload files/folders to "path" or drp App folder'''

    files = [os.path.abspath(x) for x in files]
    handler = DrpHandler()
    failed_files = handler.up(path, files)
    for name, err in failed_files:
        echo('Failed to upload %s | Error: %s' % (name, err))


@cli.command()
@click.option('--path', '-p', default='.',
              type=click.Path(exists=True, resolve_path=True),
              help='Path where files will be downloaded')
@click.argument('files', nargs=-1)
def down(path, files):
    '''Recursively download files/folders to "path" or current directory'''

    handler = DrpHandler()
    failed_files = handler.down(path, files)

    for name, err in failed_files:
        echo('Failed to download %s | Error: %s' % (name, err))


@cli.command()
@click.argument('path', nargs=1, type=click.Path(),
                default='/', required=False)
def ls(path):
    '''List files/folders in the "path" or current directory'''

    handler = DrpHandler()
    files, folders = handler.ls(path)
    if folders:
        echo('Folders:')
        echo('\t'.join(folders))
    if files:
        echo('Files:')
        echo('\t'.join(files))


@cli.command()
@click.argument('path', nargs=1, type=click.Path(),
                default='/', required=False)
def tree(path):
    '''Show file structure of "path" or current directory'''

    echo('Show tree of %s' % path)


@cli.command()
@click.argument('path', nargs=1, type=click.Path(), required=True)
def mkdir(path):
    '''Make a new directories under given path'''

    handler = DrpHandler()
    status = handler.mkdir(path)
    if not status[0]:
        echo(status[1])


@cli.command()
@click.argument('path', nargs=-1, type=click.Path(), required=True)
def rm(path):
    '''Remove files or an empty directories under given path'''

    handler = DrpHandler()
    failed_paths = handler.rm(path)
    for path, err in failed_paths:
        echo('Failed to delete %s | Error: %s' % (path, err))


@cli.command()
@click.argument('path', nargs=1, type=click.Path(), required=True)
def share(path):
    '''Copy the public URL of the file to Clipboard'''

    handler = DrpHandler()
    response = handler.share(path)
    if response:
        echo('Public URL: %s' % (response['url'],))


@cli.command()
@click.argument('path', nargs=1, type=click.Path(), required=True)
def info(path):
    '''Retrieve metadata for file/folder'''

    handler = DrpHandler()
    info = handler.info(path)
    if info[0]:
        pp = pprint.PrettyPrinter(indent=2)
        echo(pp.pprint(info[1]))


@cli.command()
@click.option('--path', '-p', default='/', type=click.Path(),
              help='The path to search within')
@click.argument('query', nargs=1, required=True)
def search(path, query):
    '''Recursively upload files/folders to "path" or drp App folder'''

    handler = DrpHandler()
    files, folders = handler.search(path, query)
    if folders:
        echo('Matching Folders:')
        echo('\t'.join(folders))
    if files:
        echo('Matching Files:')
        echo('\t'.join(files))
