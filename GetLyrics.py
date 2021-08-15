#! /usr/bin/env python3

import requests
from urllib.parse import unquote, urlparse
from bs4 import BeautifulSoup

import argparse
import os
import sys
import importlib
import dbus
import shutil

from sites import site_info
import sites

class GetLyrics:
    def __init__(self):
        parser = argparse.ArgumentParser(description='Get Lyrics of currently playing song')
        parser.add_argument("-e", "--experimental", help = "Use Experimental lyrics parser", action="store_true")
        args = parser.parse_args()

        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
        self.experimental = args.experimental
        self.title = self.get_title()
        self.lyrics = ""
        self.google_result_links = []
        self.clean_title()

        if not self.get_google_lyrics():
            print("Could not find the lyrics in google\n\n")
            self.extract_links_from_google_result()
            link = unquote(self.google_result_links[0])
            link = link.split('&')[0]
            if not self.experimental:
                os.system(f'w3m -o auto_image=FALSE {link}')
            else:
                for x in self.google_result_links:
                    base = urlparse(x).netloc
                    if base in site_info.base_urls:
                        site_name = site_info.dic[base]
                        full_module_name = "sites." + site_name
                        mymodule = importlib.import_module(full_module_name)
                        r = requests.get(x.split('&')[0])
                        soup = BeautifulSoup(r.text, features='lxml')
                        print(mymodule.get_lyrics(soup))
                        exit()
                self.generic_extractor(link)

    def get_title(self):
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
        title = metadata['xesam:title']
        if not title:
            print("Cannot fetch title")
            exit()
        return title

    def clean_title(self):
        self.title = self.title.lower()
        blacklist = ["official", "video", "mp3", "hd", "(", ")","[", "]", "audio", "ft.", "feat." "lyric","lyrical", "|", "title", "song", "-", "vod", "1080p", "4k", "720p", "hd remastered", "hit songs", "full video"]
        for word in blacklist:
            self.title = self.title.replace(word, '')

        # print(title)
        self.title = ' '.join(self.title.split())

    def get_google_lyrics(self):
        url = f"https://www.google.com/search?q={self.title.replace(' ', '+')}+lyrics"
        r = requests.get(url)
        self.soup = BeautifulSoup (r.text, features="lxml")
        mydivs = self.soup.find_all("div", {"class": "BNeawe tAd8D AP7Wnd"})
        if len(mydivs) < 2 or "youtube" in mydivs[-2].text:
            return False
        else:
            self.lyrics = mydivs[-2].text
            self.print_lyrics()
            return True

    def print_lyrics(self):
        for line in self.lyrics.split('\n'):
            print(line.center(shutil.get_terminal_size().columns))

    def extract_links_from_google_result(self):
        mydivs = self.soup.find_all("div", {"class": "kCrYT"})
        for x in mydivs:
            if x.a:
                self.google_result_links.append(x.a['href'][7:])
        self.clean_google_result_links()

    def clean_google_result_links(self):
        # blacklist = ["youtube", "download", "ie=UTF-8"]
        # for word in blacklist:
        clean_links = []
        for x in self.google_result_links:
            if "youtube" not in x and "download" not in x and "ie=UTF-8" not in x:
                clean_links.append(x)
        self.google_result_links = clean_links

    def generic_extractor(self, link):
        r = requests.get(link, headers=self.headers)
        soup = BeautifulSoup (r.text, features="lxml")
        delete_elements = ["label", "button", "a", "input", "script", "form", "header", "footer", "style", "link", "meta"]
        for element in delete_elements:
            [x.extract() for x in soup.findAll(element)]

        self.lyrics = "\n".join(item for item in soup.getText().split('\n') if item)
        self.print_lyrics()


if __name__ == '__main__':
    gl = GetLyrics()
