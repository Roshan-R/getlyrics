#! /usr/bin/env python3

class lyricsgyan:
    def __init__(self):
        self.homepage = "www.lyricsgyan.com"
        self.lyrics = ""

    def get_lyrics(self, soup):
        self.lyrics = soup.find_all('div',{'class':'entry-content'})[0].text
        return self.lyrics


if __name__ == '__main__':
    import requests
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
    from bs4 import BeautifulSoup
    m = lyricsgyan()
    r = requests.get("https://www.lyricsgyan.com/2020/01/tera-chehra-lyrics-hindi-english-adnan-sami.html", headers=headers)
    soup = BeautifulSoup(r.text, features='lxml')
    print(m.get_lyrics(soup))

def get_lyrics(soup):
    lyrics = soup.find_all('div',{'class':'entry-content'})[0].text
    return lyrics
