import requests
from bs4 import BeautifulSoup
from datetime import datetime


class chart():
    def mainCahrt(self):

        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
        req = requests.get('https://www.melon.com/chart/index.htm', headers=header)
        html = req.text
        parse = BeautifulSoup(html, 'html.parser')

        titles = parse.find_all("div", {"class": "ellipsis rank01"})
        songs = parse.find_all("div", {"class": "ellipsis rank02"})

        title = []
        song = []

        for t in titles:
            title.append(t.find('a').text)

        for s in songs:
            song.append(s.find('span', {"class": "checkEllipsis"}).text)

        now = datetime.now()
        CharL = []
        mainChart = '🎧 {}년 {}월 {}일 {}시 기준 실시간 차트 입니다! (멜론) 🎧\n\n'.format(now.year, now.month, now.day, now.hour)
        for i in range(100):
            CharL.append((str(i+1), title[i], song[i]))
            a = '%3d위: %s - %s' % (i + 1, title[i], song[i]) + '\n'
            mainChart += a
        return mainChart

    def balladChart(self):
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
        req = requests.get('https://music.bugs.co.kr/chart/track/day/nb', headers=header)
        html = req.text
        parse = BeautifulSoup(html, 'html.parser')

        titles = parse.find_all("p", {"class": "title"})
        songs = parse.find_all("p", {"class": "artist"})

        title = []
        artist = []

        for s in titles:
            title.append(s.find('a').text)

        for a in songs:
            artist.append(a.find('a').text)

        CharL = []
        balladChart = '🎧 오늘의 발라드 차트 입니다 (벅스 기준) 🎧\n\n'
        for i in range(100):
            CharL.append((str(i + 1), title[i], artist[i]))
            a = '%3d위: %s - %s' % (i + 1, title[i], artist[i]) + '\n'
            balladChart += a
        return balladChart

    def idolChart(self):
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
        req = requests.get('https://music.bugs.co.kr/chart/track/day/nid', headers=header)
        html = req.text
        parse = BeautifulSoup(html, 'html.parser')

        titles = parse.find_all("p", {"class": "title"})
        songs = parse.find_all("p", {"class": "artist"})

        title = []
        artist = []

        for s in titles:
            title.append(s.find('a').text)

        for a in songs:
            artist.append(a.find('a').text)

        CharL = []
        idolChart = '🎧 오늘의 아이돌 차트 입니다 (벅스 기준) 🎧\n\n'
        for i in range(100):
            CharL.append((str(i + 1), title[i], artist[i]))
            a = '%3d위: %s - %s' % (i + 1, title[i], artist[i]) + '\n'
            idolChart += a
        return idolChart

    def hiphopChart(self):
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
        req = requests.get('https://music.bugs.co.kr/chart/track/day/nrh', headers=header)
        html = req.text
        parse = BeautifulSoup(html, 'html.parser')

        titles = parse.find_all("p", {"class": "title"})
        songs = parse.find_all("p", {"class": "artist"})

        title = []
        artist = []

        for s in titles:
            title.append(s.find('a').text)

        for a in songs:
            artist.append(a.find('a').text)

        CharL = []
        hhChart = '🎧 오늘의 힙합 차트 입니다 (벅스 기준) 🎧\n\n'
        for i in range(100):
            CharL.append((str(i + 1), title[i], artist[i]))
            a = '%3d위: %s - %s' % (i + 1, title[i], artist[i]) + '\n'
            hhChart += a
        return hhChart

    def billboardChart(self):
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
        req = requests.get('https://www.billboard.com/charts/hot-100', headers=header)
        html = req.text
        parse = BeautifulSoup(html, 'html.parser')

        titles = parse.find_all("span", {"class": "chart-element__information__song text--truncate color--primary"})
        artists = parse.find_all("span",
                                 {"class": "chart-element__information__artist text--truncate color--secondary"})

        title = []
        artist = []

        for s in titles:
            title.append(s.text)

        for a in artists:
            artist.append(a.text)

        CharL = []
        billboardChart = '🎧 이번주 🎙빌보드🎙 hot 100 차트 입니다 🎧\n\n'
        for i in range(100):
            CharL.append((str(i + 1), title[i], artist[i]))
            a = '%3d위: %s - %s' % (i + 1, title[i], artist[i]) + '\n'
            billboardChart += a
        return billboardChart

    def metalChart(self):
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
        req = requests.get(
            'https://www.melon.com/chart/style/index.htm?styleCd=GN1006#params%5Bidx%5D=1&params%5BstartDay%5D=20191125&params%5BendDay%5D=20191201&params%5BisFirstDate%5D=false&params%5BisLastDate%5D=true',
            headers=header)
        html = req.text
        parse = BeautifulSoup(html, 'html.parser')

        titles = parse.find_all("div", {"class": "ellipsis rank01"})
        songs = parse.find_all("div", {"class": "ellipsis rank02"})

        title = []
        song = []

        for t in titles:
            title.append(t.find('a').text)

        for s in songs:
            song.append(s.find('span', {"class": "checkEllipsis"}).text)

        CharL = []
        metalChart = '🎧 이번주 헤비메탈 차트 입니다 (멜론 기준) 🎧\n\n'
        for i in range(100):
            CharL.append((str(i + 1), title[i], song[i]))
            a = '%3d위: %s - %s' % (i + 1, title[i], song[i]) + '\n'
            metalChart += a
        return metalChart
