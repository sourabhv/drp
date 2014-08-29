#!/usr/bin/env python
# encoding: utf-8

import os

import dropbox

# keys are set in virtualenv's postactivate script
app_key = os.environ.get('APP_KEY')
app_secret = os.environ.get('APP_SECRET')
access_token = os.environ.get('ACCESS_TOKEN')
user_id = os.environ.get('USER_ID')

### To get access token

# flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)

# authorize_url = flow.start()
# print '1. Go to: ' + authorize_url
# print '2. Click "Allow" (you might have to log in first)'
# print '3. Copy the authorization code.'
# code = raw_input("Enter the authorization code here: ").strip()

# access_token, user_id = flow.finish(code)

# print(access_token, user_id)

### client access

client = dropbox.client.DropboxClient(access_token)

f = open('main.py', 'rb')
response = client.put_file('./the_source.py', f, overwrite=True)
print('Uploaded:\n', response)

file_metadata = client.metadata('./the_source.py')
print('\n\nMetadata:\n', file_metadata)

f, metadata = client.get_file_and_metadata('./the_source.py')
out = open('sample.py', 'wb')
out.write(f.read())
out.close()
print('\n\nDownloaded:\n', metadata)
