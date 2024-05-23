from tkinter import *
from tkinter.ttk import Combobox


class MainGUI:
    def __init__(self):
        self.window = Tk()
        self.window.title('Find Charger')
        self.window.geometry('1000x600')

        self.menuFrame = Frame(self.window)

        self.searchButton = Button(self.menuFrame, text='검색', width=18, height=8, bg='white')
        self.searchButton.grid(row=1, column=0, padx=7, pady=20)

        self.favoritesButton = Button(self.menuFrame, text='즐찾', width=18, height=8, bg='white')
        self.favoritesButton.grid(row=2, column=0, padx=7, pady=20)

        self.graphButton = Button(self.menuFrame, text='그래프', width=18, height=8, bg='white')
        self.graphButton.grid(row=3, column=0, padx=7, pady=20)

        self.menuFrame.place(x=25, y=50)

        self.chargeFrame = Frame(self.window, width=400, height=600)
        self.cityList = Combobox(self.chargeFrame)
        self.cityList.set('시/군')
        testCity = ['1', '2', '3']
        self.chargeLabels = [Label(self.chargeFrame, width=30, height=7, bg='white' if i & 1 else 'black') for i in
                             range(4)]
        for i in range(4):
            self.chargeLabels[i].place(x=0, y=50 + (i * 16 * 7))

        self.cityList['values'] = testCity
        self.cityList.place(x=0, y=10)

        self.prevButton = Button(self.chargeFrame, width=14, height=3)
        self.nextButton = Button(self.chargeFrame, width=14, height=3)

        self.prevButton.place(x=0, y=50 + (4 * 16 * 7))
        self.nextButton.place(x=7.7 * 14, y=50 + (4 * 16 * 7))

        self.chargeFrame.place(x=225, y=10)

        self.infoFrame = Frame(self.window, width=600, height=600)
        self.infoCanvas = Canvas(self.infoFrame, width=475, height=475, bg='white')
        self.infoCanvas.place(x=0, y=25)

        self.mailButton = Button(self.infoFrame, width=12, height=5, bg='black')
        self.mailButton.place(x=300, y=50 + (4 * 16 * 7))

        self.mapButton = Button(self.infoFrame, width=12, height=5, bg='black')
        self.mapButton.place(x=100, y=50 + (4 * 16 * 7))

        self.infoFrame.place(x=475, y=0)

        self.window.mainloop()


MainGUI()
