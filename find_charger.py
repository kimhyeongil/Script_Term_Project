from tkinter import *
from tkinter.ttk import Combobox

import requests


class MainGUI:
    def __init__(self):
        self.window = Tk()
        self.window.title('Find Charger')
        self.window.geometry('1000x600')

        self.url = "https://bigdata.kepco.co.kr/openapi/v1/EVcharge.do"
        self.key = "GqAUvg9r8nJl20eWk533DCrJwwcbm81kst6Z0fEW"

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

        self.initMenu()
        self.initSearch()

        self.window.mainloop()

    def OnComboboxSelect(self, event):
        city = self.cityCombobox.get()
        for i in range(4):
            self.chargeLabels[i]['text'] = f"주소: {self.chargeInfos[city][i]['stnAddr']}\n장소: {self.chargeInfos[city][i]['stnPlace']}"

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
        self.searchFrame = Frame(self.window, width=1000, height=600)

        self.cityCombobox = Combobox(self.searchFrame)
        self.cityCombobox.set('시/군')
        self.cityCombobox['values'] = list(self.cities.keys())
        self.cityCombobox.bind("<<ComboboxSelected>>", self.OnComboboxSelect)
        self.cityCombobox.place(x=0, y=10)

        self.chargeLabels = [Label(self.searchFrame, width=34, height=7, wraplength=270,
                                   font=('arial', 12, 'bold'), anchor="nw", justify="left",
                                   bg='#f9f6f2' if i & 1 else '#D3D3D3')
                             for i in range(4)]
        for i in range(4):
            self.chargeLabels[i].place(x=0, y=50 + (i * 16 * 7))

        self.prevImg = PhotoImage(file='왼쪽이동.png')
        self.nextImg = PhotoImage(file='오른쪽이동.png')
        self.prevButton = Button(self.searchFrame, bg='white', image=self.prevImg)
        self.nextButton = Button(self.searchFrame, bg='white', image=self.nextImg)

        self.prevButton.place(x=50, y=50 + (4 * 16 * 7))
        self.nextButton.place(x=124, y=50 + (4 * 16 * 7))

        self.infoCanvas = Canvas(self.searchFrame, width=475, height=475, bg='white')
        self.infoCanvas.place(x=275, y=10)

        self.mailImg = PhotoImage(file='이메일.png')
        self.mailButton = Button(self.searchFrame, bg='white', image=self.mailImg)
        self.mailButton.place(x=475, y=500)

        self.mapImg = PhotoImage(file='지도.png')
        self.mapButton = Button(self.searchFrame, bg='white', image=self.mapImg)
        self.mapButton.place(x=325, y=500)

        self.telegramImg = PhotoImage(file='텔레그램.png')
        self.telegramButton = Button(self.searchFrame, bg='white', image=self.telegramImg)
        self.telegramButton.place(x=625, y=500)

        self.searchFrame.place(x=215, y=10)


MainGUI()
