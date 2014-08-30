#!/usr/bin/env python
# Encoding: utf-8

import os
import sys

import dropbox

# keys are set in virtualenv's postactivate script
app_key = os.environ.get('APP_KEY')
app_secret = os.environ.get('APP_SECRET')
access_token = os.environ.get('ACCESS_TOKEN')
user_id = os.environ.get('USER_ID')

# __init__
TOKEN_FILE = "token_store.txt"
api_client = None
current_path = ''


def get_access():
    """Get access token and enable client access."""

    flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
    authorize_url = flow.start()
    print '1. Go to: ' + authorize_url
    print '2. Click "Allow" (you might have to log in first)'
    print '3. Copy the authorization code.'
    code = raw_input("Enter the authorization code here: ").strip()

    try:
        access_token, user_id = flow.finish(code)
    except rest.ErrorResponse, e:
        print('Error: %s\n' % str(e))
        return
    print('Recieved access_token: %s\n User_id: %s\n', % (access_token
                                                          user_id))
    # enable client access
    with open(TOKEN_FILE, 'w') as f:
        f.write('oauth2:' + access_token)
    api_client = dropbox.client.DropboxClient(access_token)


def log(msg):
    """print to screen."""
    print msg


# Commands
# TODO: use argparse for flags/options

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


def drp_upload(*files, path):
    """upload file(s) to current directory or destination path.

    > drp up file1 file2 file3 -d [path]
    Usage:
    drp up testfile
    drp up testfile -d DropBox/sampleFolder/newfile
    """
    # TODO: add destination parameters

    # update path with slash
    if path[-1] != '/':
        path += '/'

    log("Preparing file(s) for upload ...")
    log("Uploading file(s) ...")
    for filename in files:
        with open(filename) as f:
            response = client.put_file(path+filename, f, overwrite=False,)
    print('Uploaded:\n', response.get('size'))
    log("---------------------------------------------")


def drp_download(*files, to_path):
    """download file(s) to current directory or destination_path.

    > drp down file1 file2 file3 -d [path]
    Usage:
    drp down testfile
    drp down testfile -d Desktop/newfile
    """
    log("Preparing file(s) for download ...")

    for filename in files:
        with open(filename) as f:
            f, metadata = client.get_file_and_metadata(current_path + '/' + filename)
    output = open(os.path.expanduser(to_path), 'wb')
    output.write(f.read())
    output.close()
    print('\n\nDownloaded: \n', metadata.get('size'))
    log("---------------------------------------------")


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
