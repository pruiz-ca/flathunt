#!/usr/bin/env python3

import requests
import re
import time
import telegram_send
from bs4 import BeautifulSoup
import os

interval_minutes = 5
url_wg_begin = "https://www.wg-gesucht.de/en/wg-zimmer-in-Berlin.8.0.1."
url_wg_end = ".html?offer_filter=1&city_id=8&sort_column=3&noDeact=1&dFr=1656194400&dTo=1657490400&radLat=52.487490882485&radLng=13.444272279739&categories%5B%5D=0&rent_types%5B%5D=0&rMax=600&radAdd=Bouch%C3%A9stra%C3%9Fe+39&radDis=5000&img_only=1&pagination=1&pu="

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def checkFlat(link, regex):
    with open('flats.txt', 'a+') as f:
        if(regex.match(link) and link+"\n" not in old_flats):
            new_flats.append(link)
            f.write(link+"\n")

def sleep():
    for i in range(interval_minutes):
        print("Sleeping for "+str(interval_minutes-i)+" minutes...")
        time.sleep(60)

with open('flats.txt', 'a+') as f:
    pass

while True:
    cls()
    print("Checking for new flats...")

    try:
        with open('flats.txt', 'r') as f:
            old_flats = f.readlines()
        new_flats = []

        for i in range (3):
            url_wg_gesucht = url_wg_begin + str(i) + url_wg_end
            r = requests.get(url_wg_gesucht)
            soup = BeautifulSoup(r.text, features="html.parser")

            for flat in soup.find_all('a', href=True):
                link = "https://www.wg-gesucht.de/"+flat["href"]
                regex = re.compile("https://www.wg-gesucht.de/wg.[a-zA-Z0-9_-]+.[0-9]+.html")
                checkFlat(link, regex)

        print("Found " + str(len(new_flats)) + " new flats.")

        if(new_flats != []):
            print("Sending new flats to Telegram...")
            telegram_send.send(messages=new_flats)

        sleep()

    except:
        print("Error while checking for new flats.")
        telegram_send.send(messages=["Error while checking for new flats."])
        sleep()
