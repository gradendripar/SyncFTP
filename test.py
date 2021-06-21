import logging
from ftplib import FTP

class MyFtp():
    def __init__(self):
        self.ftp = FTP()

    # 些函数实现ftp登录
    def ftp_login(self,host_ip,username,password):
        try:
            self.ftp.connect(host_ip, port=21, timeout=10)
        except :
            logging.warning('network connect time out')
            return 1001
        try:
            self.ftp.login(user=username, passwd=password)
        except:
            logging.warning('username or password error')
            return 1002
        return 1000

    # 此函数执行ftp命令，并打印命令执行结果
    def execute_some_command(self):
        # 通运sendcmd方法形式执行pwd命令，为使用形式统一起见不推荐使用此种形式，而且其实大多数命令都是支持这种形式的
        command_result = self.ftp.nlst()
        logging.warning('command_result:%s'% command_result)
        # 通过直接使用pwd方法执行pwd命令，推荐统一使用此种形式
        command_result = self.ftp.pwd()
        logging.warning('command_result:%s' % command_result)
        # 上传文件；'stor ftp.py'告诉服务端将上传的文件保存为ftp_client.py，open()是以二进制读方式打开本地要上传的文件
        command_result = self.ftp.storbinary('stor SyncFTP.zip', open("../SyncFTP.zip", 'rb'))
        logging.warning('command_result:%s' % command_result)
        # 下载文件；'retr .bash_profile'告诉服务端要下载服务端当前目录下的.bash_profile文件，open()是以二进制写方式打开本地要存成的文件
        command_result = self.ftp.retrbinary('retr download.py', open('local.txt', 'wb').write)
        logging.warning('command_result:%s' % command_result)

    # 此函数实现退出ftp会话
    def ftp_logout(self):
        logging.warning('now will disconnect with server')
        self.ftp.close()

if __name__ == '__main__':
    # 要连接的主机ip
    host_ip = '49.232.138.204'
    # 用户名
    username = 'renjijiaohu-ftp'
    # 密码
    password = 'eCAGMB3SDaGKxG6R'
    # 实例化
    my_ftp = MyFtp()
    # 如果登录成功则执行命令，然后退出
    if my_ftp.ftp_login(host_ip,username,password) == 1000:
        logging.warning('login success , now will execute some command')
        my_ftp.execute_some_command()
        my_ftp.ftp_logout()