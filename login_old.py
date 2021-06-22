# -*- coding: utf-8 -*-
"""
# @Time    : 2021/6/21 16:38
# @Software: PyCharm
# @File    : login_old.py
"""
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from ftplib import FTP
from Login import Ui_MainWindow

class FTP_login():
    def __init__(self):
        self.ftp = FTP()

    # 些函数实现ftp登录
    def ftp_login(self,host_ip,username,password):
        try:
            self.ftp.connect(host_ip, port=21, timeout=10)
        except :
            print('网络连接超时')
            return 1
        try:
            self.ftp.login(user=username, passwd=password)
        except:
            print('用户名或密码错误')
            return 2
        return 0

    # 此函数实现退出ftp会话
    def ftp_logout(self):
        print('即将断开连接')
        self.ftp.close()

if __name__ == '__main__':
    # 要连接的主机ip
    host_ip = '49.232.138.204'
    # 用户名
    username = 'renjijiaohu-ftp'
    # 密码
    password = 'eCAGMB3SDaGKxG6R'
    # 实例化
    ftp = FTP_login()
    # 如果登录成功则执行命令，然后退出
    if ftp.ftp_login(host_ip, username, password) == 0:
        print('登录成功，可以执行命令')
        ftp.ftp_logout()

PASSWORD_MODE = 2
NORMAL_MODE = 0

