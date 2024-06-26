#Push Button Get Banana

import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", '-r', package])
package = 'requirements.txt'

install (package)

#Input API Keys, Tokens, Directories into secrets.json
subprocess.run(['python3', 'Secrets.py'])

# Execute the first script
subprocess.run(['python3', 'Thumbnails.py'])

# Execute the second script
subprocess.run(['python3', 'Media_Meta.py'])

# Execute the third script
subprocess.run(['python3', 'Thumbinator.py'])
