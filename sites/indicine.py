#! /usr/bin/env python3

class indicine:
    def __init__(self):
        self.homepage = "www.indicine.com"
        self.lyrics = ""

    def get_lyrics(self, soup):
        # self.lyrics = soup.find_all('div',{'class':'_inner'})[1].text
        self.lyrics = soup.find_all('div',{'class':'entry-content'})[0].text
        return self.lyrics


if __name__ == '__main__':
    import requests
    from bs4 import BeautifulSoup
    m = indicine()
    r = requests.get("https://www.indicine.com/movies/bollywood/khwaja-mere-khwaja-lyrics-jodhaa-akbar/")
    soup = BeautifulSoup(r.text, features='lxml')
    print(m.get_lyrics(soup))

def get_lyrics(soup):
    lyrics = soup.find_all('div',{'class':'entry-content'})[0].text
    return lyrics
