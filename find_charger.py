from tkinter import *
from tkinter.ttk import Combobox


class MainGUI:
    def __init__(self):
        self.window = Tk()
        self.window.title('Find Charger')
        self.window.geometry('1000x600')

        self.menuFrame = Frame(self.window)
        searchImg = PhotoImage(file='검색창.png')
        self.searchButton = Button(self.menuFrame, text='검색', bg='white', image=searchImg)
        self.searchButton.grid(row=1, column=0, padx=7, pady=7)

        favoriteImg = PhotoImage(file='즐겨찾기창.png')
        self.favoritesButton = Button(self.menuFrame, text='즐찾', bg='white', image=favoriteImg)
        self.favoritesButton.grid(row=2, column=0, padx=7, pady=7)

        graphImg = PhotoImage(file='그래프창.png')
        self.graphButton = Button(self.menuFrame, text='그래프', bg='white', image=graphImg)
        self.graphButton.grid(row=3, column=0, padx=7, pady=7)

        self.menuFrame.place(x=25, y=50)

        self.searchFrame = Frame(self.window, width=1000, height=600)
        self.cityList = Combobox(self.searchFrame)
        self.cityList.set('시/군')
        testCity = ['1', '2', '3']
        self.chargeLabels = [Label(self.searchFrame, width=34, height=7, bg='white' if i & 1 else 'blue') for i in
                             range(4)]
        for i in range(4):
            self.chargeLabels[i].place(x=0, y=50 + (i * 16 * 7))

        self.cityList['values'] = testCity
        self.cityList.place(x=0, y=10)

        prevImg = PhotoImage(file='왼쪽이동.png')
        nextImg = PhotoImage(file='오른쪽이동.png')
        self.prevButton = Button(self.searchFrame, bg='white', image=prevImg)
        self.nextButton = Button(self.searchFrame, bg='white', image=nextImg)

        self.prevButton.place(x=50, y=50 + (4 * 16 * 7))
        self.nextButton.place(x=124, y=50 + (4 * 16 * 7))

        self.infoCanvas = Canvas(self.searchFrame, width=475, height=475, bg='white')
        self.infoCanvas.place(x=275, y=10)

        mailImg = PhotoImage(file='이메일.png')
        self.mailButton = Button(self.searchFrame, bg='white', image=mailImg)
        self.mailButton.place(x=475, y=500)

        mapImg = PhotoImage(file='지도.png')
        self.mapButton = Button(self.searchFrame, bg='white', image=mapImg)
        self.mapButton.place(x=325, y=500)

        telegramImg = PhotoImage(file='텔레그램.png')
        self.telegramButton = Button(self.searchFrame, bg='white', image=telegramImg)
        self.telegramButton.place(x=625, y=500)

        self.searchFrame.place(x=215, y=10)

        self.window.mainloop()


MainGUI()
