#!/usr/bin/python
# coding=utf-8
import paramiko
class Server():
    def __init__(self, ip, username, password):
        self.username = username
        self.password = password
        self.ip = ip
        self.connect_result = ""

    # ssh登陆并反馈连接成功或失败信息
    def connect(self):
        conn = paramiko.SSHClient()
        conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            conn.connect(self.ip, username=self.username, password=self.password)
            self.connection = conn
            self.connect_result = "Connect Server {0} {1} {2} Successfully!\n".format(
                self.ip, self.username, self.password)
        except:
            self.connect_result = "Connect Server {0} {1} {2} Failed!\n".format(
                self.ip, self.username, self.password)
            #不能正常连接的server打印信息到控制台
            print(self.connect_result)
        return self.connect_result

    # 该方法运行建立连接后执行linux命令
    def run_cmd(self, command):
        if self.connection is None:
            print("Please run connect")
            raise ValueError("Not connected")
        (stdin, stdout, stderr) = self.connection.exec_command(command)
        return stdout.read()

# 从文件读取servers信息ip 用户名 密码
def get_all_servers_login_info(server_file="./serversLst.txt"):
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

if __name__ == '__main__':
    # 读取servers.txt中的ip username password信息
    all_servers_info = get_all_servers_login_info()
    # 记录ssh登陆日志信息
    connection_log = ""
    # 逐个检查每个server ssh登陆情况
    for server in all_servers_info:
        ip, username, password = server[0], server[1], server[2]
        conn = Server(ip, username, password)
        connection_log += conn.connect()
    # 将所有服务器ssh登陆检查信息写入日志文件
    log_file = open("connect_result.log", 'w')
    log_file.write(connection_log)
    log_file.close()
