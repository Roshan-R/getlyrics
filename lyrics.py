#! /usr/bin/env python3

import dbus
import requests
from bs4 import BeautifulSoup
import shutil
import os

def get_title():
    session_bus = dbus.SessionBus()
    media_session = "null"
    for service in session_bus.list_names():
        if "org.mpris.MediaPlayer2" in service:
            media_session = service
            break

    if media_session == "null":
        print("Cannot detect any current playing songs")
        exit()

    media_bus = session_bus.get_object(media_session,
                                       "/org/mpris/MediaPlayer2")
    media_properties = dbus.Interface(media_bus,
                                      "org.freedesktop.DBus.Properties")
    metadata = media_properties.Get("org.mpris.MediaPlayer2.Player", "Metadata")

    # print(metadata)
    return metadata['xesam:title']

def clean_title(title):
    title = title.lower()
    blacklist = ["official", "video", "mp3", "hd", "(", ")","[", "]", "audio", "ft.", "lyric", "|", "title", "song", "-", "vod", "1080p", "4k"]
    for word in blacklist:
        title = title.replace(word, '')

    # print(title)
    title = ' '.join(title.split())
    return title

def get_lyircs(title):
    url = f"https://www.google.com/search?q={title.replace(' ', '+')}+lyrics"
    r = requests.get(url)
    soup = BeautifulSoup (r.text, features="lxml")
    mydivs = soup.find_all("div", {"class": "BNeawe tAd8D AP7Wnd"})
    if len(mydivs) < 2:
        print(f"sorry could not find the lyrics for {title}") 
        mydivs = soup.find_all("div", {"class": "kCrYT"})
        links = []
        for x in mydivs:
            if x.a:
                links.append(x.a['href'][7:])
                for x in links:
                    if "youtube" not in x and "download" not in x:
                        link = x
                        break

        link = link.split('&')[0]
        os.system(f'w3m {link}')



        exit()
    s = mydivs[-2].text
    for line in s.split('\n'):
        print(line.center(shutil.get_terminal_size().columns))

if __name__ == '__main__':
    title = get_title()
    title = clean_title(title)
    print(f"Fetching lyrics for {title}\n")
    get_lyircs(title)


