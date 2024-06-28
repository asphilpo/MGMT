# MGMT
A small pile of scripts for a content data entry workflow centered around Dropbox and Airtable APIs

# UPDATE: GUI EDITION
With many many many thanks to Josh Spodick for his contribution I'm excited to offer up a GUI option for the MGMT package!
Quality of life features include: 
- File Path Browser
- Save and Load Management Configuration
- "Run Script" Button
- Additional Data Fields for FPS and Frame Count -- BE SURE TO ADD THESE TO YOUR AIRTABLE OR PREPARE FOR 422 ERRORS
 (Thanks to Jackson at F9 for these update suggestions!)


## THINGS YOU NEED TO MAKE THIS TRASH FIRE FUNCTIONAL:

0. Python. I Built it in 3.12 so I'd start there.

0.5. FFMPEG. Don't leave home without it clearly defined in your PATH environment variables!

1. An Airtable API Key. You get this from the airtable developer hub.
	-Needs Read/Write Permissions of records on whatever table your content is going to be catalogued in. 
	
2. A Dropbox API App Secret and Client Id
	- You get these by making an "App" for Dropbox through their developer hub. You need to give the app 
		basically full permissions to your acct but you will mostly be using
			Read/Create Share Link Functionality.
			
			
## What it does:

1) Catalogues all of your API Keys and directories into "secrets.json" This becomes the codex through which the rest of the script finds and records media info.

1a) A NOTE ON DROPBOX/THUMBNAIL/PATH: This wants to be the relative path of your thumbnail folder as though accessing it from the web, rather than your browser. 


So this variable will read something like "/Project/Thumbnail/Folder" for the local path of "C:\\Users\Me\Dropbox\Project\Thumbnail\Folder".
It is important to leave off the Trailing "/" - it should read exactly as above with the last character of the string being the last character of your folder name.
Otherwise you will get a "Not Found" type error from the dropbox API. (Thanks Josh!)


2) Makes a fun little thumbnail at 50% duration of your clip and drops it in a folder you specify (this wants to be on your Dropbox).


2a) If you have any still image files, I suggest just copying them into the thumbnail folder directly. Maybe in a later version I will include a function that does this automagically. 


3) Adds Your media file name and some metadata to a airtable of your choosing.  -- Please note that when prompted for the table name I give a little hint about the table suffix in the url 
																				-- you can also just use the regular name of the table if you choose. 
																				-- This may be easier if you have multiple tables. 


3a) The Fields you want to have in your airtable are as follows:

- Assets
- Delivered Version
- Folder
- Resolution
- Date Created
- Duration
- FPS
- Frame Count
- Thumbnail

***If any of these are spelled differently or mismatched in your table you will get a 422 Error from airtable.***

I would start them all [EXCEPT THUMBNAILS] as single-line text fields, but once you've done a volley, I like to change version, resolution, and folder to single-selects, and then add additional entries for the select as I go, to leverage the 
	Built in color-coding of Airtable.

Thumbnails wants to be an attachment field. This is how we trick airtable into uploading all the images for us.

***Bear in mind, the above are the only fields the script NEEDS in order to work, but the power of airtable is any additional fields, cross-lookups, and show-specific tags you might want to use alongside in additional fields. These will be ignored during any patches that occur on an update function.***

4) Takes all the fun little Thumbnails from 2., makes a dropbox link for them, and posts that as a json packet to the corresponding file in your Airtable under "Thumbnails". Unless there isn't a record with a name that matches your thumbnail. In which case it just moves on.


That's it that's literally the whole thing!

Run it as many times as you want when you get new versions delivered. Keep an eye on the command output for 422 errors from Airtable-- this means something is formatted in a way that your table cannot accept, and is a clue to check a file's resolution, version, name formatting etc.
The script will also print the failed data packet for you to check in the same line. 

Took me an embarrassing amount of time to make but hopefully saves you some time in the future! 
Many thank yous to the folks that helped me smooth out the rough edges into slightly less rough edges. 




# HOW TO RUN IT:

1. Create your airtable with the appropriate fields listed above

2. retrieve all API keys and secrets needed from both airtable and dropbox

3. Just Click on _GUI.py and fill out the required fields. All Fields must be filled out to work. 
<img width="706" alt="Screenshot 2024-06-14 at 10 45 08 AM" src="https://github.com/KirbyLV/airtable_asset_MGMT/assets/127134899/8a76a8ee-7741-48b8-a944-eb9c3dec48e2">

> [!IMPORTANT]
> 3a. You can use the "Browse" buttons to select:
> 	>The "Content Directory" - This is where you have all of your media assets you plan on using.
>  >
> 	>The "Thumbnail Output Directory" - This is the dropbox location where the app will place thumbnails to be used in the airtable display.
>
> 3b. The "Dropbox Relative Thumbnail Path" is the thumbnail output directory AFTER your dropbox folder location. For example, if your thumbnail output location is "/Users/myname/dropbox(personal)/apps/thumbnails" then your Dropbox Relative Thumbnail Path will be "/apps/thumbnails"
>
> 3c. The "Airtable Token" is the Airtable API token generated from the airtable developer hub
>
> 3d. The "Airtable Base Key" can be found in the URL of the airtable you are using as your content tracker. Look in the URL address bar of the airtbale web page when you have the table open and find the section starting with "app". For example, within `https://airtable.com/appxxxxxxx/tblyyyyyyy/viwzzzzzzz?blocks=hide` the "Base Key" is "appxxxxxxx"
>
> 3e. The "Airtable Table Key" can be found in the URL of the airtable you are using as your content tracker. Look in the URL address bar of the airtbale web page when you have the table open and find the section starting with "tbl". For example, within `https://airtable.com/appxxxxxxx/tblyyyyyyy/viwzzzzzzz?blocks=hide` the "Base Key" is "tblyyyyyyy"
>
> 3f. The "Dropbox App Key" and "Dropbox App Secret" are the api key and secret generated within the dropbox developer hub when you created an app.

  4. After populating all fields above, click on "Save Configuration" and then "Retrieve Dropbox Refresh Token" 
  	4a. The "Retrieve Dropbox Refresh Token" will open a webpage prompting you to login to the appropriate dropbox, grant permissions, and will generate a key. Copy the resulting key and paste it into the popup box below, then hit "OK"

<img width="273" alt="Screenshot 2024-06-14 at 10 54 53 AM" src="https://github.com/KirbyLV/airtable_asset_MGMT/assets/127134899/23deacdb-ebda-4683-996c-e4941ef8a562">

5. After populating all fields, and retrieving a refresh token, you will be able to run the app. The app will comb through your content directory, generate thumbnails, compare versions, and popualte the appropriate data in the airtable you designated. 

> [!TIP]
> If you are relaunching the app after using it before, and want to keep the same airtable and dropbox and location settings, you can click on "Load Existing Data" and all of the data previously used will load. You may have to generate a new refresh token. 

Enjoy!

THIS IS A WORK IN PROGRESS!

All back end by Andy Philpo. Front end by Josh Spodick.
