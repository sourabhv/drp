#!/usr/bin/env python
# Encoding: utf-8

import os
import sys

from click import echo, prompt, confirm
import dropbox


class DropboxerHandler(object):

    # access_token is set in env vars
    access_token = os.environ.get('ACCESS_TOKEN')

    def __init__(self, forceinit=False):
        if forceinit or not self.access_token:
            self.initApp(forceinit=forceinit)
        else:
            self.client = dropbox.client.DropboxClient(self.access_token)

    def initApp(self, forceinit):
        """Get access token and enable client access."""

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

    def upload(self, path, files):
        """Upload file(s) to given path or app's root.

        $ drp up [-p path] file[ file[ file[...]]]
        Usage:
        drp up testfile
        drp up -d DropBox/sampleFolder/newfiles testfile
        """

        uploaded_files = []

        # fix path
        path = '/' + path.strip('/') + '/'

        for filename in files:
            try:
                with open(filename) as f:
                    response = self.client.put_file(path + filename, f)
                    upfilename = str(dict(response)['path']).split('/')[-1]
                    uploaded_files.append([filename, upfilename])
            except IOError as e:
                echo(str(e))

        return uploaded_files


    def download(self, path, files):
        """Download file(s) to current directory or destination_path.

        > drp down [-p path] file[ file[ file[...]]]
        Usage:
        drp down testfile
        drp down -p ../newfile testfile
        """

        failed_files = []

        for file in files:
            try:
                filename = file.split('/')[-1]
                out = open(os.path.join(path, filename), 'wb')
                with self.client.get_file(file) as f:
                    out.write(f.read())
                out.close()
            except dropbox.rest.ErrorResponse as e:
                failed_files.append([file, str(e)])
        return failed_files

def drp_ls(path):
    """list files/folders in current directory(default:root)"""
    response = api_client.metadata(current_path)
    if 'contents' in response:
        for f in response['contents']:
            name = os.path.basename(f['path'])
            encoding = locale.getdefaultlocale()[1]
            print(('%s\n' % name).encode(encoding))


def drp_cd(path):
    """navigate inside the directories."""
    if path == "..":
        current_path = "/".join(current_path.split("/")[0:-1])
    else:
        current_path += "/" + path


def drp_tree():
    """show file structure of current directory"""
    pass




def drp_rm(filename):
    """delete a file or directory"""
    api_client.file_delete(current_path + "/" + filename)
    log("Removed")


def drp_mkdir(foldername):
    """create a new directory"""
    api_client.file_create_folder(current_path + "/" + foldername)
    log("Directory created.")


def drp_share_file(filename):
    """copy public URL of source_file_path to clipboard"""
    log("Here's your URL: ")
    print api_client.share(filename, short_url=True)['url']
    # TODO: copy to clipboard


def drp_fileinfo(path):
    """Retrieve metadata for a file or folder."""
    file_metadata = client.metadata(path)
    print('\n\nMetadata:\n', file_metadata)


def drp_search(q):
    """Search Dropbox for filenames containing the given string."""
    results = self.api_client.search(self.current_path, q)
    log("searching ... ")
    log("Here are the search results ... ")
    for r in results:
        print("%s\n" % r['path'])


def main():
    if APP_KEY == '' or APP_SECRET == '':
        exit("You need to set your APP_KEY and APP_SECRET!")
    sys.exit(0)


if __name__ == '__main__':
    main()
