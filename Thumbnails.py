#Andy's Handy Thumbnail Factory
#No need to thank me, it's literally just ffmpeg.

import os
import subprocess
import json
import re
import shutil
from Secrets import *

with open('secrets.json', 'r') as json_file:
    data = json.load(json_file)

# POINT YOUR DIRECTORY AT THE JSON
CONTENT_SOURCE = data['CONTENT_SOURCE']
THUMB_DEPOT = data['THUMB_DEPOT']

def get_video_duration(file_path):
    ffprobe_cmd = [
        'ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'json', file_path
    ]
    result = subprocess.run(ffprobe_cmd, capture_output=True, text=True)
    json_output = json.loads(result.stdout)
    duration = float(json_output['format']['duration'])
    return duration

def create_thumbnails(input_directory, output_directory, thumbnail_time_percent):
    total_files_processed = 0

    for root, dirs, files in os.walk(input_directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file.lower().endswith(('.mov', '.mp4')):
                create_thumbnail(file_path, output_directory, thumbnail_time_percent)
                total_files_processed += 1
            elif file.lower().endswith(('.jpeg', '.jpg', '.png')):
                shutil.copy(file_path, output_directory)
                total_files_processed += 1


    print(f"Processing finished on {total_files_processed} files.")

def create_thumbnail(file_path, output_directory, thumbnail_time_percent):
    try:
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        thumbnail_file_name = f"{file_name}.jpg"
        thumbnail_path = os.path.join(output_directory, thumbnail_file_name)

        video_duration = get_video_duration(file_path)

        if video_duration <= 1:  # Check if the video duration is less than or equal to 1 second
            thumbnail_time = 0  # Set thumbnail time to 0 if the duration is too short
        else:
            thumbnail_time = video_duration * (thumbnail_time_percent / 100.0) / 2

        cmd = [
            'ffmpeg', '-n', '-ss', str(thumbnail_time), '-i', file_path, '-vframes', '1', '-q:v', '2',
            thumbnail_path
        ]
        subprocess.run(cmd, check=True, stderr=subprocess.PIPE)

        print(f"Thumbnail created: {file_name}")
    except Exception as e:
        print(f"Error creating thumbnail for file '{file_path}': {str(e)}")

# Prompt the user for input and output directories, and thumbnail time as a percentage
# We are hardcoding these variables but I used to to a version that would prompt you in the command line. 
# But in this house we believe in one-click automations so just specify your input and outputs below.
# The time float is a little hit or miss but 50 is ok for most files. If you're feeling adventurous, delete the old thumbnail of some 
# that were fails and try a different %. Right now I think it ignores existing thumbnails to prevent disparity in the Thumbinator

#Note that the Thumbinator is a Dropbox based workflow but I bet we could make it play nice on other cloud storage platforms
#Especially if they have a desktop client.

input_directory = CONTENT_SOURCE
output_directory = THUMB_DEPOT 
thumbnail_time_percent = float(50)

# Generate thumbnails
create_thumbnails(input_directory, output_directory, thumbnail_time_percent)





