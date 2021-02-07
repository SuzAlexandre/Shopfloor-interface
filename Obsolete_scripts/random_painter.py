import sys, random
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore

class Example(QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):      
        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('Points')
        self.mousePressEvent = self.paintPoint
        self.show()

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawPoints(qp)
        qp.end()
        
    def drawPoints(self, qp):
      
        pen = QtGui.QPen(QtCore.Qt.red)
        pen.setWidth(3)
        qp.setPen(pen)
        size = self.size()
        
        x=10
        y=10
        self.redpoint=QtCore.QPoint(x,y)
        qp.drawPoint(self.redpoint)    
        

    def paintPoint(self,event):
        x = event.pos().x()
        y = event.pos().y() 
        print('Button pressed at x: ' + str(x) + ' y:' + str(y))
        self.redpoint.setX(x)
        self.redpoint.setY(y)
        self.update()


def main():
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()