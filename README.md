# MGMT
A small pile of scripts for a content data entry workflow centered around Dropbox and Airtable APIs


THINGS YOU NEED TO MAKE THIS TRASH FIRE FUNCTIONAL:

0. Python. I Built it in 3.12 so I'd start there.

0.5. FFMPEG. Don't leave home without it clearly defined in your PATH environment variables!

1. An Airtable API Key. You get this from the airtable developer hub.
	-Needs Read/Write Permissions of records on whatever table your content is going to be catalogued in. 
	
2. A Dropbox API App Secret and Client Id
	- You get these by making an "App" for Dropbox through their developer hub. You need to give the app 
		basically full permissions to your acct but you will mostly be using
			Read/Create Share Link Functionality.
			
			
What it does:

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
- Thumbnail

***If any of these are spelled differently or mismatched in your table you will get a 422 from airtable.***

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



HOW TO RUN IT:

Just Click on _MGMT.py and it should do the rest!
***IF YOU ARE ON A MAC, RUN _MGMT_OSX.py*** It uses a slightly different syntax.
