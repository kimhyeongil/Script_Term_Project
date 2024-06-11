import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tkinter import *
from tkinter import simpledialog, messagebox

from tkintermapview import TkinterMapView

import Data
import kakaomap


class BookmarkFrame(Frame):
    def __init__(self, master, **args):
        super().__init__(**args)
        self.isGraph = True
        self.page = 0
        self.index = None
        self.initWidget()

    def OnEnable(self):
        self.isGraph = True
        self.page = 0
        self.index = None
        self.showChargeList()
        self.mapButton['image'] = self.mapImg
        self.infoCanvas.place(x=300, y=5)
        self.mapView.place_forget()
        self.showGraph()

    def initWidget(self):
        self.chargeLabels = [Label(self, width=28, height=4, wraplength=240,
                                   font=('arial', 12, 'bold'), anchor="nw", justify="left",
                                   bg='#f9f6f2' if i & 1 else '#D3D3D3')
                             for i in range(6)]

        for i in range(len(self.chargeLabels)):
            self.chargeLabels[i].bind("<Button-1>", lambda event, index=i: self.OnClickInfoListLabel(event, index))
            self.chargeLabels[i].place(x=0, y=50 + (i * 20 * 4))

        prevImg = PhotoImage(file='왼쪽이동.png')
        self.prevButton = Button(self, bg='white', image=prevImg, command=self.prevPage)
        self.prevButton.image = prevImg
        self.prevButton.place(x=72, y=50 + (6 * 20 * 4))

        nextImg = PhotoImage(file='오른쪽이동.png')
        self.nextButton = Button(self, bg='white', image=nextImg, command=self.nextPage)
        self.nextButton.image = nextImg
        self.nextButton.place(x=146, y=50 + (6 * 20 * 4))

        self.infoCanvas = Canvas(self, width=500, height=500, bg='white')
        self.mapView = TkinterMapView(self, width=500, height=500, corner_radius=0)

        self.infoCanvas.place(x=300, y=5)

        mailImg = PhotoImage(file='이메일.png')
        self.mailButton = Button(self, bg='white', image=mailImg, command=self.sendMail)
        self.mailButton.image = mailImg
        self.mailButton.place(x=490, y=515)

        self.mapImg = PhotoImage(file='지도.png')
        self.smallGraphImg = PhotoImage(file='그래프.png')
        self.mapButton = Button(self, bg='white', image=self.mapImg, command=self.changeInfoType)
        self.mapButton.place(x=340, y=515)

        telegramImg = PhotoImage(file='텔레그램.png')
        self.telegramButton = Button(self, bg='white', image=telegramImg)
        self.telegramButton.image = telegramImg
        self.telegramButton.place(x=640, y=515)

    def showChargeList(self):
        for i in range(len(self.chargeLabels)):
            index = i + self.page * len(self.chargeLabels)
            if index < len(Data.bookmarkCities):
                self.chargeLabels[i][
                    'text'] = f"주소: {Data.bookmarkCities[index]['stnAddr']}\n장소: {Data.bookmarkCities[index]['stnPlace']}"
            else:
                self.chargeLabels[i]['text'] = ''

    def OnClickInfoListLabel(self, event, index):
        if index + self.page * len(self.chargeLabels) < len(Data.bookmarkCities):
            self.index = index + self.page * len(self.chargeLabels)
            if self.isGraph:
                self.showGraph()
            else:
                self.showChargeMap()

    def showGraph(self):
        self.infoCanvas.delete('all')
        if not self.index:
            return

        offset = int(self.infoCanvas['height']) - 50
        height = 35

        rapidCnt = Data.bookmarkCities[self.index]['rapidCnt']
        self.infoCanvas.create_rectangle(100, offset, 200, offset - height * rapidCnt, fill='red')
        self.infoCanvas.create_text(106, offset + 20, text='급속 충전기',
                                    anchor="w", font=('consolas', 12, 'bold'))
        self.infoCanvas.create_text(150, offset - height * rapidCnt - 20, text=str(rapidCnt),
                                    font=('consolas', 12, 'bold'))

        slowCnt = Data.bookmarkCities[self.index]['slowCnt']
        self.infoCanvas.create_rectangle(300, offset, 400,
                                         offset - height * slowCnt,
                                         fill='red')
        self.infoCanvas.create_text(306, offset + 20, text='완속 충전기',
                                    anchor="w", font=('consolas', 12, 'bold'))
        self.infoCanvas.create_text(350, offset - height * slowCnt - 20, text=str(slowCnt),
                                    font=('consolas', 12, 'bold'))

        self.infoCanvas.create_text(10, 20, text=Data.bookmarkCities[self.index]['stnAddr'],
                                    anchor="w", font=('consolas', 12, 'bold'))

    def showChargeMap(self):
        self.infoCanvas.delete('all')

        center = kakaomap.geocode(Data.bookmarkCities[self.index]['stnAddr'])
        self.mapView.set_position(*center)
        for city in Data.bookmarkCities:
            addr = city['stnAddr']
            self.mapView.set_marker(*kakaomap.geocode(addr))

    def changeInfoType(self):
        self.isGraph = not self.isGraph
        if self.isGraph:
            self.mapButton['image'] = self.mapImg
            self.infoCanvas.place(x=300, y=5)
            self.mapView.place_forget()
            self.showGraph()
        else:
            self.mapButton['image'] = self.smallGraphImg
            self.infoCanvas.place_forget()
            self.mapView.place(x=300, y=5)
            self.showChargeMap()

    def sendMail(self):
        receiver_email = simpledialog.askstring("입력", "이메일을 입력하세요:")
        # 보낼 이메일 계정 정보
        sender_email = "alfkcjstk853@tukorea.ac.kr"
        password = "ylkc fzte deio jcif"

        # 이메일 내용 작성
        message = MIMEMultipart("alternative")
        message["Subject"] = "즐겨찾기 충전소 정보"
        message["From"] = sender_email
        message["To"] = receiver_email

        # 이메일 내용 추가 (plain text)
        for city in Data.bookmarkCities:
            text = '주소: ' + city['stnAddr'] + '\n'
            text += '장소: ' + city['stnPlace'] + '\n'
            text += '급속 충전기: ' + str(city['rapidCnt']) + '\n'
            text += '완속 충전기: ' + str(city['slowCnt']) + '\n'
        # 이메일 내용 설정
        part1 = MIMEText(text, "plain")

        # 이메일에 내용 추가
        message.attach(part1)

        # Gmail 서버와 연결
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())

        messagebox.showinfo("완료", "이메일을 발송했습니다.")

    def nextPage(self):
        self.page = min(self.page + 1,
                        (len(Data.bookmarkCities) - 1) // len(self.chargeLabels))
        self.showChargeList()

    def prevPage(self):
        self.page = max(self.page - 1, 0)
        self.showChargeList()
