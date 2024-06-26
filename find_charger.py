import spam
from tkinter import *
import requests
from telepot.loop import MessageLoop

import Data
import telegram
from GraphFrame import GraphFrame
from SearchFrame import SearchFrame
from BookmarkFrame import BookmarkFrame


class MainGUI:
    def __init__(self):
        self.window = Tk()
        self.window.title('Find Charger')
        self.window.geometry('1024x624')

        self.url = "https://bigdata.kepco.co.kr/openapi/v1/EVcharge.do"
        with open('API키', 'rb') as file:
            self.key = file.read().decode('utf-8')
            self.key = spam.decrypt(self.key)

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
        self.selectedFrame = self.searchFrame
        self.selectedFrame.place(x=215, y=10)


        MessageLoop(telegram.bot, telegram.handle).run_as_thread()

        self.window.mainloop()

    def initMenu(self):
        self.menuFrame = Frame(self.window)
        searchImg = PhotoImage(file='검색창.png')
        self.searchButton = Button(self.menuFrame, text='검색', bg='white', image=searchImg,
                                   command=lambda: self.changeFrame(self.searchFrame, self.searchButton))
        self.searchButton.image = searchImg
        self.searchButton.grid(row=1, column=0, padx=7, pady=7)

        bookmarkImg = PhotoImage(file='즐겨찾기창.png')
        self.bookmarkButton = Button(self.menuFrame, text='즐찾', bg='white', image=bookmarkImg,
                                     command=lambda: self.changeFrame(self.bookmarkFrame, self.bookmarkButton))
        self.bookmarkButton.image = bookmarkImg
        self.bookmarkButton.grid(row=2, column=0, padx=7, pady=7)

        graphImg = PhotoImage(file='그래프창.png')
        self.graphButton = Button(self.menuFrame, text='그래프', bg='white', image=graphImg,
                                  command=lambda: self.changeFrame(self.graphFrame, self.graphButton))
        self.graphButton.image = graphImg
        self.graphButton.grid(row=3, column=0, padx=7, pady=7)

        self.selectedButton = self.searchButton
        self.selectedButton['bg'] = 'red'
        self.menuFrame.place(x=25, y=50)

    def changeFrame(self, frame, button):
        if frame != self.selectedFrame:
            self.selectedButton['bg'] = 'white'
            self.selectedFrame.place_forget()
            frame.place(x=215, y=10)
            self.selectedFrame = frame
            self.selectedButton = button
            self.selectedButton['bg'] = 'red'
            self.selectedFrame.OnEnable()


MainGUI()
