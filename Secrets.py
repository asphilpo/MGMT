#Many Many Thanks To Drew Winston Without Whomst You'd Have To
#Copy And Paste All This Stuff
#Across 3 Seperate Scripts

#WHEN I WAS YOUR AGE...Etc...Etc...

import os
import json

from Dropbox_Token_Despenser import DropboxTokenDespenser
#from Dropbox_Token_Despenser import DropboxTokenDespenser

defaultsSettings = data = '''
{
  "DROPBOX_SECRET": null,
  "DROPBOX_KEY": null,
  "DROPBOX_ACCESS_TOKEN": null,
  "DROPBOX_REFRESH_TOKEN": null,
  "AIRTABLE_API_KEY": null,
  "AIRTABLE_BASE_KEY": null,
  "AIRTABLE_TABLE_NAME": null,
  "AIRTABLE_URL":  null,
  "CONTENT_SOURCE": null,
  "THUMB_DEPOT": null,
  "THUMB_DB_PATH": null
}
'''
defaults =json.loads(defaultsSettings)
settingsPath = 'secrets.json'

def MakeNewSettings():
    print('No Local Settings Found. Let us make them...')
    defaults['CONTENT_SOURCE'] = input("Content Directory: ").strip()
    defaults['THUMB_DEPOT'] = input("Thumbnail Output Directory ").strip()
    defaults['THUMB_DB_PATH'] = input("DROPBOX API PATH i.e. Dropbox/Format/Thumbnail/Path : ").strip()
    defaults['AIRTABLE_API_KEY'] = input("Airtable API Key: ").strip()
    defaults['AIRTABLE_BASE_KEY'] = input("Airtable Base Key [BASE_STARTS_WITH_app_IN_URL]: ").strip()
    defaults['AIRTABLE_TABLE_NAME'] = input("Airtable Table Name [TABLE_STARTS_WITH_tbl_IN_URL]: ").strip()
    defaults['AIRTABLE_URL'] = f'https://api.airtable.com/v0/{defaults['AIRTABLE_BASE_KEY']}/{defaults['AIRTABLE_TABLE_NAME']}'
    defaults['DROPBOX_SECRET'] = input("Dropbox Secret: ").strip()
    defaults['DROPBOX_KEY'] = input("Dropbox Key: ").strip()
    getDB = input('Generate Dropbox Tokens? [y/n] ').lower().strip()
    if getDB == 'y' or getDB == 'yes':
        print('okay')
        try:
            access_token, refresh_token= DropboxTokenDespenser(defaults['DROPBOX_KEY'],defaults['DROPBOX_SECRET'])
            defaults['DROPBOX_ACCESS_TOKEN']=access_token
            defaults['DROPBOX_REFRESH_TOKEN']=refresh_token
        except Exception as e :
            print('Token Generation Failed!',e)

    final = open(settingsPath,'w')
    final.write(json.dumps(defaults))
    final.close()
    return defaults



try:
    file = open(settingsPath, "r")
    data = json.load(file)
    file.close()
except:
    open(settingsPath, 'w+').close()
    data = MakeNewSettings()
    

AIRTABLE_API_KEY = data['AIRTABLE_API_KEY']
AIRTABLE_BASE_KEY = data['AIRTABLE_BASE_KEY']
AIRTABLE_TABLE_NAME = data['AIRTABLE_TABLE_NAME']
AIRTABLE_URL = data['AIRTABLE_URL']
DROPBOX_SECRET=  data['DROPBOX_SECRET']
DROPBOX_KEY = data['DROPBOX_KEY']
DROPBOX_ACCESS_TOKEN = data['DROPBOX_ACCESS_TOKEN']
DROPBOX_REFRESH_TOKEN = data['DROPBOX_REFRESH_TOKEN']


if os.path.exists('secrets.json') :
    print('Settings Found. Proceeding.')
else:
    MakeNewSettings()