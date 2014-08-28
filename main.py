import os

import dropbox

# keys are set in virtualenv's postactivate script
app_key = os.environ.get('APP_KEY')
app_secret = os.environ.get('APP_SECRET')

flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
