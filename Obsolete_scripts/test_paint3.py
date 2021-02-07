import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import points


class GraphicsScene(QGraphicsScene):
    def __init__(self, parent=None):
        QGraphicsScene.__init__(self, parent)
        self.setSceneRect(-100, -100, 200, 200)
        self.opt = ""

    def setOption(self, opt):
        self.opt = opt

    def mousePressEvent(self, event):
        pen = QPen(Qt.black)
        brush = QBrush(Qt.black)
        x = event.scenePos().x()
        y = event.scenePos().y()
        if self.opt == "Generate":
            ellipse = QGraphicsEllipseItem(0,0,4,4)
            ellipse.setPen(Qt.red)
            ellipse.setBrush(Qt.red)
            ellipse.setX(x)
            ellipse.setY(y)
            self.addItem(ellipse)
        elif self.opt == "Select":
            for item in self.items():
                # check x location compare to actual x
                if abs(x-item.x())<10 and abs(y-item.y())<10:
                    self.removeItem(item)
                    # item.hide()


class SimpleWindow(QMainWindow, points.Ui_Dialog):
    def __init__(self, parent=None):
        super(SimpleWindow, self).__init__(parent)
        self.setupUi(self)

        self.scene = GraphicsScene(self)
        self.graphicsView.setScene(self.scene)
        self.graphicsView.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        group = QButtonGroup(self)
        group.addButton(self.radioButton)
        group.addButton(self.radioButton_2)

        group.buttonClicked.connect(lambda btn: self.scene.setOption(btn.text()))
        self.radioButton.setChecked(True)
        self.scene.setOption(self.radioButton.text())



app = QApplication(sys.argv)
form = SimpleWindow()
form.show()
app.exec_()