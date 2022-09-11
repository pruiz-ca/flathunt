#!/usr/bin/env python3

import requests
import re
import time
import json
import telegram_send
import dotenv
from bs4 import BeautifulSoup
import os

dotenv.load_dotenv()

# if .env file is not present, print error and exit
if not os.path.exists('.env'):
    print("Please create a .env file with env_example as template and fill in your credentials")
    exit(1)

email = os.getenv('EMAIL')
pwd = os.getenv('PASSWORD')
url_wg_gesucht = os.getenv('URL_WG_GESUCHT')
interval_minutes = os.getenv('INTERVAL_MINUTES')


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def checkFlat(link, regex):
    with open('flats.txt', 'a+') as f:
        if(regex.match(link) and link+"\n" not in old_flats):
            new_flats.append(link)
            f.write(link+"\n")


def sleep():
    for i in range(interval_minutes):
        print("Sleeping for " + str(interval_minutes - i) + " minutes...")
        time.sleep(60)


def login(session):
    url = "https://www.wg-gesucht.de/ajax/sessions.php?action=login"

    payload = json.dumps({
        "login_email_username": f"{email}",
        "login_password": f"{pwd}",
        "login_form_auto_login": "1",
        "display_language": "de"
    })

    headers = {
        'sec-ch-ua': '"Microsoft Edge";v="105", " Not;A Brand";v="99", "Chromium";v="105"',
        'DNT': '1',
        'sec-ch-ua-mobile': '?0',
        'X-Authorization': 'Bearer',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.33',
        'X-Dev-Ref-No': '',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-Client-Id': 'wg_desktop_website',
        'X-Requested-With': 'XMLHttpRequest',
        'X-User-Id': '',
        'sec-ch-ua-platform': '"macOS"',
        'host': 'www.wg-gesucht.de'
    }

    session.get("https://www.wg-gesucht.de/en/")
    r = session.post(url, headers=headers, data=payload)
    if (r.status_code == 200):
        print("Login successful")
    else:
        print("Login failed")
        telegram_send.send(messages=["Login Failed"])


with open('flats.txt', 'a+') as f:
    pass

session = requests.Session()
login(session)

cls()
while True:
    print("Checking for new flats...")

    try:
        with open('flats.txt', 'r') as f:
            old_flats = f.readlines()
        new_flats = []

        header = {
            'sec-ch-ua': '"Microsoft Edge";v="105", " Not;A Brand";v="99", "Chromium";v="105"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'Upgrade-Insecure-Requests': '1',
            'DNT': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.33',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'host': 'www.wg-gesucht.de',
            'Cookie': f'PHPSESSID={session.cookies["PHPSESSID"]}; X-Access-Token={session.cookies["X-Access-Token"]}; X-Client-Id=wg_desktop_website; X-Dev-Ref-No={session.cookies["X-Dev-Ref-No"]}; X-Refresh-Token={session.cookies["X-Refresh-Token"]}; dev_ref_no={session.cookies["dev_ref_no"]}; last_cat=0%2C1; last_city=8; last_type=0; login_token={session.cookies["login_token"]}'
        }

        r = session.get(url_wg_gesucht, headers=header)
        soup = BeautifulSoup(r.text, features="html.parser")

        for flat in soup.find_all('a', href=True):
            link = "https://www.wg-gesucht.de/" + flat["href"]
            regex = re.compile(
                "https://www.wg-gesucht.de/wg.[a-zA-Z0-9_-]+.[0-9]+.html")
            checkFlat(link, regex)

        print("Found " + str(len(new_flats)) + " new flats.")

        if(new_flats != []):
            print("Sending new flats to Telegram...")
            telegram_send.send(messages=new_flats)
        sleep()

    except:
        print("Error while checking for new flats.")
        telegram_send.send(messages=["Error while checking for new flats."])
        login(session)
        sleep()
