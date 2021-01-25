import requests
from bs4 import BeautifulSoup

class musicCr:
    def getSong(self, song):
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
        req = requests.get(
            'https://www.youtube.com/results?search_query={}+mv'.format(song),
            headers=header)
        html = req.text
        parse = BeautifulSoup(html, 'html.parser')

        r = parse.find_all("a",
                           {"class": "yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink spf-link"})

        r = str(r[0])
        titleIdx = r.find('>')
        r = r[titleIdx:]
        outSong = r[1:-4]
        return outSong

    def getURL(self, song):
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
        req = requests.get(
            'https://www.youtube.com/results?search_query={}+mv'.format(song),
            headers=header)
        html = req.text
        parse = BeautifulSoup(html, 'html.parser')

        r = parse.find_all("a",
                           {"class": "yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink spf-link"})

        r = str(r[0])
        hrefIdx = r.find('href')
        r = r[hrefIdx:]
        href = ''
        for i in r:
            href += i
            if i == " ":
                break

        href = href[6:-2]
        outputUrl = "https://www.youtube.com" + href
        return outputUrl