import click
from handler import DropboxerHandler


@click.group()
def cli():
    '''drp is a DropBoxer command. DropBoxer is a command line tool
    for Dropbox to ease upload, download of files and get public URLs.
    '''
    pass


@cli.command()
def init():
    '''Initialize the DropBoxer by getting Dropbox access token'''
    handler = DropboxerHandler(forceinit=True)


@cli.command()
@click.option('--path', '-p', default='/', type=click.Path(),
              help='Path where files will be uploaded')
@click.argument('files', nargs=-1)
def up(path, files):
    '''Recursively upload files/folders to "path" or DropBoxer App folder'''
    handler = DropboxerHandler()
    uploaded_files = handler.upload(path, files)
    for src, dst in uploaded_files:
        if src != dst:
            click.echo('Uploaded %s as %s' %(src, dst))


@cli.command()
@click.option('--path', '-p', default='.',
              type=click.Path(exists=True, resolve_path=True),
              help='Path where files will be downloaded')
@click.argument('files', nargs=-1)
def down(path, files):
    '''Recursively download files/folders to "path" or current directory'''
    handler = DropboxerHandler()
    failed_files = handler.download(path, files)

    click.echo('Failed File(s):')
    for filename, err in failed_files:
        click.echo('-> %s [%s] %s' % (filename, err[1:4], err[8:-1]))


@cli.command()
@click.argument('path', nargs=1, type=click.Path(),
                default='/', required=False)
def ls(path):
    '''List files/folders in the "path" or current directory'''
    click.echo('Listing everything in %s' % path)


@cli.command()
@click.argument('path', nargs=1, type=click.Path(),
                default='/', required=False)
def tree(path):
    '''Show file structure of "path" or current directory'''
    click.echo('Show tree of %s' % path)


@cli.command()
@click.argument('path', nargs=1, type=click.Path(), required=True)
def mkdir(path):
    '''Make a new directory under given path,
    ie, mkdir /foo/bar will make bar provided foo exists
    '''
    s = 'Will make %s under %s'
    click.echo(s % (path.split('/')[-1], '/'.join(path.split('/')[:-1])))


@cli.command()
@click.argument('path', nargs=1, type=click.Path(), required=True)
def rm(path):
    '''Remove a file or an empty directory under given directory'''
    s = 'Will delete %s under %s'
    click.echo(s % (path.split('/')[-1], '/'.join(path.split('/')[:-1])))


@cli.command()
@click.argument('path', nargs=1, type=click.Path(), required=True)
def share(path):
    '''Copy the public URL of the file to Clipboard'''
    s = 'Getting public url of %s under %s'
    click.echo(s % (path.split('/')[-1], '/'.join(path.split('/')[:-1])))


@cli.command()
@click.argument('path', nargs=1, type=click.Path(), required=True)
def info(path):
    '''Retrieve metadata for file/folder'''
    s = 'Getting metadata of %s under %s'
    click.echo(s % (path.split('/')[-1], '/'.join(path.split('/')[:-1])))
