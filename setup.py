from setuptools import setup

setup(
    name='DropBoxer',
    version='1.0',
    description='DropBoxer is a command line utility to ease upload, download and sharing of files',
    long_description='''DropBoxer is Dropbox CLI tool which supports following:
        Upload, Download, Delete, Share, List files/folders, Show file structure tree
    DropBoxer works in its own App folder to decrease secutity risks, but please file a Github Issue if you wish DropBoxer to be able to access your DropBox root
    ''',
    author='Sourabh Verma',
    author_email='sourabh.coder@gmail.com',
    py_modules=['dropboxer'],
    install_requires=[
        'dropbox',
        'click'
    ],
    entry_points='''
        [console_scripts]
        drp=dropboxer.dropboxer:cli
    ''',
)
