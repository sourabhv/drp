#!/usr/bin/env python
# Encoding: utf-8

import os
import sys
import urllib2

from click import echo, prompt, confirm
import dropbox


class DropboxerHandler(object):

    # access_token is set in env vars
    access_token = os.environ.get('ACCESS_TOKEN')

    def __init__(self, forceinit=False):
        # check if internet connection is available
        try:
            response = urllib2.urlopen('http://74.125.228.100', timeout=1)
        except urllib2.URLError as e:
            echo('No internet connection available. Exiting ...')
            sys.exit(0)

        if forceinit or not self.access_token:
            self.initApp(forceinit=forceinit)
        else:
            self.client = dropbox.client.DropboxClient(self.access_token)

    def initApp(self, forceinit):
        '''Get access token and enable client access

        returns None'''

        confirm_str = 'One access token already exists, get a new one?'
        if self.access_token and forceinit:
            if not confirm(confirm_str):
                return

        app_key = prompt('Enter your app key')
        app_secret = prompt('Enter your app secret')
        flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
        authorize_url = flow.start()
        echo('1. Go to: ' + authorize_url)
        echo('2. Click "Allow" (you might have to log in first)')
        echo('3. Copy the authorization code.')
        code = prompt("Enter the authorization code").strip()

        try:
            access_token, user_id = flow.finish(code)
            echo('Recieved access_token: %s\n User_id: %s\n'
                 % (access_token, user_id))
            echo('Add access_token value to your environment variables')
        except dropbox.rest.ErrorResponse as e:
            echo('Error: %s' % str(e))

    def up(self, path, files):
        '''Upload file(s) to given path (default: root directory).

        returns a list of pairs filename and its filename on dropbox
        '''

        uploaded_files = []

        # fix path
        path = '/' + path.strip('/') + '/'

        for filename in files:
            try:
                with open(filename) as f:
                    response = dict(self.client.put_file(path + filename, f))
                    upfilename = os.path.basename(response['path'])
                    uploaded_files.append([filename, upfilename])
            except IOError as e:
                echo(str(e))

        return uploaded_files

    def down(self, path, files):
        '''Download file(s) to given path (default: current directory).

        return list of failed files and the error string
        '''

        failed_files = []

        for file in files:
            try:
                filename = os.path.basename(file)
                out = open(os.path.join(path, filename), 'wb')
                with self.client.get_file(file) as f:
                    out.write(f.read())
                out.close()
            except dropbox.rest.ErrorResponse as e:
                failed_files.append([file, str(e)])
        return failed_files

    def ls(self, path):
        '''List files/folders in given path (default: root directory)

        returns 2 lists - files and folders
        '''

        files, folders = [], []

        try:
            response = self.client.metadata(path)
        except dropbox.rest.ErrorResponse as e:
            echo(str(e))
        else:
            if 'contents' in response:
                for item in response['contents']:
                    name = os.path.basename(item['path'])
                    if item['is_dir']:
                        folders.append(name)
                    else:
                        files.append(name)
        finally:
            return files, folders

    def tree(self, path):
        '''Show file tree structure of given path (default: root directory)

        return None
        '''

        pass

    def mkdir(self, path):
        '''Create a new directories under given path

        returns None'''

        try:
            self.client.file_create_folder(path)
        except dropbox.rest.ErrorResponse as e:
            echo(e)

    def rm(self, name):
        '''Delete a file or a non-empty directory

        returns True if deleted successfully, False otherwise'''

        meta = self.info(name)
        if meta and meta['is_dir'] and meta['contents']:
            echo('Cannot delete a non-empty directory')
            return False
        else:
            self.client.file_delete(name)
            return True

    def share(self, path):
        '''Create a public URL of file/filer of given path

        returns dict with URL if succeeds, None otherwise'''

        try:
            return self.client.share(path, short_url=True)
        except dropbox.rest.ErrorResponse as e:
            echo(str(e))

    def info(self, path):
        '''Retrieve metadata for a file or folder

        returns metadata dictionary'''
        try:
            return self.client.metadata(path)
        except dropbox.rest.ErrorResponse as e:
            echo(str(e))

    def search(path, query):
        '''Search Dropbox for files/folders containing the given string'''
        files, folders = [], []
        try:
            response = self.client.search(path, query)
        except dropbox.rest.ErrorResponse as e:
            echo(str(e))
        else:
            for item in response:
                if item['is_dir']:
                    folders.append(item['path'])
                else:
                    files.append(item['path'])
        finally:
            return files, folders
