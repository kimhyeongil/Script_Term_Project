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
        self.index = None
        self.initWidget()
        self.cityChargeCnt = dict()

    def initWidget(self):
        self.cityCombobox = Combobox(self)
        self.cityCombobox.set('시/군')
        self.cityCombobox['values'] = list(Data.cities.keys())
        self.cityCombobox.bind("<<ComboboxSelected>>", self.OnComboboxSelect)
        self.cityCombobox.place(x=0, y=10)

        self.infoCanvas = Canvas(self, width=800, height=500, bg='white')
        self.infoCanvas.place(x=0, y=50)
        self.mapView = TkinterMapView(self, width=500, height=500, corner_radius=0)

    def OnComboboxSelect(self, event):
        self.showGraph()

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
        wOffset = 10
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
            self.mapView.set_marker(*kakaomap.geocode(addr))
