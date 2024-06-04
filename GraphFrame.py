import re
from collections import defaultdict
from tkinter import *
from tkinter.ttk import Combobox

from tkintermapview import TkinterMapView

import Data
import kakaomap


class GraphFrame(Frame):
    def __init__(self, master, **args):
        super().__init__(**args)
        self.isGraph = True
        self.page = 0
        self.initWidget()
        self.cityChargeCnt = dict()

    def initWidget(self):
        self.cityCombobox = Combobox(self)
        self.cityCombobox.set('시/군')
        self.cityCombobox['values'] = list(Data.cities.keys())
        self.cityCombobox.bind("<<ComboboxSelected>>", self.OnComboboxSelect)
        self.cityCombobox.place(x=0, y=10)

        self.infoCanvas = Canvas(self, width=800, height=450, bg='white')
        self.infoCanvas.place(x=0, y=50)
        self.mapView = TkinterMapView(self, width=800, height=450, corner_radius=0)

        self.mapImg = PhotoImage(file='지도.png')
        self.smallGraphImg = PhotoImage(file='그래프.png')
        self.mapButton = Button(self, bg='white', image=self.mapImg, command=self.change)
        self.mapButton.place(x=340, y=515)

    def OnComboboxSelect(self, event):
        if self.isGraph:
            self.showGraph()
        else:
            self.showChargeMap()

    def showGraph(self):
        city = self.cityCombobox.get()
        self.infoCanvas.delete('all')

        if city not in self.cityChargeCnt:
            pattern = r'\b\w+(동|읍|면)\b'
            self.cityChargeCnt[city] = defaultdict(int)
            for info in Data.chargeInfos[city]:
                town = re.search(pattern, info['stnAddr'])
                if town:
                    town = town.group()
                    self.cityChargeCnt[city][town] += info['rapidCnt'] + info['slowCnt']
        h = int(self.infoCanvas['height'])
        hOffset = h - 50
        height = (h - 100) // max(self.cityChargeCnt[city].values())

        w = int(self.infoCanvas['width'])
        wOffset = 25
        width = (w - wOffset * 2) // len(self.cityChargeCnt[city])

        for i, (town, cnt) in enumerate(self.cityChargeCnt[city].items()):
            self.infoCanvas.create_rectangle(wOffset + (i * width), hOffset,
                                             wOffset + ((i + 1) * width), hOffset - height * cnt,
                                             fill='red')
            self.infoCanvas.create_text(wOffset + (i * width) + width // 4, hOffset + 20, text=town,
                                        anchor="w", font=('consolas', 10, 'bold'), width=width // 2)
            self.infoCanvas.create_text(wOffset + (i * width) + width // 2, hOffset - height * cnt - 20,
                                        text=str(cnt), font=('consolas', 12, 'bold'))

        self.infoCanvas.create_text(10, 20, text=city, anchor="w", font=('consolas', 12, 'bold'))

    def showChargeMap(self):
        city = self.cityCombobox.get()
        self.infoCanvas.delete('all')

        center = kakaomap.geocode(city)
        self.mapView.set_position(*center)
        for city in Data.chargeInfos[city]:
            addr = city['stnAddr']
            if addr:
                self.mapView.set_marker(*kakaomap.geocode(addr))

    def change(self):
        self.isGraph = not self.isGraph
        if self.isGraph:
            self.mapButton['image'] = self.mapImg
            self.infoCanvas.place(x=0, y=50)
            self.mapView.place_forget()
            self.showGraph()
        else:
            self.mapButton['image'] = self.smallGraphImg
            self.infoCanvas.place_forget()
            self.mapView.place(x=0, y=50)
            self.showChargeMap()
