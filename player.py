import os
import sys
import random
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
import requests
from bs4 import BeautifulSoup
from playersub import *
from Chart import chart
import youtube_dl
from downCr import musicCr
from equalizer_bar import EqualizerBar

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)


class Player(QWidget):

    def __init__(self):
        super().__init__()
        self.player = CPlayer(self)
        self.playlist = []
        self.selectedList = [0]
        self.playOption = QMediaPlaylist.Sequential
        self.strChart = chart
        self._background_color = QtGui.QColor('#D4F4FA')
        self.setWindowTitle('플레이어')
        self.initUI()

    def initUI(self):

        vbox = QVBoxLayout()

        # 재생목록
        box = QVBoxLayout()
        gb = QGroupBox('재생목록')
        vbox.addWidget(gb)

        self.table = QTableWidget(0, 2, self)
        headerLabel = ['노래제목', '감상률']
        self.table.setHorizontalHeaderLabels(headerLabel)
        self.table.horizontalHeader().setSectionResizeMode(0,QHeaderView.Stretch)
        # read only
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # single row selection
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        # signal
        self.table.itemSelectionChanged.connect(self.tableChanged)
        self.table.itemDoubleClicked.connect(self.tableDbClicked)
        box.addWidget(self.table)

        hbox = QHBoxLayout()
        btnDownload = QPushButton('노래 다운')
        btnAdd = QPushButton('노래 추가')
        btnDel = QPushButton('노래 삭제')
        btnLyrics = QPushButton('현재 노래 가사')
        btnDownload.clicked.connect(self.showDown)
        btnAdd.clicked.connect(self.addList)
        btnDel.clicked.connect(self.delList)
        btnLyrics.clicked.connect(self.lyricsMsg)
        hbox.addWidget(btnDownload)
        hbox.addWidget(btnAdd)
        hbox.addWidget(btnDel)
        hbox.addWidget(btnLyrics)

        box.addLayout(hbox)
        gb.setLayout(box)

        # 이퀄라이저
        label = QLabel(self)
        label.setText('eq')

        vbox.addWidget(label)
        self.equalizer = EqualizerBar(20, ['##104952', '#225B64', '#346D76', '#467F88', '#6AA3AC', '#8EC7D0', '#A0D9E2',
                                           '#B2EBF4', '#C4FDFF', '#D6FFFF', '#E8FFFF', '#FAFFFF'])

        self._timer = QtCore.QTimer()
        self._timer.stop()
        self._timer.setInterval(10000)
        self._timer.timeout.connect(self.update_values)
        self._timer.start()
        vbox.addWidget(self.equalizer)

        # 재생 컨트롤
        box = QHBoxLayout()
        gb = QGroupBox('Play Control')
        vbox.addWidget(gb)

        text = ['◀◀', '▶', '⏸', '▶▶', '■']
        grp = QButtonGroup(self)
        for i in range(len(text)):
            btn = QPushButton(text[i], self)
            grp.addButton(btn, i)
            box.addWidget(btn)
        grp.buttonClicked[int].connect(self.btnClicked)

        # Volume
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setRange(0, 100)
        self.slider.setValue(50)
        self.slider.valueChanged[int].connect(self.volumeChanged)
        box.addWidget(self.slider)
        gb.setLayout(box)


        # 재생 옵션
        box = QHBoxLayout()
        gb = QGroupBox('Play Option')
        vbox.addWidget(gb)

        str = ['현재음악(1회재생)', '현재음악(반복)', '순서재생', '반복재생', '랜덤재생']
        grp = QButtonGroup(self)
        for i in range(len(str)):
            btn = QRadioButton(str[i], self)
            if i == QMediaPlaylist.Sequential:
                btn.setChecked(True)
            grp.addButton(btn, i)
            box.addWidget(btn)

        grp.buttonClicked[int].connect(self.radClicked)

        gb.setLayout(box)

        # 차트
        bbox = QVBoxLayout()
        gb = QGroupBox('음악차트')
        vbox.addWidget(gb)
        box = QHBoxLayout()
        str = ['실시간', '빌보드', '발라드', '아이돌', '힙합', '락/메탈']
        grp = QButtonGroup(self)
        for i in range(len(str)):
            btn = QPushButton(str[i], self)
            grp.addButton(btn, i)
            box.addWidget(btn)

        grp.buttonClicked[int].connect(self.chartClicked)

        self.tt = QTextBrowser(self)
        data = chart.mainCahrt(self)
        self.tt.append(data)

        bbox.addLayout(box)
        bbox.addWidget(self.tt)
        gb.setLayout(bbox)

        self.setLayout(vbox)
        self.show()

    # 다운로드 기능
    def showDown(self):
        d = QDialog()
        d.setWindowTitle('⬇다운로드⬇')
        d.setGeometry(100, 100,200,100)

        layout = QVBoxLayout()
        layout.addStretch(1)

        edit = QTextEdit()
        font = edit.font()
        font.setPointSize(20)
        edit.setFont(font)
        self.edit = edit
        layout.addWidget(edit)
        subLayout = QHBoxLayout()

        btnSearch = QPushButton("검색")
        btnSearch.clicked.connect(self.search)

        btnDown = QPushButton("다운로드")
        btnDown.clicked.connect(self.musicDown)

        subLayout.addWidget(btnSearch)
        subLayout.addWidget(btnDown)
        layout.addLayout(subLayout)

        layout.addStretch(1)
        d.setLayout(layout)
        d.exec_()

    def search(self):
        inputSong = self.edit.toPlainText()
        msg = """
        📽 검색결과입니다 📽
        입력한 노래: {}
        다운받을 노래 제목: {}

        --------------
        다운 받으려는 노래가 아니라면 가수 제목과 함께 재검색 해주세요.
        [예시] 뮤즈 싸이코""".format(inputSong, musicCr.getSong(self, inputSong))

        lMsg = QMessageBox(self)
        lMsg.about(self, '안내', msg)

    def musicDown(self):
        inputSong = self.edit.toPlainText()
        originPath = os.getcwd()
        os.chdir("..")
        os.chdir("..")
        if os.path.isdir('ADplayer') == False:
            os.makedirs('ADplayer')
        outDir = os.getcwd() + '/ADplayer'
        os.chdir(outDir)
        path = os.path.join(outDir, '%(inputSong)s.%(ext)s')

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': path,
            'postprocessors': [
                {'key''': 'FFmpegExtractAudio',
                 'preferredcodec': 'mp3',
                 'preferredquality': '192',
                 },
                {'key': 'FFmpegMetadata'},
            ],
        }

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([musicCr.getURL(self, inputSong)])
                ssMsg = QMessageBox(self)
                msg = '다운로드 성공!❤ \n🎵 파일 이름: {}.mp3\n💿 저장 경로: {}'.format(inputSong, outDir)
                ssMsg.about(self, '🎶', msg)
        except youtube_dl.utils.DownloadError as err:
            lMsg = QMessageBox(self)
            lMsg.about(self, '에러', '다운로드 에러')
            self.edit.setText('')
            print(err)
        dirList = os.listdir(outDir)
        for i in dirList:
            if i == 'NA.mp3':
                name = i.replace("NA", inputSong)
                os.rename(i, name)
        os.chdir(originPath)

    # 차트기능
    def chartClicked(self, chart):
        if chart == 0:
            self.tt.clear()
            data = self.strChart.mainCahrt(self)
            self.tt.append(data)
        elif chart == 1:
            self.tt.clear()
            data = self.strChart.billboardChart(self)
            self.tt.append(data)
        elif chart == 2:
            self.tt.clear()
            data = self.strChart.balladChart(self)
            self.tt.append(data)
        elif chart == 3:
            self.tt.clear()
            data = self.strChart.idolChart(self)
            self.tt.append(data)
        elif chart == 4:
            self.tt.clear()
            data = self.strChart.hiphopChart(self)
            self.tt.append(data)
        else:
            self.tt.clear()
            data = self.strChart.metalChart(self)
            self.tt.append(data)

    # 선택한 값 변화시
    def tableChanged(self):
        self.selectedList.clear()
        for item in self.table.selectedIndexes():
            self.selectedList.append(item.row())

        self.selectedList = list(set(self.selectedList))

        if self.table.rowCount() != 0 and len(self.selectedList) == 0:
            self.selectedList.append(0)

    # 노래 추가
    def addList(self):
        originPath = os.getcwd()
        os.chdir("..")
        os.chdir("..")
        if os.path.isdir('ADplayer') == False:
            os.makedirs('ADplayer')
        outDir = os.getcwd() + '/ADplayer'
        os.chdir(outDir)
        files = QFileDialog.getOpenFileNames(self
                                             , 'Select one or more files to open'
                                             , ''
                                             , 'Sound (*.mp3 *.wav *.ogg *.flac *.wma)')
        cnt = len(files[0])
        a = str(files[0])
        a = a[2:-6]
        x = a.split('/')
        songname = x[-1]

        row = self.table.rowCount()
        self.table.setRowCount(row + cnt)
        os.chdir(originPath)

        for i in range(row, row + cnt):
            self.table.setItem(i, 0, QTableWidgetItem(songname))
            pbar = QProgressBar(self.table)
            pbar.setAlignment(Qt.AlignCenter)
            self.table.setCellWidget(i, 1, pbar)
        self.createPlaylist()

    # 노래 삭제
    def delList(self):
        row = self.table.rowCount()

        index = []
        for item in self.table.selectedIndexes():
            index.append(item.row())

        index = list(set(index))
        index.reverse()
        for i in index:
            self.table.removeRow(i)

        self.createPlaylist()

    # 재생 도구 기능 구현
    def btnClicked(self, id):
        if id == 0:  # ◀◀
            self.player.prev()
        elif id == 1:  # ▶
            if self.table.rowCount() > 0:
                self.player.play(self.playlist, self.selectedList[0], self.playOption)
            self._timer.setInterval(80)
            self._timer.timeout.connect(self.update_values)
            self._timer.start()
        elif id == 2:  # ⏸
            self.player.pause()
            self._timer.stop()
        elif id == 3:  # ▶▶
            self.player.next()
        else:  # ■
            self.player.stop()
            self._timer.stop()

    # 가사 크롤링
    def lyricsCr(self, songname):
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
        req = requests.get(
            'https://www.melon.com/search/song/index.htm?q={}&section=song&searchGnbYn=Y&kkoSpl=N&kkoDpType=&ipath=srch_form'.format(
                songname), headers=header)
        html = req.text
        parse = BeautifulSoup(html, 'html.parser')
        lysNum = parse.find_all('a', {'class': 'btn btn_icon_detail'})
        s = ''
        for i in str(lysNum[0]):
            if i.isdigit() == True:
                s += i
        s = s[:len(s) // 2]

        req2 = requests.get('https://www.melon.com/song/detail.htm?songId={}'.format(s), headers=header)
        html2 = req2.text
        parse = BeautifulSoup(html2, 'html.parser')
        lyrics = parse.find_all("div", {"class": "lyric"})
        artist = parse.find_all("a", {"class": "artist_name"})
        l = str(lyrics)
        l = l[75:-7]
        for i in l:
            if i == '\t':
                l = l[1:]
        artist = artist[0].find('span').text
        lenErrorcheck = len(lyrics)
        if lenErrorcheck == 0:
            print('Error')
            errMsg = QMessageBox(self)
            errMsg.about(self, '에러', '에러!!!')
            self.edit.setText('')
        st = ''
        for i in lyrics:
            a = l.split('<br/>')
            for j in a:
                if i == ' ':
                    st += '\n'
                else:
                    st += j + '\n'
        gasa = songname + '-' + artist + '\n\n' + st

        lyricsMsg = QDialog()
        lyricsMsg.setWindowTitle('가사')
        layout = QVBoxLayout()
        layout.addStretch(1)

        edit = QTextBrowser()
        edit.append(gasa)
        layout.addWidget(edit)


        layout.addStretch(1)
        lyricsMsg.setLayout(layout)
        lyricsMsg.exec_()

    # 가사 버튼 이벤트
    def lyricsMsg(self):
        idx = self.selectedList[0]
        song = self.playlist[idx][:-4]
        song = song.split('/')
        self.lyricsCr(song[-1])

    # 더블클릭시 재생
    def tableDbClicked(self, e):
        self.player.play(self.playlist, self.selectedList[0], self.playOption)

    # 볼륨 조절
    def volumeChanged(self):
        self.player.upateVolume(self.slider.value())

    def radClicked(self, id):
        self.playOption = id
        self.player.updatePlayMode(id)

    # 배경 색 입히기
    def paintEvent(self, e):
        self.table.setColumnWidth(0, self.table.width() * 0.7)
        self.table.setColumnWidth(1, self.table.width() * 0.2)

    # 재생 리스트 생성
    def createPlaylist(self):
        self.playlist.clear()
        for i in range(self.table.rowCount()):
            self.playlist.append('/home/hyerin/ADplayer/' + self.table.item(i, 0).text() + '.mp3')

    # 미디어 값 변화시
    def updateMediaChanged(self, index):
        if index >= 0:
            self.table.selectRow(index)

    def updateDurationChanged(self, index, msec):
        self.pbar = self.table.cellWidget(index, 1)
        if self.pbar:
            self.pbar.setRange(0, msec)

    def updatePositionChanged(self, index, msec):
        self.pbar = self.table.cellWidget(index, 1)
        if self.pbar:
            self.pbar.setValue(msec)

    # 색 입히기
    def paintEvent(self, e):
        self.table.setColumnWidth(0, self.table.width() * 0.7)
        self.table.setColumnWidth(1, self.table.width() * 0.2)

    def paintEvent(self, e):
        painter = QtGui.QPainter(self)
        brush = QtGui.QBrush()
        brush.setColor(self._background_color)
        brush.setStyle(Qt.SolidPattern)
        rect = QtCore.QRect(0, 0, painter.device().width(), painter.device().height())
        painter.fillRect(rect, brush)

    # 이퀄라이저 조절
    def update_values(self):
        self.equalizer.setValues([
            min(100, v+random.randint(0, 50) if random.randint(0, 5) > 2 else v)
            for v in self.equalizer.values()
            ])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Player()
    sys.exit(app.exec_())