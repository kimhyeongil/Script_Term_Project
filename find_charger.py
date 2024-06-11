from tkinter import *
import requests
from telepot.loop import MessageLoop

import Data
import telegram
from GraphFrame import GraphFrame
from SearchFrame import SearchFrame
from bookmarkFrame import BookmarkFrame


class MainGUI:
    def __init__(self):
        self.window = Tk()
        self.window.title('Find Charger')
        self.window.geometry('1024x624')

        self.url = "https://bigdata.kepco.co.kr/openapi/v1/EVcharge.do"
        self.key = "GqAUvg9r8nJl20eWk533DCrJwwcbm81kst6Z0fEW"

        params = {
            "metroCd": 31,
            "apiKey": self.key
        }

        Data.chargeInfos = {city: [] for city in Data.cities.keys()}
        ret = requests.get(self.url, params=params).json()['data']

        for data in ret:
            for city in Data.cities.keys():
                if data['city'] in Data.cities[city]:
                    Data.chargeInfos[city].append(data)

        self.initMenu()

        self.searchFrame = SearchFrame(self.window, width=1024 - 215, height=624)
        self.graphFrame = GraphFrame(self.window, width=1024 - 215, height=624)
        self.bookmarkFrame = BookmarkFrame(self.window, width=1024 - 215, height=624)
        self.selected = self.searchFrame
        self.selected.place(x=215, y=10)

        MessageLoop(telegram.bot, telegram.handle).run_as_thread()

        self.window.mainloop()

    def initMenu(self):
        self.menuFrame = Frame(self.window)
        searchImg = PhotoImage(file='검색창.png')
        self.searchButton = Button(self.menuFrame, text='검색', bg='white', image=searchImg,
                                   command=lambda: self.changeFrame(self.searchFrame))
        self.searchButton.image = searchImg
        self.searchButton.grid(row=1, column=0, padx=7, pady=7)

        bookmarkImg = PhotoImage(file='즐겨찾기창.png')
        self.bookmarkButton = Button(self.menuFrame, text='즐찾', bg='white', image=bookmarkImg,
                                     command=lambda: self.changeFrame(self.bookmarkFrame))
        self.bookmarkButton.image = bookmarkImg
        self.bookmarkButton.grid(row=2, column=0, padx=7, pady=7)

        graphImg = PhotoImage(file='그래프창.png')
        self.graphButton = Button(self.menuFrame, text='그래프', bg='white', image=graphImg,
                                  command=lambda: self.changeFrame(self.graphFrame))
        self.graphButton.image = graphImg
        self.graphButton.grid(row=3, column=0, padx=7, pady=7)

        self.menuFrame.place(x=25, y=50)

    def changeFrame(self, frame):
        if frame != self.selected:
            print('change')
            self.selected.place_forget()
            frame.place(x=215, y=10)
            self.selected = frame
            self.selected.OnEnable()


MainGUI()
