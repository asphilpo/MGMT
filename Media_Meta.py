#Grant & Andy's Handy Content Manager -- Does the data entry so you can spend more time in catering!
#All Rights Reserved? Or Whatever. I'm not a lawyer and lets be honest chatGPT wrote half of this anyway.

#import your stuff. Explicit vs. Implicit! It's the Python way!
import os
import re
import csv
import requests
import subprocess
from datetime import datetime
import math
import json
from Secrets import *

with open('secrets.json', 'r') as json_file:
    data = json.load(json_file)

# POINT YOUR DIRECTORY AT THE JSON
CONTENT_SOURCE = data['CONTENT_SOURCE']

# Airtable credentials and base info


# Define headers for authorization
headers = {
    'Authorization': f'Bearer {AIRTABLE_API_KEY}',
    'Content-Type': 'application/json'
}


# Define the folder to look into. Use regex and a double \\ to avoid escape characters. Do you need both? maybe not idk.
# You can put any path inside the '' just using d3 as an example.
# Or make a prompt input if you want to interact with the script every time you run it. 
# I'd rather embed the path and make it one-click. 

folder_path = CONTENT_SOURCE


# Function to convert seconds to minutes and seconds for when your designer can't convert s in their head.
def seconds_to_minutes_seconds(seconds):
    minutes = math.floor(seconds / 60)
    seconds = seconds % 60
    return "{:02d}:{:02d}".format(int(minutes), int(seconds))

def get_file_names_and_versions(folder_path):
    file_names = []
    version_numbers = []
    root_folders = []
    sub_folders = []
    resolutions = []
    dates = []
    durations = []

    for root, dirs, files in os.walk(folder_path):
        sub_folder = os.path.basename(root)  # Get the name of the immediate parent folder
        parent_folder = os.path.basename(os.path.dirname(root))  # Get the name of the parent folder
        
        for file in files:
            # Extract file name and version number using regex (case-insensitive)
            result = re.search(r'^(.+?)_v(\d+)(\.\w+)', file, re.IGNORECASE)
            if result:
                file_name_without_version = result.group(1)
                file_extension = result.group(3)
                version_number = result.group(2)
                file_names.append(file_name_without_version + file_extension)
                version_numbers.append('v' + version_number)
            else:
                file_names.append(file)  # Append original file name if no version number found
                version_numbers.append('v00')
            root_folders.append(parent_folder)
            sub_folders.append(sub_folder)
            
            # Full path to the file
            file_path = os.path.join(root, file)
            
            # Initialize variables with default values
            resolution = '0x0'
            date_created = '0000-00-00 00:00:00'
            duration = '0'

            try:
                # Run ffprobe command
                cmd = [
                    'ffprobe', '-v', 'error', '-select_streams', 'v:0',
                    '-show_entries', 'stream=width,height,duration', '-of', 'csv=p=0',
                    file_path
                ]
                result = subprocess.run(cmd, check=True, capture_output=True, text=True)
                output = result.stdout.strip()
                
                # Check if output is non-empty
                if output:
                    data = output.split(',')
                    
                    # Ensure that data contains at least three elements before accessing its elements
                    if len(data) >= 3:
                        resolution = data[0] + 'x' + data[1]

                        if data[2] != 'N/A':
                            duration_seconds = float(data[2])
                            duration = seconds_to_minutes_seconds(duration_seconds)

                    # Get the file creation timestamp
                    timestamp = os.path.getctime(file_path)
                    date_created = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                    
            except subprocess.CalledProcessError as e:
                # Log the error or print it
                print(f"Error analyzing file {file_path}: {e}")
                
            # Append data to arrays
            resolutions.append(resolution)
            dates.append(date_created)
            durations.append(duration)

    return file_names, version_numbers, root_folders, sub_folders, resolutions, dates, durations


file_names, version_numbers, root_folders, sub_folders, resolutions, dates, durations = get_file_names_and_versions(folder_path)


# Combine file names and version numbers into a list of tuples
data = list(zip(file_names, version_numbers, root_folders, sub_folders, resolutions, dates, durations))

# Define CSV file path
#csv_file_path = 'data.csv'

# Write data to CSV file - this is a useful sanity check to be sure your data is being organized correctly but is commented out for now.
#with open(csv_file_path, 'w', newline='') as csvfile:
#    writer = csv.writer(csvfile)
#    writer.writerow(['File Name', 'Version Number', 'Folder', 'Subfolder', 'Resolution', 'Date Created', 'Duration'])  # Write header
#    for file_names, version_numbers, root_folders, sub_folders, resolutions, dates, durations in data:
#        writer.writerow([file_names, version_numbers, root_folders, sub_folders, resolutions, dates, durations])

#print(f"CSV file '{csv_file_path}' generated successfully.")
#print (version_numbers) #unnecessary now vith the various sanity checks in the add function?
# Define the function to check if asset already exists in Airtable using versionless names
def asset_exists(asset_name):
    params = {
        'filterByFormula': f'{{Assets}} = "{asset_name}"'
    }
    response = requests.get(AIRTABLE_URL, params=params, headers=headers)
    data = response.json()
    if 'records' in data and len(data['records']) > 0:
        return True, data['records'][0]['id']  # Return True and record ID if the asset exists
    return False, None

# Define the function to add file names to Airtable if they don't already exist
def add_file_names_to_airtable(file_names, version_numbers, root_folders, sub_folders, resolutions, dates, durations):
    for file_name, version_number, root_folder, sub_folder, resolution, date_created, duration in zip(file_names, version_numbers, root_folders, sub_folders, resolutions, dates, durations):
        asset_exists_status, record_id = asset_exists(file_name)

        if asset_exists_status:
            # Asset already exists, update the version number and metadata
            data = {
                "fields": {
                
                    "Delivered Version": version_number,  # Include version number in the data
                    "Date Created" : date_created,
                    "Resolution" : resolution,
                    "Duration" : duration,

                }
            }
            response = requests.patch(f"{AIRTABLE_URL}/{record_id}", json=data, headers=headers)
            if response.status_code != 200:
                print(f"Failed to update version number for {os.path.splitext(file_name)[0]}. Status code: {response.status_code}")
                print(data) #sanity check on Airtable 402 errors to see why a record bounced
            else:
                print(f"Version number for {file_name} updated successfully.")
        else:
            # Asset does not exist, create a new entry. Note we are using the sub_folder array for the folder entry. 
            # parent_folder could also be called here if you wanted two layers of directory organization in your table.
            # But we didn't so it doesn't. 
            data = {
                "fields": {
                
                    "Assets": file_name,
                    "Folder": sub_folder,
                    "Delivered Version": version_number,
                    "Date Created" : date_created,
                    "Resolution" : resolution,
                    "Duration" : duration,

                }
            }
            response = requests.post(AIRTABLE_URL, json=data, headers=headers)
            if response.status_code != 200:
                print(f"Failed to add {file_name} to Airtable. Status code: {response.status_code}")
                print(data) #sanity check on Airtable 402 errors to see why a record bounced
            else:
                print(f"{file_name} added to Airtable successfully.")            

 
# Add file names and update versions to Airtable
print(file_names) #sanity check on all the records found
add_file_names_to_airtable(file_names, version_numbers, root_folders, sub_folders, resolutions, dates, durations) #do the thing.




