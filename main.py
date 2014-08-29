#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import dropbox

# keys are set in virtualenv's postactivate script
app_key = os.environ.get('APP_KEY')
app_secret = os.environ.get('APP_SECRET')
access_token = os.environ.get('ACCESS_TOKEN')
user_id = os.environ.get('USER_ID')

def get_access(self):
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
        self.stdout.write('Error: %s\n' % str(e))
        return

    print('Recieved access_token: %s\n User_id: %s\n', %s(access_token
                                                          user_id))

    ### enable client access
    with open(self.TOKEN_FILE, 'w') as f:
        f.write('oauth2:' + access_token)
    self.api_client = dropbox.client.DropboxClient(access_token)


def log(msg):
    """print to screen."""
    print msg


### Commands
#TODO: use argparse for use flags/options

def drp_ls():
    """list files/folders in current directory(default:root)"""
    pass

def drp_cd():
    """navigate inside the directories."""
    pass

def drp_tree():
    """show file structure of current directory"""
    pass

def drp_upload(*files, dest_path):
    """upload file(s) to current directory or destination path.

    > drp up file1 file2 file3 -d [dest_path]
    Usage:
      drp up testfile
      drp up testfile -d DropBox/sampleFolder/newfile
    """
    # TODO: add destination parameters

    # update path with slash 
    if dest_path[-1] != '/':
        dest_path += '/'

    log("Preparing file(s) for upload ...")
    log("Uploading file(s) ...")

    for filename in files:
        with open(filename) as f:
            response = client.put_file(dest_path+filename, f, overwrite=False,)
    print('Uploaded:\n', response)
    log("---------------------------------------------")

def drp_download():
    """download file(s) to current directory or destination_path.

    > drp down file1 file2 file3 -d [dest_path]
    Usage:
      drp down testfile
      drp down testfile -d Desktop/newfile
    """
    log("Preparing file(s) for download ...")

    f, metadata = client.get_file_and_metadata('./the_source.py')
    #out = open('sample.py', 'wb')
    #out.write(f.read())
    #out.close()
    #print('\n\nDownloaded: \n', metadata)
    pass

def drp_rm():
    pass

def drp_share_file():
    """copy public URL of source_file_path to clipboard"""
    pass

def drp_fileinfo():
    #file_metadata = client.metadata('./the_source.py')
    #print('\n\nMetadata:\n', file_metadata)
    pass


def main():
    if APP_KEY == '' or APP_SECRET == '':
        exit("You need to set your APP_KEY and APP_SECRET!")
    sys.exit(0)

if __name__ == '__main__':
    main()
