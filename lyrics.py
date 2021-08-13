#! /usr/bin/env python3

import requests
from urllib.parse import unquote
from bs4 import BeautifulSoup

import argparse
import os
import sys
import dbus
import shutil


ex = 0
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}


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
    blacklist = ["official", "video", "mp3", "hd", "(", ")","[", "]", "audio", "ft.", "lyric","lyrical", "|", "title", "song", "-", "vod", "1080p", "4k", "720p", "hd remastered", "hit songs"]
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
        print("Could not find the lyrics in google") 
        mydivs = soup.find_all("div", {"class": "kCrYT"})
        links = []
        for x in mydivs:
            if x.a:
                links.append(x.a['href'][7:])
                for x in links:
                    if "youtube" not in x and "download" not in x and "ie=UTF-8" not in x:
                        link = x
                        break

        link = unquote(link)
        link = link.split('&')[0]

        print(f"Opening {link}")

        if ex:
            r = requests.get(link, headers=headers)
            soup = BeautifulSoup (r.text, features="lxml")
            # print(soup)

            delete_elements = ["label", "button", "a", "input", "script", "form", "header", "footer", "style", "link", "meta"]
            for element in delete_elements:
                [x.extract() for x in soup.findAll(element)]

            # print(soup)
            new = "\n".join(item for item in soup.getText().split('\n') if item)
            # print(new)
            # print(soup.getText())
            for line in new.split('\n'):
                print(line.center(shutil.get_terminal_size().columns))
        else:
            os.system(f'w3m -o auto_image=FALSE {link}')

        exit()
    s = mydivs[-2].text
    for line in s.split('\n'):
        print(line.center(shutil.get_terminal_size().columns))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get Lyrics of currently playing song')
    parser.add_argument("-e", "--Experimental", help = "Show Experimental lyrics parser", action="store_true")
    args = parser.parse_args()

    if args.Experimental:
        ex = 1

    title = get_title()
    title = clean_title(title)
    print(f"Fetching lyrics..\n")
    get_lyircs(title)
