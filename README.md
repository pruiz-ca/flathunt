## Install:
- run: ``` pip install -r requirements.txt ``` to install required packages

## Usage
 - setup telegram-send with your bot (instructions: https://pypi.org/project/telegram-send/)
 - fill the urls in the script with your search urls
 - run: ``` python flathunt.py ```

The script checks every 10 mins for new flats and sends telegram msg if new flats are found.

The script was designed with the german websites. Depending on your language / changes in website design you might need to change the regular expressions used to filter links
