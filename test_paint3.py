import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
#import points

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
        ellipse = QGraphicsEllipseItem()
        x = event.scenePos().x()
        y = event.scenePos().y()
        if self.opt == "Generate":
            self.addEllipse(x, y, 4, 4, pen, brush)
        elif self.opt == "Select":
            print(x, y)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(538, 269)
        self.graphicsView = QGraphicsView(Dialog)
        self.graphicsView.setGeometry(QRect(130, 10, 371, 221))
        self.graphicsView.setObjectName("graphicsView")
        self.radioButton = QRadioButton(Dialog)
        self.radioButton.setGeometry(QRect(20, 30, 82, 31))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QRadioButton(Dialog)
        self.radioButton_2.setGeometry(QRect(20, 80, 82, 17))
        self.radioButton_2.setObjectName("radioButton_2")

        self.retranslateUi(Dialog)
        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.radioButton.setText(_translate("Dialog", "Generate"))
        self.radioButton_2.setText(_translate("Dialog", "Select"))

class SimpleWindow(QMainWindow, Ui_Dialog):
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