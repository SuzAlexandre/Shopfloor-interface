import sys
from typing import Match
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import datetime

# Create some default setup
Ok_char = '✔'
Nok_char = "✘"
Ok_color = 'color: green'
Nok_color = 'color: red'
Default_font = 'Arial' #'Hind'

class Color(QWidget):
    def __init__(self, color, *args, **kwargs):
        super(Color, self).__init__(*args, **kwargs)
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Production interface")
        self.setGeometry(350,150,600,600)
        self.UI()

    def paintEvent(self, e):
        qp = QPainter(self)
        self.drawRectangles(qp)
        qp.setBrush(QColor(100, 000, 0))
        qp.drawRect(0,0,20,20)
        qp.drawLine(0,0,50,50)
        pen=QPen(Qt.red)
        pen.setWidth(10)
        qp.setPen(pen)
        qp.drawPoint(60,60)

    def drawRectangles(self, qp):    
        qp.setBrush(QColor(255, 0, 0, 100))
        qp.save() # save the QPainter config

        qp.drawRect(10, 15, 20, 20)

        qp.setBrush(QColor(0, 0, 255, 100))
        qp.drawRect(50, 15, 20, 20)

        qp.restore() # restore the QPainter config            
        qp.drawRect(100, 15, 20, 20)

    def UI(self):
        # Setting up main layout
        mainLayout=QVBoxLayout()
        self.tabs=QTabWidget()

        # Adding an horizontal layout that will include vertical layout
        tab1GridLayout=QGridLayout()
        
        # Adding barcode box and status
        self.DMC_text=QLabel("Barcode:")
        self.DMC_text.setAlignment(Qt.AlignRight)
        self.DMC_input=QLineEdit()

        self.Status_text=QLabel(Nok_char)
        self.Status_text.setFont(QFont(Default_font,100))
        self.Status_text.setAlignment(Qt.AlignCenter)
        self.Status_text.setStyleSheet(Nok_color)

        self.Info_text=QLabel("Information")
        self.Info_text.setAlignment(Qt.AlignCenter)
        self.Info_output=QLabel("Part status to be displayed here")
        self.Info_output.setWordWrap(True)
        self.Info_output.setStyleSheet("background-color: lightgrey;""border : 2px solid black;")
        self.Info_output.setAlignment(Qt.AlignTop)

        # Adding elements to quality layout
        tab1GridLayout.addWidget(self.DMC_text,1,0)
        tab1GridLayout.addWidget(self.DMC_input,1,1)
        tab1GridLayout.addWidget(self.Status_text,2,1)
        tab1GridLayout.addWidget(self.Info_text,0,2)
        tab1GridLayout.addWidget(self.Info_output,1,2,2,1)

        # setup grid layout size
        tab1GridLayout.setRowStretch(2,1)
        tab1GridLayout.setColumnStretch(0,1)
        tab1GridLayout.setColumnStretch(1,2)
        tab1GridLayout.setColumnStretch(2,3)
        
         # Adding barcode box and status
        self.scrap_tab_DMC_text=QLabel("Barcode:")
        self.scrap_tab_DMC_text.setAlignment(Qt.AlignRight)
        self.scrap_tab_DMC_input=QLineEdit()

        self.setLayout(tab1GridLayout)

        mainLayout.addWidget(self.tabs)
        self.setLayout(mainLayout)

        self.painter=QPainter(self)
        self.pen=QPen(Qt.red)
        self.pen.setWidth(50)
        self.painter.setPen(self.pen)
        self.painter.drawPoint(60,60)

        self.show()
    
    def scrapTabLayout(self):
        # Function to define the scrap tab layout
        print('From scrapTabLayout function')

    def btnFunc(self):
        self.text.setText("Button is active")
        sys.exit()

    def getPos(self,event):
        x = event.pos().x()
        y = event.pos().y() 
        print('Button pressed at x: ' + str(x) + ' y:' + str(y))

        # test add a red dot
        painter = QPainter(self)
        point = QPoint(x,y)
        painter.setPen(QColor(255,0,0,200))
        painter.drawPixmap(point,self.pixmap)
        # painter.drawPoint(x,y)
        
    def updateScrapPic(self,view):
        # setting up the picture path
        picture_path= 'img/part_view_' + str(view) + '.png'

        self.pixmap=QPixmap(picture_path)
        self.pixmap_scaled=self.pixmap.scaledToHeight(300)
        self.img_label.setPixmap(self.pixmap_scaled)
        self.img_label.setGeometry(0,0,100,300)

def main():
    App=QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec_())

if __name__=='__main__':
    main()