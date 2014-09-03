#!/usr/bin/env python
# Encoding: utf-8

import os
import sys
import urllib2

from click import echo, prompt, confirm
import dropbox


class DrpHandler(object):

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
        '''Recursively Upload file(s) to given path (default: root directory).

        returns a list of pairs filename and its filename on dropbox
        '''

        failed_files = []

        for file in files:
            filename = os.path.basename(file)
            if os.path.exists(file):
                if os.path.isdir(file):
                    status = self.mkdir(os.path.join(path, filename))
                    if status[0]:
                        newpath = os.path.join(path, filename)
                        newfiles = os.listdir(file)
                        newfiles = [os.path.join(file, x) for x in newfiles]
                        new_failed_files = self.up(newpath, newfiles)
                        failed_files.extend(new_failed_files)
                    else:
                        failed_files.append([file, status[1]])
                else:
                    try:
                        with open(file, 'rb') as f:
                            uppath = os.path.join(path, filename)
                            self.client.put_file(uppath, f)
                    except IOError as e:
                        failed_files.append([file, str(e)])
            else:
                failed_files.append([file, 'Does not exist'])

        return failed_files

    def down(self, path, files):
        '''Recursively Download file(s) to given path (default: current directory).

        return list of failed files and the error string
        '''

        failed_files = []

        for file in files:
            filename = os.path.basename(file)
            meta = self.info(file)
            if meta[0]:
                meta = meta[1]
                if meta['is_dir']:
                    try:
                        os.mkdir(os.path.join(path, filename))
                        newpath = os.path.join(path, filename)
                        newfiles = [x['path'] for x in meta['contents']]
                        new_failed_files = self.down(newpath, newfiles)
                        failed_files.extend(new_failed_files)
                    except OSError:
                        failed_files.append([file, 'Directory already exists'])
                else:
                    try:
                        out = open(os.path.join(path, filename), 'wb')
                        with self.client.get_file(file) as f:
                            out.write(f.read())
                        out.close()
                    except dropbox.rest.ErrorResponse as err:
                        err = self.prettyErr(str(err))
                        failed_files.append([file, err])
            else:
                failed_files.append([file, 'Does not exist'])

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

        return True if succesful, else False'''

        try:
            self.client.file_create_folder(path)
            return (True,)
        except dropbox.rest.ErrorResponse as err:
            err = self.prettyErr(str(err))
            return False, err

    def rm(self, paths):
        '''Delete files or a non-empty directories

        returns list of paths not removed succesfully'''

        failed_paths = []

        for path in paths:
            meta = self.info(path)
            if meta[0]:
                if meta[1]['is_dir'] and meta[1]['contents']:
                    failed_paths.append([path, 'NonEmptyDirectory'])
                else:
                    self.client.file_delete(path)
            else:
                failed_paths.append([path, 'Does not exist'])

        return failed_paths

    def share(self, path):
        '''Create a public URL of file/filer of given path

        returns dict with URL if succeeds, None otherwise'''

        try:
            return self.client.share(path, short_url=True)
        except dropbox.rest.ErrorResponse as e:
            echo(str(e))

    def info(self, path):
        '''Retrieve metadata for a file or folder

        returns metadata dictionary if succeeds, else None'''
        try:
            meta = self.client.metadata(path)
            if not meta.get('is_deleted', None):
                return True, meta
        except dropbox.rest.ErrorResponse as e:
            pass
        return (False,)

    def search(self, path, query):
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

    def prettyErr(self, str):
        s = str.find('"') + 1
        e = str.find('"', s)
        return str[s:e]
