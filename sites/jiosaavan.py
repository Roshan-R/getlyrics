#! /usr/bin/env python3

class jiosaavn:
    def __init__(self):
        self.homepage = "www.jiosaavn.com"
        self.lyrics = ""

    def get_lyrics(self, soup):
        self.lyrics = "\n".join([ x.text for x in soup.find('div', {'class':'u-disable-select'}).find_all('span') ][:-1])
        return self.lyrics


if __name__ == '__main__':
    import requests
    from bs4 import BeautifulSoup
    m = jiosaavn()
    r = requests.get("https://www.jiosaavn.com/lyrics/subhanalla-lyrics/Mg0FehxJe0s")
    soup = BeautifulSoup(r.text, features='lxml')
    print(m.get_lyrics(soup))

def get_lyrics(soup):
    lyrics = "\n".join([ x.text for x in soup.find('div', {'class':'u-disable-select'}).find_all('span') ][:-1])
    return lyrics
