import json

from FTP_UI import Ui_Form
from PyQt5.QtWidgets import QWidget, QDirModel, QTreeWidgetItem
from PyQt5.QtGui import QIcon, QTextCursor
import logging
from ftplib import FTP

class FTPWindow(QWidget, Ui_Form):
    def __init__(self, proPath,parent=None):
        super(FTPWindow, self).__init__(parent)
        self.proPath=proPath
        self.ftp = FTP()
        self.login_inform=[]
        self.setupUi(self)
        self.setWindowTitle('FTP同步云盘')
        # 设置窗口的图标，引用当前目录下的web.png图片
        self.setWindowIcon(QIcon(self.proPath + '/static/login.jpg'))
        self.setSignal()
        self.downing=True
        #************** 初始化按键
        self.Bt_down.setEnabled(False)
        self.Bt_up.setEnabled(False)
        # self.private = paramiko.RSAKey.from_private_key_file('E:/文档汇总/服务器SSH密钥/Tencent_4（私钥）/Tooziya.pem')
        # # 创建SSH对象
        # self.ssh = paramiko.SSHClient()
        # # 允许连接不在know_hosts文件中的主机，否则可能报错：paramiko.ssh_exception.SSHException: Server '192.168.43.140' not found in known_hosts
        # self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ftp_root="/home/tooziya/ftp"

        # ************** 初始化变量
        """FTP窗口"""
        self.ftp.encoding = "UTF-8"
        self.select_file = ""  # listView中选择的文件名
        self.file_list = []  # 存放查询FTP返回的当前目录所有文件列表
        self.ftp_tip = []  # 存储当前登陆信息

        # FTP登录
        with open('login_inform.json', 'r') as f:
            self.login_inform=json.loads(json.load(f))
        host = self.login_inform[0]  # 获取IP地址框内容
        port = self.login_inform[1]  # 获取端口号，注意要转换为int
        user = self.login_inform[2]  # 获取用户名
        passwd = self.login_inform[3]  # 获取密码
        self.ftp_tip=self.login_inform

        self.ftp.connect(host, port, timeout=10)  # 连接FTP
        self.ftp.login(user, passwd)  # 登录FTP
        self.Text_log.append("FTP服务器登录成功")
        self.ftp_connect()

        """本地窗口"""
        # self.sysfile = QFileSystemModel() # 获取本地文件系统
        # self.sysfile.setRootPath('')
        # self.treeView_local.setModel(self.sysfile)
        self.model = QDirModel()
        # self.model.setFilter(QtCore.QDir.NoDotAndDotDot | QtCore.QDir.AllDirs)
        self.treeView_local.header().hide()  # 隐藏表头
        self.treeView_local.setModel(self.model)
        for col in range(1, 4):
            self.treeView_local.setColumnHidden(col, True)

        self.save_path=""
        # self.treeView_local.setRootIndex(self.model.index(self.save_path))
        self.save_name=""

    # 信号绑定设置
    def setSignal(self):
        self.Bt_link.clicked.connect(self.ftp_connect)
        # self.Bt_down.clicked.connect(self.Bt_down_run)
        self.Bt_up.clicked.connect(self.ftp_connect)
        # 任意输入框改变就可以重新使能连接按键
        self.lineEdit_ip.editingFinished.connect(self.BtEnabled)
        self.lineEdit_port.editingFinished.connect(self.BtEnabled)
        self.lineEdit_user.editingFinished.connect(self.BtEnabled)
        self.lineEdit_pwd.editingFinished.connect(self.BtEnabled)
        self.treeWidget_master.itemClicked.connect(self.select_item_ftp)
        # self.treeView_local.doubleClicked.connect(self.select_item_local)
        self.treeView_local.expanded.connect(self.select_item_local)
        self.treeView_local.clicked.connect(self.select_item_local)
        # self.treeWidget_master.doubleClicked.connect(self.cd_button)

    # 按键使能
    def BtEnabled(self):
        self.Bt_link.setEnabled(True)
        self.Bt_down.setEnabled(False)
        self.Bt_up.setEnabled(False)

    # ftp 连接登录
    def ftp_connect(self):
        self.treeWidget_master.clear()

        self.file_list = self.ftp.nlst()  # 查询当前目录的所有文件列表
        self.Bt_link.setEnabled(False)


        self.root = QTreeWidgetItem(self.treeWidget_master)
        self.root.setText(0, '/')
        self.root.setIcon(0,QIcon(self.setItem_Icon('/')))
        self.root.setToolTip(0,'/')
        self.dirItem(self.root)
        self.cursor = self.Text_log.textCursor()
        self.Text_log.moveCursor(self.cursor.End)
        # # 连接服务器
        # result=self.ssh.connect(hostname=b'49.232.138.204', port=22, username=b'root', pkey=self.private)
        # self.Text_log.append(result)
        # print("link success!")
        self.treeWidget_master.itemExpanded.connect(self.dirItem_new)
        # for col in range(len(self.file_list)):
        #     print(col)
        #     self.treeWidget_master.setColumnHidden(col, True)
        # print(self.ftp.dir('/DetectMask.zip'))

    # 判断数据类型，设置图标
    def setItem_Icon(self,obj):
        if "." in obj:  # 是文件则不能进入
            icon = self.proPath+"/Icon/file.png"
        else:  # 是文件夹则可以进入
            icon = self.proPath+"/Icon/folder.png"

        if ".jpg" in obj or ".jpeg" in obj or ".png" in obj:  # 是文件则不能进入
            icon = self.proPath+"/Icon/file_img.png"
        elif ".zip" in obj or ".rar" in obj or ".7z" in obj:
            icon = self.proPath+"/Icon/file_zip.png"

        elif ".xls" in obj or ".xlsx" in obj:
            icon = self.proPath+"/Icon/file_excel.png"
        elif ".ppt" in obj or "pptx" in obj:
            icon = self.proPath+"/Icon/file_ppt.png"
        elif ".doc" in obj or ".docx" in obj or ".7z" in obj:
            icon = self.proPath+"/Icon/file_word.png"
        elif ".pdf" in obj:
            icon = self.proPath+"/Icon/file_pdf.png"
        elif ".py" in obj:
            icon = self.proPath + "/Icon/file_python.png"
        return icon


    # 递归操作，遍历ftp服务器所有文件
    def dirItem(self,item):
        # print(item.toolTip((0)))
        list=self.ftp.nlst(str(item.toolTip(0)))
        # for name1 in list:
        #     print("      ",name1)
        #self.showMessage("加载... ", QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.black)
        for i,path in enumerate(list):
            name=path.split('/')[-1]
            child = QTreeWidgetItem(item)
            item.addChild(child)
            child.setIcon(0,QIcon(self.setItem_Icon(name)))
            child.setText(0,name)
            # print(self.ftp.pwd())
            child.setToolTip(0,path)
            # print(child.toolTip(0))
            # print(this,name)


    # 动态加载dirItem
    def dirItem_new(self, item):
        # print(item.toolTip((0)))
        # list=self.ftp.nlst(str(item.toolTip(0)))
        child_num = item.childCount()
        for i in range(child_num):
            cc_num=item.child(i).childCount()
            item.child(i).setExpanded(False)
            if cc_num>=0:
                for j in range(cc_num):
                    item.child(i).removeChild(item.child(i).child(j))
            if self.checkFileDir(self.ftp, item.child(i).toolTip(0)) == "dir":
                self.dirItem(item.child(i))

        # time.sleep(10)


    """递归操作，耗费资源+加载时间久，放弃"""
    # 递归操作，遍历ftp服务器所有文件
    # def dirItem(self,list,item):
    #     # list=self.ftp.nlst(str(item.toolTip(0)))
    #     # self.showMessage("加载... ", QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.black)
    #     for i,name in enumerate(list):
    #         child = QTreeWidgetItem(item)
    #         item.addChild(child)
    #         child.setIcon(0,QIcon(self.setItem_Icon(name)))
    #         child.setText(0,name)
    #         child.setToolTip(0,self.ftp.pwd())
    #         # print(child.toolTip(0))
    #         # print(this,name)
    #         this = self.checkFileDir(self.ftp, name)
    #         if this == "dir":
    #             # print(self.ftp.pwd(), name)
    #             self.ftp.cwd(name)
    #             filelist=self.ftp.nlst()
    #             # for name1 in filelist:
    #             #     print("      ",name1)
    #             self.dirItem(filelist,child)
    #             self.ftp.cwd("..")

    # 判断是否为文件

    def checkFileDir(self,ftp, file_name):
        """
        判断当前目录下的文件与文件夹
        :param ftp: 实例化的FTP对象
        :param file_name: 文件名/文件夹名
        :return:返回字符串“File”为文件，“Dir”问文件夹，“Unknow”为无法识别
        """
        rec = ""
        try:
            rec = ftp.cwd(file_name)  # 需要判断的元素

            ftp.cwd("..")  # 如果能通过路径打开必为文件夹，在此返回上一级
        except ftplib.error_perm as fe:
            rec = fe  # 不能通过路劲打开必为文件，抓取其错误信息

        finally:
            # print(file_name,rec)
            if "550" in str(rec)[:3]:
                return "file"
            elif "250" in str(rec)[:3]:
                return "dir"
            else:
                return "unknow"

    # 单击选中，使能下载按键
    def select_item_ftp(self, item):
        # print(item.text(0),item.columnCount())
        self.select_item=item
        self.select_file = item.toolTip(0)
        if '.' in self.select_file:    # 如果是文件，则可下载
            self.Bt_down.setEnabled(True)
        else:  # 否则是文件夹，不能下载
            self.Bt_down.setEnabled(True)

    # 选择文件保存目录
    def select_item_local(self,obj):
        self.save_path=self.model.filePath(obj)

    # 更新主窗口显示
    def handleDisplay(self, data):
        if "ERROR" in data:
            self.Text_log.append(data)
            self.Bt_link.setEnabled(True)

        else:
            self.cursor = self.Text_log.textCursor()
            self.cursor.select(QTextCursor.LineUnderCursor)
            self.cursor.removeSelectedText()
            # self.Text_log.moveCursor(QtGui.QTextCursor.StartOfLine, QtGui.QTextCursor.MoveAnchor)
            self.Text_log.insertPlainText(data)
            if data=="100%":
                self.downing=True
                self.Text_log.append("Download Success!")
                self.thread.quit()
                # 执行命令
                # stdin：标准输入（就是你输入的命令）；stdout：标准输出（就是命令执行结果）；stderr:标准错误（命令执行过程中如果出错了就把错误打到这里），stdout和stderr仅会输出一个
                self.mv_file()
                self.Bt_down.setEnabled(False)

    # 移动文件
    # def mv_file(self):
    #     old_file=False
    #     path, file = os.path.split(self.select_file)
    #     print(self.ftp_root + path + "/old_file/")
    #     # s = self.ftp.mkd(path + "/old_file/")
    #     stdin, stdout, stderr = self.ssh.exec_command(
    #         "mkdir  %s" % (self.ftp_root + path + "/old_file/" ))
    #
    #     stdin, stdout, stderr = self.ssh.exec_command(
    #         "mv %s  %s" % (self.ftp_root + self.select_file, self.ftp_root + path + "/old_file/" + file))
    #     #
    #     # self.Text_log.append(str(stdout))
    #     parent = self.select_item.parent()
    #
    #     print(parent.toolTip(0))
    #     parent.setExpanded(False)
    #     parent.removeChild(self.select_item)
    #     child_num = parent.childCount()
    #     for i in range(child_num):
    #         if self.checkFileDir(self.ftp, parent.child(i).toolTip(0)) == "dir":
    #             if parent.child(i).text(0)=="old_file":
    #
    #                 old_file=True
    #     if old_file==False:
    #
    #         item_name = "old_file"
    #         child = QTreeWidgetItem(parent)
    #         parent.addChild(child)
    #         child.setIcon(0, QIcon(self.setItem_Icon(item_name)))
    #         child.setText(0, item_name)
    #         # print(self.ftp.pwd())
    #         child.setToolTip(0, path + "/old_file")
    #     # else:
    #         # child_num = parent.childCount()
    #         # for i in range(child_num):
    #         #     parent.removeChild(parent.child(i))
    #         # self.dirItem(parent)
    #
    #     parent.setExpanded(True)
    #     self.treeWidget_master.update()
        # self.select_item.setExpanded(True)

    # # 下载晚间操作
    # def Bt_down_run(self):
    #
    #     if self.save_path=="":
    #         self.Text_log.append("未选择保存路径")
    #         self.downing = True
    #         reply = QMessageBox.warning(self,
    #                                     "警告",
    #                                     "未选择保存路径",
    #                                     QMessageBox.Ok)
    #         return
    #
    #     if self.select_file=="":
    #         self.Text_log.append("未选择下载文件")
    #         self.downing = True
    #         reply = QMessageBox.warning(self,
    #                                     "警告",
    #                                     "未选择下载文件",
    #                                     QMessageBox.Ok)
    #         return
    #
    #     if self.downing == False:
    #         reply = QMessageBox.warning(self,
    #                                     "警告",
    #                                     "正在下载，请等待。。。",
    #                                     QMessageBox.Ok)
    #         return
    #     self.downing = False
    #     self.save_name = self.save_path + "/%s" % self.select_file.split('/')[-1]
    #     # print(self.select_file, self.save_name)
    #     self.Text_log.append("开始下载,\"%s\"将文件下载到\"%s\""%(self.select_file,self.save_name))
    #     if self.checkFileDir(self.ftp,self.select_file) =="dir":
    #         self.Text_log.append("这是文件夹，不能下载")
    #         return
    #
    #     print(self.save_name)
    #
    #     if os.path.exists(self.save_name):
    #         reply = QMessageBox.warning(self,
    #                                      "文件已存在",
    #                                      "是否覆盖？",
    #                                      QMessageBox.Yes | QMessageBox.No)
    #         if reply == QMessageBox.Yes:
    #             os.remove(self.save_name)
    #         else:
    #             self.downing = True
    #             return
    #
    #     # 创建线程
    #     self.down = down_Thread(self.ftp_tip,self.select_file,self.save_name)
    #     # self.down = down_Thread(self)
    #     # thread = MyThread(target=self.tcp_run, args=(self.ftp_tip,self.select_file,self.save_name))
    #     # target = self.ftp.retrbinary, args = ("RETR %s" % self.select_file, open(self.save_name, 'wb').write)
    #     # 连接信号
    #     self.down.update_date.connect(self.handleDisplay)
    #     self.thread = QThread()
    #     self.Text_log.append("0%")
    #     self.down.moveToThread(self.thread)
    #     # 开始线程
    #     self.thread.started.connect(self.down.run)
    #     self.thread.start()
