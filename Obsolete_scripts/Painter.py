import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *

if __name__ == "__main__":

    app = QGuiApplication(sys.argv)
    
    if len(app.arguments()) < 2:
    
        sys.stderr.write("Usage: %s <image file> <overlay file>\n" % sys.argv[0])
        sys.exit(1)
    
    image = QImage(app.arguments()[1])
    if image.isNull():
        sys.stderr.write("Failed to read image: %s\n" % app.arguments()[1])
        sys.exit(1)
    
    overlay = QImage(app.arguments()[2])
    if overlay.isNull():
        sys.stderr.write("Failed to read image: %s\n" % app.arguments()[2])
        sys.exit(1)
    
    if overlay.size() > image.size():
    
        overlay = overlay.scaled(image.size(), Qt.KeepAspectRatio)
    
    painter = QPainter()
    painter.begin(image)
    painter.drawImage(0, 0, overlay)
    painter.end()
    
    label = QLabel()
    label.setPixmap(QPixmap.fromImage(image))
    label.show()
    
    sys.exit(app.exec_())