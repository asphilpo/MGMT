import os
import csv
import re
import json


# Configuration

with open('secrets.json', 'r') as json_file:
    data = json.load(json_file)
    
CSV_INPUT_PATH = data["REPORTS_DIR"]+'/data.csv'
CSV_OUTPUT_PATH = data["REPORTS_DIR"]+'/dataThumbs.csv'
IMAGE_FOLDER = data['THUMB_DEPOT_LOCAL']

def get_base_name(filename):
    """Remove version suffix and extension."""
    return re.sub(r'\.\w+$', '', filename)
    

def find_thumbnail(base_name, image_files):
    """Find a thumbnail that matches the base name."""
    for image in image_files:
        if get_base_name(image) == base_name:
            return image
    return None

def update_csv_with_local_thumbs(input_csv, output_csv, image_folder):
    # Step 1: List all local image files
    image_files = os.listdir(image_folder)

    # Step 2: Read original CSV
    with open(input_csv, newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['Thumbnail Link']
        rows = list(reader)

    # Step 3: Process each row
    for row in rows:
        base_name = get_base_name(row['File Name'])
        thumbname = base_name + "_" + row['Version Number']
        print(base_name)
        thumb_file = find_thumbnail(thumbname, image_files)
        if thumb_file:
            row['Thumbnail Link'] = f'images/{thumb_file}'
        else:
            row['Thumbnail Link'] = ''

    # Step 4: Write updated CSV
    with open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f'✅ Updated CSV with local image links: {output_csv}')

# Run it
update_csv_with_local_thumbs(CSV_INPUT_PATH, CSV_OUTPUT_PATH, IMAGE_FOLDER)
