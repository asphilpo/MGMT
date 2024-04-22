#FEAR THE THUMBINATOR
#An Andy Philpo Hassle-Elimination Tool 

import os
import csv
import requests
import dropbox
import re
import json
from Secrets import *


with open('secrets.json', 'r') as json_file:
    data = json.load(json_file)

# POINT YOUR DIRECTORY AT THE JSON
CONTENT_SOURCE = data['CONTENT_SOURCE']
THUMB_DB_PATH = data['THUMB_DB_PATH']

#FOR ALL OF THIS TO WORK YOU NEED A DROPBOX OAUTH CODE FLOW WHICH IS HONESTLY
#A PAIN IN THE A$$ IMO
#I GOT IT WORKING BY ESSENTIALLY DOING AN OAUTH REQUEST ONCE USING THE CODE SNIPPET FROM THE API DOC
#SLOTTING IN THE REFRESH TOKEN THAT IT PRINTED BELOW
#AND IT'S JUST WORKED FOR ME SINCE THEN

# I WILL INCLUDE THE OAUTH AS I USED IT AT THE BOTTOM OFTHIS SCRIPT, COMMENTED OUT.
# MOVE IT TO THE TOP OF THE SCRIPT, OR RUN IT AS ITS OWN .PY
# TO TRY GETTING A REFRESH TOKEN
# TO PLUG INTO THE REFRESH TOKEN VARIABLE BELOW

#SOMEONE WHO GETS OAUTH BETTER COULD PROBABLY WORK IT INTO THIS CODE
#IF SOMEONE ACTUALL WANTS TO USE THIS APP SPECIFICALLY, RATHER THAN CREATING THEIR OWN, 
#I'M HAPPY TO GENERATE A USER TOKEN FOR YOU.
#BUT THE KEY AND STUFF IS ALL TIED TO MY ACCOUNT SO MAYBE NOT THE BEST IDEA???


# Dropbox access token (replace with your own)
#ACCESS_TOKEN = "YOUR ACCESS TOKEN WOULD GO HERE IF WE USED SHORT LIVED TOKENS"

# VARIABLES FOR DB API


def refresh_access_token(DROPBOX_REFRESH_TOKEN, DROPBOX_KEY, DROPBOX_SECRET):
    url = 'https://api.dropbox.com/oauth2/token'
    data = {
        'refresh_token': DROPBOX_REFRESH_TOKEN,
        'grant_type': 'refresh_token',
        'client_id': DROPBOX_KEY,
        'client_secret': DROPBOX_SECRET
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        print("Error refreshing access token:", response.text)
        return None



access_token = refresh_access_token(DROPBOX_REFRESH_TOKEN, DROPBOX_KEY, DROPBOX_SECRET)
if access_token:
    print("Access token:", access_token) #access token sanity check
    
# Initialize Dropbox client
refresh_access_token(DROPBOX_REFRESH_TOKEN, DROPBOX_KEY, DROPBOX_SECRET)
dbx = dropbox.Dropbox(access_token)


# Define headers for authorization
headers = {
    'Authorization': f'Bearer {AIRTABLE_API_KEY}',
    'Content-Type': 'application/json'
}

# Function to get share link for a file from Dropbox OLD VERSION
#def get_share_link(file_path):
#    shared_link_metadata = dbx.sharing_create_shared_link(file_path)
#    return shared_link_metadata.url

#Here's where we leverage the Dropbox API to get shared links
#In order for Airtable to download the image at the location for a local thumbnail, it needs to be dl=1
#Which I assume means "download permission true" in dbspeak. 

def get_share_link(file_path):
    shared_link_metadata = dbx.sharing_create_shared_link(file_path)
    share_link = shared_link_metadata.url
    
    # Replace ?dl=0 with ?dl=1 in the share link
    share_link = share_link.replace('dl=0', 'dl=1')
    
    return share_link


# Function to get file names in a folder from Dropbox

def list_files(folder_path):
    files = []
    for entry in dbx.files_list_folder(folder_path).entries:
        if isinstance(entry, dropbox.files.FileMetadata):
            files.append(entry.name)
    return files

# Function to match thumbnails with filenames and update Airtable with shared links
# Note that the Thumbnail needs to match exactly with the filename except version or extension. 
# And that we're comparing thumbnail to record, not the other way around.
# If there's no record for a Thumbnail, the item bounces.
# So this script runs last in the stack.

# We use a json container for the link because that is what airtable wants to see when you upload something to an Attachment field.
# Which all image files are, generally, in the database.
# You could include the filename as part of the patch if you wanted. I didn't want. 

def match_thumbnails_to_airtable(thumbnail_folder_path):
    # Get list of files in the thumbnail folder on Dropbox
    thumbnail_files = list_files(thumbnail_folder_path)
    
    # Iterate through each thumbnail file
    for file_name in thumbnail_files:
        # Get shared link for the thumbnail file
        share_link = get_share_link(f"{thumbnail_folder_path}/{file_name}")
        
        # Find the corresponding record in Airtable with matching filename
        asset_name = os.path.splitext(file_name)[0]  # Remove file extension to match with asset names
        asset_exists_status, record_id = asset_exists(asset_name)
        
        # If matching record found in Airtable, update 'Thumbnail' field with shared link
        if asset_exists_status:
            # Update Airtable with the thumbnail attachment
            data = {
                "fields": {
                    "Thumbnail": [
                        {
                            "url": share_link,
                            "filename": ""
                        }
                    ]
                }
            }
            response = requests.patch(f"{AIRTABLE_URL}/{record_id}", json=data, headers=headers)
            if response.status_code == 200:
                print(f"Thumbnail attachment for {asset_name} updated successfully.")
                print(share_link)
            else:
                print(f"Failed to update thumbnail attachment for {asset_name}. Status code: {response.status_code}")
        else:
            print(f"No matching asset found for thumbnail: {asset_name}")         
            

# Function to check if asset already exists in Airtable using filename before the _v suffix
def asset_exists(asset_name):
    # Extract filename before _v suffix (case insensitive)
    result = re.split(r"_v\d+|_V\d+|\.\w+", asset_name, re.IGNORECASE)[0]
    if result:
        asset_name_without_version = result
        params = {
            'filterByFormula': f'OR( {{Assets}} = "{asset_name_without_version}.mov", {{Assets}} = "{asset_name_without_version}.png")'
        }
        response = requests.get(AIRTABLE_URL, params=params, headers=headers)
        data = response.json()
        if 'records' in data and len(data['records']) > 0:
            return True, data['records'][0]['id']  # Return True and record ID if the asset exists
    return False, None


# Call the function to match thumbnails with filenames and update Airtable
thumbnail_folder_path = THUMB_DB_PATH  # specify the folder path in your Dropbox
print(AIRTABLE_TABLE_NAME)
match_thumbnails_to_airtable(thumbnail_folder_path)
print ('THANK YOU FOR USING THUMBINATOR')

