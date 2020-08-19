#!/usr/bin/python
# coding=utf-8
"""
Server对象用来定义server的ip、用户名、密码以及连接日志等属性，
包含connect方法用于ssh登陆, run_cmd方法用于执行linux命令
"""
import paramiko
import uuid

class SSHConnection(object):

    def __init__(self, host='192.168.2.103', port=22, username='root',pwd='123456'):
        self.host = host
        self.port = port
        self.username = username
        self.pwd = pwd
        self.__k = None
        #self.__transport = None

    def connect(self):
        transport = paramiko.Transport((self.host,self.port))
        transport.connect(username=self.username,password=self.pwd)
        self.__transport = transport

    def close(self):
        self.__transport.close()

    def upload(self,local_path,target_path):
        # 连接，上传
        # file_name = self.create_file()
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        # 将location.py 上传至服务器 /tmp/test.py
        sftp.put(local_path, target_path)

    def download(self,remote_path,local_path):
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        sftp.get(remote_path,local_path)

    def exeSynCmd(self, command):
        ssh = paramiko.SSHClient()
        ssh._transport = self.__transport
        # 执行命令
        stdin, stdout, stderr = ssh.exec_command(command)
        # 获取命令结果
        result = stdout.read()
        print (str(result,encoding='utf-8'))
        return result
    def exeASynCmd(self, command):
        ssh = paramiko.SSHClient()
        ssh._transport = self.__transport
        command = "nohup " + command + " >/dev/null 2>&1 &n"
        # 执行命令
        stdin, stdout, stderr = ssh.exec_command(command)
        # 获取命令结果
        result = stdout.read()
        print (str(result,encoding='utf-8'))
        return result
        
    def exeASynCmd2(self, command):
        #连接成功后打开一个channel
        xshellSSH  = paramiko.SSHClient()
        xshellSSH._transport = self.__transport
        channel = xshellSSH._transport.open_session()
        #设置会话超时时间
        channel.settimeout(30)
        #打开远程的terminal
        #channel.get_pty()
        #激活terminal
        #channel.invoke_shell()
        #然后就可以通过chan.send('command')和chan.recv(recv_buffer)来远程执行命令以及本地获取反馈。
        # 执行命令
        ret = {"true"}
        channel.exec_command(command)
        #chan.send(command)
        # 获取命令结果
        #result = stdout.read()
        #result=chan.recv(1024)
        #print (str(result,encoding='utf-8'))
        #return result

# 从文件读取servers信息ip 用户名 密码
def get_all_servers_login_info(server_file="./servers.txt"):
    try:
        f = open(server_file)
        all_servers = f.read()
    except:
        print("ERROR: 读取文件{0}失败".format(server_file))
    finally:
        f.close()
    all_servers = all_servers.split('\n')
    ssh_list = []
    for ssh in all_servers:
        if (len(ssh) > 0):
            ssh_list.append(ssh.split())
    return ssh_list

def main():
    # 读取servers.txt中的ip username password信息
    all_servers_info = get_all_servers_login_info()
    # 记录ssh登陆日志信息
    connection_log = ""
    for server in all_servers_info:
        ip, username, password = server[0], server[1], server[2]
        conn = SSHConnection(host=ip, username=username, pwd=password)
        conn.connect()
        conn.exeASynCmd("ls")
 
if __name__ == '__main__':
    main()