POSSIBLE_CLIENT_OPERATIONS = ['', 'List', 'Upload', 'Download', 'Move', 'Create', 'Delete']
POSSIBLE_OPERATIONS_ACTION = {'': 0, 'List': 1, 'Upload': 2, 'Download': 3, 'Move': 4, 'Delete': 5}

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.show()
        self._server_message = ''
        self._ftp_client = FTP_login()
        self._userAction = ''
        self._download_path = ''
        self._uploadFile = ''
        self._loggedIn = False
        self.cb_show_password.setChecked(False)
        self.pb_upload.setValue(0)
        self.pb_download.setValue(0)

        f = self.lb_ftp_server_address.font()
        f.setPointSize(8)
        self.lb_password.setFont(f)
        self.lb_username.setFont(f)
        self.lb_ftp_server_address.setFont(f)
        self.lb_server_response.setFont(f)
        # self.lb_action.setFont(f)
        self.lb_movepath.setFont(f)
        self.lb_upload_path.setFont(f)
        self.lb_filename.setFont(f)
        self.lb_create_file.setFont(f)
        self.lb_delete_directory.setFont(f)

        login_ip=self.lineEdit.text()
        login_user = self.lineEdit2.text()
        login_password = self.lineEdit_3.text()

        # self.btn_connect.pressed.connect(self.btn_connect_handler)
        # # self.btn_disconnect.pressed.connect(self.btn_disconnect_handler)
        # self.btn_list.pressed.connect(self.btn_list_handler)
        # self.cb_show_password.stateChanged.connect(self.cb_show_password_handler)
        # # self.comboBox_userAction.currentIndexChanged[str].connect(self.comboBox_userAction_handler)
        # # self.btn_proceed.pressed.connect(self.btn_proceed_handler)
        # self.btn_loadfile.pressed.connect(self.btn_loadfile_handler)
        # self.btn_upload.pressed.connect(self.btn_upload_handler)
        # self.btn_move.pressed.connect(self.btn_move_handler)
        # # self.btn_upload.clicked.connect(self.uploadProgress)
        # self.btn_download.pressed.connect(self.btn_download_handler)
        # self.btn_saveto.pressed.connect(self.btn_saveto_handler)
        # self.btn_create.pressed.connect(self.btn_create_handler)
        # self.btn_delete.pressed.connect(self.btn_delete_handler)

    # def btn_loadfile_handler(self):
    #     self.pb_upload.setValue(0)
    #     self._uploadFile, _ = QFileDialog.getOpenFileName(self, 'Open File', '', '', 'All files(*.*)')
    #
    # # Triggered when the upload button is pressed it then calls the client back end functions to upload the selected file
    # # to the server. This function verifies the user is connected to the server and controls the
    # # progress bar update rate. If user is not logged in it displays Not logged in message.
    # # Displays the server response message in the QTextBrowser widget
    # def btn_upload_handler(self):
    #     if self._loggedIn:
    #         path = self.le_upload_path.text()
    #         self._ftp_client.stor(str(path), self._uploadFile)
    #         self._server_message += self._ftp_client.getServerMessage()
    #         self.td_server_response.insertPlainText(self._server_message)
    #         # self._scrollBar.setValue(self._scrollBar.maxValue())
    #
    #         progress = 0
    #         while progress <= 100:
    #             progress += 0.001
    #             self.pb_upload.setValue(progress)
    #
    #     else:
    #         print("Cannot Upload \n PLEASE LOGIN TO A SERVER")
    #
    #     self.td_server_response.moveCursor(QTextCursor.End)
    #
    # # Triggered when the download button is pressed it calls the client back end function to download a file specified
    # # by the user in the File Name textbox. It verifies the user is connected to the server and controls the download
    # # progress bar update rate. If user is not logged in it displays a message.
    # # Displays the server response message in the QTextBrowser widget
    # def btn_download_handler(self):
    #     if self._loggedIn:
    #         file_to_download = self.le_download_path.text()
    #         self._ftp_client.retr(file_to_download, self._download_path)
    #         self._server_message += self._ftp_client.getServerMessage()
    #
    #         progress = 0
    #         while progress <= 100:
    #             progress += 0.001
    #             self.pb_download.setValue(progress)
    #
    #     else:
    #         self._server_message += 'Cannot Download \n PLEASE LOGIN TO A SERVER'
    #         self.td_server_response.setText(self._server_message)
    #
    #     self._server_message += '\n'
    #     self.td_server_response.setText(self._server_message)
    #     self.td_server_response.moveCursor(QTextCursor.End)
    #
    # # Triggered when the save to button is pressed. It opens a file selector window and stores the selected path.
    # # The path includes the user specified name. This path is used by the btn_download_handler() function to save the
    # # downloaded file
    # def btn_saveto_handler(self):
    #     self.pb_upload.setValue(0)
    #     self._download_path, _ = QFileDialog.getSaveFileName(self, 'Save File', '', '', 'All files(*.*)')
    #
    # # Triggered when the connect button is pressed. This handler is responsible for calling the client back end function
    # # to login to the FTP_login server. It is also responsible for closing the FTP_login session as it becomes the disconnect button
    # # as soon as the user is logged in. Displays the server response message in the QTextBrowser widget
    # def btn_connect_handler(self):
    #     if not self._loggedIn:
    #         ftp_server_address = self.le_ftp_server_address.text()
    #         username = self.le_username.text()
    #         password = self.le_password.text()
    #         if len(ftp_server_address) > 3:
    #             self._loggedIn = self._ftp_client.login(ftp_server_address, username, password)
    #             self._server_message = self._ftp_client.getServerMessage()
    #             self.td_server_response.setText(self._server_message)
    #             # print(self._server_message)
    #         else:
    #             pass
    #         # lock all the inputs for user name and servers.
    #         self.le_username.setReadOnly(True)
    #         self.le_password.setReadOnly(True)
    #         self.le_ftp_server_address.setReadOnly(True)
    #         self.btn_connect.setText('Disconnect')
    #     else:
    #         self._loggedIn = False
    #         self._ftp_client.quit()
    #         self._server_message += '\n'
    #         self._server_message += self._ftp_client.getServerMessage()
    #         self.td_server_response.setText(self._server_message)
    #         self.le_username.setReadOnly(False)
    #         self.le_password.setReadOnly(False)
    #         self.le_ftp_server_address.setReadOnly(False)
    #         self.btn_connect.setText('Connect')
    #
    #     self._server_message += '\n'
    #     self.td_server_response.setText(self._server_message)
    #     self.td_server_response.moveCursor(QTextCursor.End)
    #
    # # Triggered when the List Directories button is pressed. It calls the client back end functions to send a LIST
    # # command to the FTP_login server. The function verifies if the user is logged in.
    # # Displays the server response message in the QTextBrowser widget
    # def btn_list_handler(self):
    #     if self._loggedIn:
    #         self._ftp_client.list()
    #         if len(self._server_message) > 1:
    #             self._server_message += '\n'
    #         self._server_message += self._ftp_client.getServerMessage()
    #         self._server_message += '\n'
    #         self.td_server_response.setText(self._server_message)
    #     else:
    #         self.td_server_response.setText('PLEASE LOGIN TO A SERVER')
    #
    #     self.td_server_response.moveCursor(QTextCursor.End)
    #
    # # Triggered when the show password checkbox is ticked. It toggles the password visibility on and off at the convenience of the user
    # def cb_show_password_handler(self, s):
    #     if s == Qt.Checked:
    #         self.le_password.setEchoMode(NORMAL_MODE)
    #     else:
    #         self.le_password.setEchoMode(PASSWORD_MODE)
    #
    # # Triggered when the Move button is pressed. The function moves the user to the working directory defined by
    # # the path in the textbox. If the user leaves the path textbox empty it is assumed the user wants to move to the
    # # root directory. Displays the server response message in the QTextBrowser widget
    # def btn_move_handler(self):
    #     if self._loggedIn:
    #         path = self.le_move.text()
    #         if path == '':
    #             self._ftp_client.cdup()
    #         else:
    #             self._ftp_client.cwd(path)
    #
    #         self._server_message += self._ftp_client.getServerMessage()
    #         self.td_server_response.setText(self._server_message)
    #     else:
    #         print("Cannot Change Directories \n PLEASE LOGIN TO A SERVER")
    #
    #     self.td_server_response.moveCursor(QTextCursor.End)
    #
    # # Triggered when the Create button is pressed. The function creates a directory in the FTP_login server.
    # # The directory is created in the current working directory.
    # # The directory name is defined by the user in the available textbox.
    # # Displays the server response message in the QTextBrowser widget
    # def btn_create_handler(self):
    #     if self._loggedIn:
    #         filename = self.le_create_file.text()
    #         self._ftp_client.mkd(filename)
    #         self._server_message += self._ftp_client.getServerMessage()
    #     else:
    #         self._server_message += 'Cannot create a directory \n PLEASE LOGIN TO A SERVER\n'
    #         self.td_server_response.setText(self._server_message)
    #
    #     self._server_message += '\n'
    #     self.td_server_response.setText(self._server_message)
    #     self.td_server_response.moveCursor(QTextCursor.End)
    #
    # # Triggered when the Delete button is pressed. The function deletes a file in the server.
    # # The file is defined by the available textbox. It can delete files and folders
    # # Displays the server response message in the QTextBrowser widget
    # def btn_delete_handler(self):
    #     if self._loggedIn:
    #         filename = self.le_delete_file.text()
    #         x = filename.find('.')
    #         if x > 0:
    #             self._ftp_client.dele(str(filename))
    #         else:
    #             self._ftp_client.rmd(str(filename))
    #
    #
    #     self._server_message += self._ftp_client.getServerMessage()
    #     self._server_message += '\n'
    #     self.td_server_response.setText(self._server_message)
    #     self.td_server_response.moveCursor(QTextCursor.End)

if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui_hello = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
