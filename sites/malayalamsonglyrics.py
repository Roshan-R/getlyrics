#! /usr/bin/env python3

class malayalamsonglyrics:
    def __init__(self):
        self.homepage = "http://malayalamsonglyrics.blogspot.com"
        self.lyrics = ""

    def get_lyrics(self, soup):
        divs = soup.find_all('div', {'class':'MsoNormal'})
        for div in divs:
            if div.span:
                self.lyrics = self.lyrics + "\n" + div.span.text
        return self.lyrics


if __name__ == '__main__':
    import requests
    from bs4 import BeautifulSoup
    m = malayalamsonglyrics()
    r = requests.get("https://malayalamsonglyrics.blogspot.com/2013/11/thazhvaram-melake-lyrics-thira.html")
    soup = BeautifulSoup(r.text, features='lxml')
    print(m.get_lyrics(soup))
