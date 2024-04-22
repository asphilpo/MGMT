#Push Button Get Banana

import subprocess

#Input API Keys, Tokens, Directories into secrets.json
subprocess.run(['python', 'Secrets.py'])

# Execute the first script
subprocess.run(['python', 'Thumbnails.py'])

# Execute the second script
subprocess.run(['python', 'Media_Meta.py'])

# Execute the third script
subprocess.run(['python', 'Thumbinator.py'])
