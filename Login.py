import json
import os
from FTP import *
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.Qt import *
from ftplib import FTP

class Ui_MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.ftp = FTP()
        self.inform={}

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(450, 250)
        MainWindow.setWindowIcon(QIcon('static/logo.jpg'))
        # MainWindow.setStyleSheet("background-image:url(static/1.jpg)")
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralWidget)
        self.lineEdit.setGeometry(QtCore.QRect(175, 25, 180, 20))
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralWidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(175, 65, 180, 20))
        self.lineEdit_2.setText("")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralWidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(175, 105, 180, 20))
        self.lineEdit_3.setText("")
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.centralWidget)
        self.lineEdit_4.setGeometry(QtCore.QRect(175, 145, 180, 20))
        self.lineEdit_4.setText("")
        self.lineEdit_4.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_4.setObjectName("lineEdit_4")

        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(95, 28, 80, 15))
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralWidget)
        self.label_2.setGeometry(QtCore.QRect(95, 68, 80, 15))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralWidget)
        self.label_3.setGeometry(QtCore.QRect(95, 108, 80, 15))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralWidget)
        self.label_4.setGeometry(QtCore.QRect(95, 148, 80, 15))
        self.label_4.setObjectName("label_4")
        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setGeometry(QtCore.QRect(140, 185, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_2.setGeometry(QtCore.QRect(240, 185, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralWidget)

        self.pushButton.clicked.connect(self.login)
        self.pushButton_2.clicked.connect(MainWindow.close)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "FTP同步云盘"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "请输入FTP地址"))
        self.lineEdit_2.setPlaceholderText(_translate("MainWindow", "请输入端口号"))
        self.lineEdit_3.setPlaceholderText(_translate("MainWindow", "请输入用户名"))
        self.lineEdit_4.setPlaceholderText(_translate("MainWindow", "请输入密码"))
        self.label.setText(_translate("MainWindow", "IP地址"))
        self.label_2.setText(_translate("MainWindow", "端口号"))
        self.label_3.setText(_translate("MainWindow", "用户名"))
        self.label_4.setText(_translate("MainWindow", "密码"))
        self.pushButton.setText(_translate("MainWindow", "确定"))
        self.pushButton_2.setText(_translate("MainWindow", "取消"))

        self.lineEdit.setText("49.232.138.204")
        self.lineEdit_2.setText("21")
        self.lineEdit_3.setText("renjijiaohu-ftp")
        self.lineEdit_4.setText("eCAGMB3SDaGKxG6R")

    # 此函数实现ftp登录
    def login(self):
        login_ip = self.lineEdit.text()
        login_port = int(self.lineEdit_2.text())
        login_user = self.lineEdit_3.text()
        login_password = self.lineEdit_4.text()

        try:
            self.ftp.connect(host=login_ip, port=login_port, timeout=10)
        except:
            QMessageBox.warning(self, '警告', 'FTP地址错误，网络连接超时!', QMessageBox.Yes)
        try:
            self.ftp.login(user=login_user, passwd=login_password)
        except:
            QMessageBox.warning(self, "警告", "用户名或密码错误！", QMessageBox.Yes)
        self.inform = [login_ip, login_port, login_user, login_password]
        with open('login_inform.json', 'w') as f:
            json.dump(json.dumps(self.inform), f)
        ui_ftp.show()
        MainWindow.close()

    # 此函数实现退出ftp会话
    def ftp_logout(self):
        print('即将断开连接')
        self.ftp.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QMainWindow()
    proPath = os.path.split(os.path.realpath(__file__))[0]
    ui = Ui_MainWindow()
    ui_ftp = FTPWindow(proPath)
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())