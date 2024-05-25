from tkinter import *
from tkinter.ttk import Combobox

import requests


class MainGUI:
    def __init__(self):
        self.window = Tk()
        self.window.title('Find Charger')
        self.window.geometry('1000x600')

        self.cities = {'가평군': [42], '고양시': [85, 86, 87], '과천시': [21], '광명시': [16],
                       '광주시': [39], '구리시': [22], '군포시': [24], '김포시': [47], '남양주시': [27], '동두천시': [18],
                       '부천시': [64, 62, 63, 61], '성남시': [70, 68, 69],
                       '수원시': [75, 77, 74, 76], '시흥시': [26],
                       '안산시': [49, 19], '안성시': [46], '안양시': [81, 80],
                       '양주시': [31], '양평군': [43], '여주시': [33], '연천군': [40], '오산시': [23], '용인시': [90, 91, 45],
                       '의왕시': [25], '의정부시': [13], '이천시': [44], '파주시': [37], '평택시': [17], '포천시': [41], '하남시': [28],
                       '화성시': [35]}

        self.initMenu()
        self.initSearch()

        self.window.mainloop()

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
        self.cityCombobox.place(x=0, y=10)

        self.chargeLabels = [Label(self.searchFrame, width=34, height=7, bg='white' if i & 1 else 'blue') for i in
                             range(4)]
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
