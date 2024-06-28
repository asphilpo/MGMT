import tkinter
import os
import csv
import tkinter.messagebox
import tkinter.simpledialog
import requests
import dropbox
import re
import webbrowser

from dropbox import DropboxOAuth2FlowNoRedirect

def DropboxTokenDispenser(APP_KEY,APP_SECRET):
    auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET)

    authorize_url = auth_flow.start()
    dbURL = authorize_url + '&response_type=code&token_access_type=offline'
    webbrowser.open(dbURL, new=1, autoraise=True)
    
    authorization_code = tkinter.simpledialog.askstring(title='Dropbox Authorization Code', prompt='Enter the Dropbox Authorization Code:')
    
    auth_result = auth_flow.finish(authorization_code.strip())
    print(auth_result)
    access_token = auth_result.access_token
    refresh_token = auth_result.refresh_token

    return access_token, refresh_token