from setuptools import setup

setup(
    name='Drp',
    version='0.1',

    description='Drp is a Dropbox command line utility to ease upload, download and sharing of files',
    long_description='''Drp is Dropbox CLI tool which supports
    Upload, Download, Delete, Share, List files/folders, Show file structure tree
    Drp works in its own App folder (and not the Dropbox root) to decrease secutity risks.
    ''',

    author='Sourabh Verma',
    author_email='sourabh.coder@gmail.com',

    license='GPLv3',
    keywords='dropbox cli tool',
    url='https://github.com/sourabhv/drp',
    download_url='https://github.com/sourabhv/drp/archive/0.1.tar.gz',
    website='https://github.com/sourabhv/drp',

    packages=[
        'drp'
    ],

    install_requires=[
        'dropbox',
        'click'
    ],

    entry_points='''
        [console_scripts]
        drp=drp.drp:cli
    ''',
)
