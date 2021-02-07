import sys
#import pyodbc
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

self.image = QLabel()
self.image.setPixmap(QPixmap("test_bg.jpg"))
self.image.setObjectName("image")
self.image.mousePressEvent = self.getPos

def getPos(self , event):
    x = event.pos().x()
    y = event.pos().y() 