from tkinter import *
from tkinter.ttk import Combobox


class MainGUI:
    def __init__(self):
        self.window = Tk()
        self.window.title('Find Charger')
        self.window.geometry('800x600')

        self.menuFrame = Frame(self.window)

        self.searchButton = Button(self.menuFrame, text='검색', width=18, height=8, bg='white')
        self.searchButton.grid(row=1, column=0, padx=7, pady=20)

        self.favoritesButton = Button(self.menuFrame, text='즐찾', width=18, height=8, bg='white')
        self.favoritesButton.grid(row=2, column=0, padx=7, pady=20)

        self.graphButton = Button(self.menuFrame, text='그래프', width=18, height=8, bg='white')
        self.graphButton.grid(row=3, column=0, padx=7, pady=20)

        self.menuFrame.place(x=25, y=50)

        self.window.mainloop()


MainGUI()
