import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test window")
        self.setGeometry(350,150,600,600)
        self.setupUI()

    def setupUI(self):
        # setup user interface
        self.img_label = QLabel()

        # Create main layout
        mainLayout = QGridLayout()

        # create a graphic scene
        self.graphscene = QGraphicsScene(self)
        self.graphview = QGraphicsView(self.graphscene)
        self.graphview.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.graphscene.setSceneRect(0,0,200,250)
        ellipse = QGraphicsEllipseItem(50,50,5,5)
        ellipse.setBrush(Qt.red)
        ellipse.setPen(Qt.red)
        # self.graphscene.addItem(ellipse)

        # add mouse press event
        self.graphview.mousePressEvent=self.addPoints

        # create some buttons
        self.butt1 = QRadioButton("Add")
        self.butt1.setChecked(True)
        self.butt2 = QRadioButton("Remove")

        mainLayout.addWidget(self.butt1,1,1)
        mainLayout.addWidget(self.butt2,2,1)

        mainLayout.addWidget(self.graphview,1,2,2,1)

        picture_path = 'img/part_view_0.png'
        self.pixmap=QPixmap(picture_path)
        self.pixmap_scaled=self.pixmap.scaledToHeight(220)

        self.imItem = self.graphscene.addPixmap(self.pixmap_scaled)

        self.setLayout(mainLayout)

        
        # Setup picture path
        # self.img_label.setGeometry(0,0,400,300)

        self.show()
    
    def addPoints(self,event):
        x = event.x()
        y = event.y()
        # will create or delete items according to radio butt
        if self.butt1.isChecked():
            # Adding new element
            ellipse = QGraphicsEllipseItem(0,0,5,5)
            ellipse.setPen(Qt.blue)
            ellipse.setBrush(Qt.blue)
            ellipse.setPos(x,y)
            self.graphscene.addItem(ellipse)
        elif self.butt2.isChecked():
            # Delete element if in the same area
            for item in self.graphscene.items():
                # check x location compare to actual x
                if abs(x-item.x())<10 and abs(y-item.y())<10:
                    self.graphscene.removeItem(item)

def main():
    App=QApplication(sys.argv)
    window=Window()
    sys.exit(App.exec_())

if __name__=='__main__':
    main()