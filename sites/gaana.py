#! /usr/bin/env python3

class gaana:
    def __init__(self):
        self.homepage = "www.gaana.com"
        self.lyrics = ""

    def get_lyrics(self, soup):
        self.lyrics = soup.find_all('div',{'class':'_inner'})[1].text
        return self.lyrics


if __name__ == '__main__':
    import requests
    from bs4 import BeautifulSoup
    m = gaana()
    r = requests.get("https://gaana.com/lyrics/kun-fayakun")
    soup = BeautifulSoup(r.text, features='lxml')
    print(m.get_lyrics(soup))

def get_lyrics(soup):
    lyrics = soup.find_all('div',{'class':'_inner'})[1].text
    return lyrics
