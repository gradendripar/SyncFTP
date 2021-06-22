import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
class MainWindow(QMainWindow):
    def __init__(self,parent=None):
        super(MainWindow,self).__init__(parent)
        bar=self.menuBar()
        file=bar.addMenu('File')
        open=file.addMenu('Save')
        open.addAction('open as')
        file.addAction('close')
        self.setWindowTitle('QMainWindow')
class wi(QWidget):
    def __init__(self,parent=None):
        super(wi,self).__init__(parent)
        vb=QVBoxLayout()
        lb=QLabel(self)
        self.pb = QPushButton('P1')
        self.pb.clicked.connect(self.click)
        vb.addWidget(self.pb)
        self.setLayout(vb)
    def click(self):
        print('Click me')
if __name__ == '__main__':
    app = QApplication(sys.argv)
    m= MainWindow()
    m.setCentralWidget(wi())
    m.show()
    sys.exit(app.exec_())

