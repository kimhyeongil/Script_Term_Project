from tkinter import *
from tkinter import messagebox, simpledialog
from tkinter.ttk import Combobox

import requests
from tkintermapview import TkinterMapView
from kakaomap import KakaoMap

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class MainGUI:
    def __init__(self):
        self.window = Tk()
        self.window.title('Find Charger')
        self.window.geometry('1024x624')

        self.url = "https://bigdata.kepco.co.kr/openapi/v1/EVcharge.do"
        self.key = "GqAUvg9r8nJl20eWk533DCrJwwcbm81kst6Z0fEW"

        self.kakaomap = KakaoMap('0573ceea6c41a38389f3ab94d86e8482')
        self.cities = {'가평군': ['가평군'], '고양시': ['고양시 덕양구', '고양시 일산동구', '고양시 일산서구'],
                       '과천시': ['과천시'], '광명시': ['광명시'], '광주시': ['광주시'], '구리시': ['구리시'],
                       '군포시': ['군포시'], '김포시': ['김포시'], '남양주시': ['남양주시'], '동두천시': ['동두천시'],
                       '부천시': ['부천시'], '성남시': ['성남시 분당구', '성남시 수정구', '성남시 중원구'],
                       '수원시': ['수원시 권선구', '수원시 영통구', '수원시 장안구', '수원시 팔달구'],
                       '시흥시': ['시흥시'], '안산시': ['안산시 단원구', '안산시 상록구'], '안성시': ['안성시'],
                       '안양시': ['안양시 동안구', '안양시 만안구'], '양주시': ['양주시'], '양평군': ['양평군'],
                       '여주시': ['여주시'], '연천군': ['연천군'], '오산시': ['오산시'],
                       '용인시': ['용인시 기흥구', '용인시 수지구', '용인시 처인구'], '의왕시': ['의왕시'],
                       '의정부시': ['의정부시'], '이천시': ['이천시'], '파주시': ['파주시'], '평택시': ['평택시'],
                       '포천시': ['포천시'], '하남시': ['하남시'], '화성시': ['화성시']}
        self.page = 0

        params = {
            "metroCd": 31,
            "apiKey": self.key
        }

        ret = requests.get(self.url, params=params).json()['data']

        self.chargeInfos = {city: [] for city in self.cities.keys()}
        for data in ret:
            for city in self.cities.keys():
                if data['city'] in self.cities[city]:
                    self.chargeInfos[city].append(data)

        self.isGraph = True

        self.initMenu()
        self.initSearch()

        self.window.mainloop()

    def showChargeList(self):
        city = self.cityCombobox.get()
        for i in range(len(self.chargeLabels)):
            index = i + self.page * len(self.chargeLabels)
            if index < len(self.chargeInfos[city]):
                self.chargeLabels[i][
                    'text'] = f"주소: {self.chargeInfos[city][index]['stnAddr']}\n장소: {self.chargeInfos[city][index]['stnPlace']}"
            else:
                self.chargeLabels[i]['text'] = ''

    def OnComboboxSelect(self, event):
        self.page = 0
        self.showChargeList()

    def OnClickInfoListLabel(self, event, index):
        city = self.cityCombobox.get()

        if city in self.cities:
            if index + self.page * len(self.chargeLabels) < len(self.chargeInfos[city]):
                self.index = index + self.page * len(self.chargeLabels)
                if self.isGraph:
                    self.showGraph()
                else:
                    self.showChargeMap()

    def showGraph(self):
        city = self.cityCombobox.get()
        self.infoCanvas.delete('all')

        offset = int(self.infoCanvas['height']) - 50
        height = 35

        rapidCnt = self.chargeInfos[city][self.index]['rapidCnt']
        self.infoCanvas.create_rectangle(100, offset, 200, offset - height * rapidCnt, fill='red')
        self.infoCanvas.create_text(106, offset + 20, text='급속 충전기',
                                    anchor="w", font=('consolas', 12, 'bold'))
        self.infoCanvas.create_text(150, offset - height * rapidCnt - 20, text=str(rapidCnt),
                                    font=('consolas', 12, 'bold'))

        slowCnt = self.chargeInfos[city][self.index]['slowCnt']
        self.infoCanvas.create_rectangle(300, offset, 400,
                                         offset - height * slowCnt,
                                         fill='red')
        self.infoCanvas.create_text(306, offset + 20, text='완속 충전기',
                                    anchor="w", font=('consolas', 12, 'bold'))
        self.infoCanvas.create_text(350, offset - height * slowCnt - 20, text=str(slowCnt),
                                    font=('consolas', 12, 'bold'))
        self.infoCanvas.create_text(10, 20, text=self.chargeInfos[city][self.index]['stnAddr'],
                                    anchor="w", font=('consolas', 12, 'bold'))

    def showChargeMap(self):
        city = self.cityCombobox.get()
        self.infoCanvas.delete('all')

        center = self.kakaomap.geocode(self.chargeInfos[city][self.index]['stnAddr'])
        self.mapView.set_position(*center)


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
        message["Subject"] = "충전소 정보"
        message["From"] = sender_email
        message["To"] = receiver_email

        city = self.cityCombobox.get()

        # 이메일 내용 추가 (plain text)
        text = '주소: ' + self.chargeInfos[city][self.index]['stnAddr'] + '\n'
        text += '장소: ' + self.chargeInfos[city][self.index]['stnPlace'] + '\n'
        text += '급속 충전기: ' + str(self.chargeInfos[city][self.index]['rapidCnt']) + '\n'
        text += '완속충전기: ' + str(self.chargeInfos[city][self.index]['slowCnt'])
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
        if self.cityCombobox.get() in self.cities:
            self.page = min(self.page + 1,
                            (len(self.chargeInfos[self.cityCombobox.get()]) - 1) // len(self.chargeLabels))
            self.showChargeList()

    def prevPage(self):
        if self.cityCombobox.get() in self.cities:
            self.page = max(self.page - 1, 0)
            self.showChargeList()

    def initMenu(self):
        self.menuFrame = Frame(self.window)
        self.searchImg = PhotoImage(file='검색창.png')
        self.searchButton = Button(self.menuFrame, text='검색', bg='white', image=self.searchImg)
        self.searchButton.grid(row=1, column=0, padx=7, pady=7)

        self.favoriteImg = PhotoImage(file='즐겨찾기창.png')
        self.favoritesButton = Button(self.menuFrame, text='즐찾', bg='white', image=self.favoriteImg)
        self.favoritesButton.grid(row=2, column=0, padx=7, pady=7)

        self.graphImg = PhotoImage(file='그래프창.png')
        self.graphButton = Button(self.menuFrame, text='그래프', bg='white', image=self.graphImg)
        self.graphButton.grid(row=3, column=0, padx=7, pady=7)

        self.menuFrame.place(x=25, y=50)

    def initSearch(self):
        self.searchFrame = Frame(self.window, width=1024, height=624)

        self.cityCombobox = Combobox(self.searchFrame)
        self.cityCombobox.set('시/군')
        self.cityCombobox['values'] = list(self.cities.keys())
        self.cityCombobox.bind("<<ComboboxSelected>>", self.OnComboboxSelect)
        self.cityCombobox.place(x=0, y=10)

        self.chargeLabels = [Label(self.searchFrame, width=28, height=4, wraplength=260,
                                   font=('arial', 12, 'bold'), anchor="nw", justify="left",
                                   bg='#f9f6f2' if i & 1 else '#D3D3D3')
                             for i in range(6)]
        for i in range(len(self.chargeLabels)):
            self.chargeLabels[i].bind("<Button-1>", lambda event, index=i: self.OnClickInfoListLabel(event, index))
            self.chargeLabels[i].place(x=0, y=50 + (i * 20 * 4))

        self.prevImg = PhotoImage(file='왼쪽이동.png')
        self.nextImg = PhotoImage(file='오른쪽이동.png')
        self.prevButton = Button(self.searchFrame, bg='white', image=self.prevImg, command=self.prevPage)
        self.nextButton = Button(self.searchFrame, bg='white', image=self.nextImg, command=self.nextPage)

        self.prevButton.place(x=72, y=50 + (6 * 20 * 4))
        self.nextButton.place(x=146, y=50 + (6 * 20 * 4))

        self.infoCanvas = Canvas(self.searchFrame, width=500, height=500, bg='white')
        self.mapView = TkinterMapView(self.searchFrame, width=500, height=500, corner_radius=0)

        self.infoCanvas.place(x=300, y=5)

        self.mailImg = PhotoImage(file='이메일.png')
        self.mailButton = Button(self.searchFrame, bg='white', image=self.mailImg, command=self.sendMail)
        self.mailButton.place(x=490, y=515)

        self.mapImg = PhotoImage(file='지도.png')
        self.smallGraphImg = PhotoImage(file='그래프.png')
        self.mapButton = Button(self.searchFrame, bg='white', image=self.mapImg, command=self.changeInfoType)
        self.mapButton.place(x=340, y=515)

        self.telegramImg = PhotoImage(file='텔레그램.png')
        self.telegramButton = Button(self.searchFrame, bg='white', image=self.telegramImg)
        self.telegramButton.place(x=640, y=515)

        self.searchFrame.place(x=215, y=10)


MainGUI()
