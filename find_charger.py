from tkinter import *
import requests

import Data
from GraphFrame import GraphFrame
from SearchFrame import SearchFrame


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
        self.searchFrame.place(x=215, y=10)
        self.selected = self.searchFrame
        self.window.mainloop()

    def initMenu(self):
        self.menuFrame = Frame(self.window)
        searchImg = PhotoImage(file='검색창.png')
        self.searchButton = Button(self.menuFrame, text='검색', bg='white', image=searchImg,
                                   command=lambda: self.changeFrame(self.searchFrame))
        self.searchButton.image = searchImg
        self.searchButton.grid(row=1, column=0, padx=7, pady=7)

        favoriteImg = PhotoImage(file='즐겨찾기창.png')
        self.favoritesButton = Button(self.menuFrame, text='즐찾', bg='white', image=favoriteImg)
        self.favoritesButton.image = favoriteImg
        self.favoritesButton.grid(row=2, column=0, padx=7, pady=7)

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


MainGUI()
