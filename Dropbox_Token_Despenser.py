import os
import csv
import requests
import dropbox
import re
import webbrowser

from dropbox import DropboxOAuth2FlowNoRedirect


def DropboxTokenDespenser(APP_KEY,APP_SECRET):

    # Initialize the Dropbox OAuth 2.0 flow
    auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET)

    # Generate the authorization URL
    authorize_url = auth_flow.start()

    # Print the URL and prompt the user to visit it and authorize your app
    print("1. Go to: " + authorize_url + '&response_type=code&token_access_type=offline')
    print("2. Click 'Allow' (you might have to log in first)")
    print("3. Copy the authorization code.")

    # Once the user authorizes your app and gets the authorization code, you can exchange it for an access token
    authorization_code = input("Enter the authorization code here: ").strip()

    # Call the finish method to complete the authorization process
    auth_result = auth_flow.finish(authorization_code)

    # Extract the access token and refresh token from the auth_result
    print(auth_result)
    access_token = auth_result.access_token
    refresh_token = auth_result.refresh_token

    return access_token, refresh_token
    # Now you have both access token and refresh token
    print("Access Token:", access_token)
    print("Refresh Token:", refresh_token)

def DropboxTokenDespenserGUI(APP_KEY,APP_SECRET):

    # Initialize the Dropbox OAuth 2.0 flow
    auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET)

    # Generate the authorization URL
    authorize_url = auth_flow.start()

    #Open webpage in new window
    dbURL = authorize_url + '&response_type=code&token_access_type=offline'
    webbrowser.open(dbURL, new=1, autoraise=True)

def DropboxTokenAuthorizationGUI(APP_KEY,APP_SECRET,REFRESH_KEY):
    # Initialize the Dropbox OAuth 2.0 flow
    auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET)

    # Generate the authorization URL
    authorize_url = auth_flow.start()

    # Once the user authorizes your app and gets the authorization code, you can exchange it for an access token
    authorization_code = REFRESH_KEY

    # Call the finish method to complete the authorization process
    auth_result = auth_flow.finish(authorization_code)

    # Extract the access token and refresh token from the auth_result
    print(auth_result)
    access_token = auth_result.access_token
    refresh_token = auth_result.refresh_token

    return access_token, refresh_token



##################### OAUTH EXAMPLE BELOW ##########################################

#from dropbox import DropboxOAuth2FlowNoRedirect

'''
This example walks through a basic oauth flow using the existing long-lived token type
Populate your app key and app secret in order to run this locally
'''
#APP_KEY = "CLIENT ID GOES HERE"
#APP_SECRET = "CLIENT SECRET GOES HERE"

#auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET)

#authorize_url = auth_flow.start()
#print("1. Go to: " + authorize_url)
#print("2. Click \"Allow\" (you might have to log in first).")
#print("3. Copy the authorization code.")
#auth_code = input("Enter the authorization code here: ").strip()

#try:
#    oauth_result = auth_flow.finish(auth_code)
#except Exception as e:
#    print('Error: %s' % (e,))
#    exit(1)

#with dropbox.Dropbox(oauth2_access_token=oauth_result.access_token) as dbx:
#    dbx.users_get_current_account()
#    print("Successfully set up client!")
#    print(oauth_result)
# Initialize Dropbox client
#dbx = dropbox.Dropbox(oauth_result)

# Define your app key and secret obtained from the Dropbox developer console
#APP_KEY = "CLIENT ID GOES HERE"
#APP_SECRET = "CLIENT SECRET GOES HERE"

# Initialize the Dropbox OAuth 2.0 flow
#auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET)

# Generate the authorization URL
#authorize_url = auth_flow.start()

# Print the URL and prompt the user to visit it and authorize your app
#print("1. Go to: " + authorize_url)
#print("2. Click 'Allow' (you might have to log in first)")
#print("3. Copy the authorization code.")

# Once the user authorizes your app and gets the authorization code, you can exchange it for an access token
#authorization_code = input("Enter the authorization code here: ").strip()

# Call the finish method to complete the authorization process
#auth_result = auth_flow.finish(authorization_code)

# Extract the access token and refresh token from the auth_result
#access_token = auth_result.access_token
#refresh_token = auth_result.refresh_token

# Now you have both access token and refresh token
#print("Access Token:", access_token)
#print("Refresh Token:", refresh_token)

