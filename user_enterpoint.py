#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__:"chenjing"
# date:2017/2/24
import getpass
import os
import subprocess
import hashlib, time

from django.contrib.auth import authenticate  # django验证用户密码


class UserPortal(object):
    """用户命令行端交互入口"""

    def __init__(self):
        self.user = None

    def user_auth(self):
        """完成用户交互"""
        retry_count = 0
        while retry_count < 3:
            username = input("Username:").strip()
            if len(username) == 0: continue
            password = getpass.getpass("Password:").strip()  # getpass模块不能再windows下调用
            if len(password) == 0:
                print("Password cannot bu null.")
                continue
            user = authenticate(username=username, password=password)
            if user:
                self.user = user
                print("welcome login...")
                return
            else:
                print("Invalid username or password!")
            retry_count += 1
        else:
            exit("Too many attempts.")

    def interactive(self):
        """交互函数"""
        self.user_auth()
        if self.user:  # 如果self.user有值即为真
            exit_flag = False
            while not exit_flag:
                # print(self.user.bind_hosts.select_related())  # 输出<QuerySet [<BindHost: nginx_01_11(192.168.31.11)@root:123456>]>
                # print(self.user.bind_hosts.select_related())  # 输出，和上面一样
                # 用户登录成功后，第一步：打印分组
                for index, host_group in enumerate(self.user.host_groups.all()):
                    print("%s. %s[%s]" % (index, host_group.name, host_group.bind_hosts.all().count()))

                """因为python特性,index循环完成之后，其值没有被释放"""
                print('%s. Ungrouped Hosts[%s]' % (index + 1, self.user.bind_hosts.all().count()))

                # 第二步：选择分组,并打印所选分组中的主机
                user_input = input("Choose Group:").strip()
                if len(user_input) == 0: continue
                if user_input.isdigit():
                    user_input = int(user_input)
                    if user_input >= 0 and user_input < self.user.host_groups.all().count():
                        selected_hostgroup = self.user.host_groups.all()[user_input]
                    elif user_input == self.user.host_groups.all().count():  # 选中了"未分组"组
                        selected_hostgroup = self.user
                        """这里有一个小技巧，因为self.user和self.user.host_groups都有一个多对多外键bind_hosts"""
                    else:
                        print("invalid hostgroup")
                        continue

                    while True:
                        for index, bind_host in enumerate(selected_hostgroup.bind_hosts.all()):
                            print("%s. %s(%s user:%s)" % (index,
                                                          bind_host.host.hostname,
                                                          bind_host.host.ip_addr,
                                                          bind_host.host_user.username))

                        # 第三步：选择主机
                        user_input2 = input("Choose Host:").strip()
                        if len(user_input2) == 0: continue
                        if user_input2.isdigit():
                            user_input2 = int(user_input2)
                            if user_input2 >= 0 and user_input2 < selected_hostgroup.bind_hosts.all().count():
                                selected_bindhost = selected_hostgroup.bind_hosts.all()[user_input2]
                                print("logging host", selected_bindhost)

                                # 第四步：使用SSH原生客户端sshpass登录选中的主机（代码必须运行在windows）
                                md5_str = hashlib.md5(str(time.time()).encode()).hexdigest()
                                # login_cmd格式：sshpass -p 123456 ssh root@192.168.31.11 -o "StrictHostKeyChecking no"
                                login_cmd = 'sshpass -p {password} /usr/local/openssh7/bin/ssh {user}@{ip_addr} -o "StrictHostKeyChecking no" -Z {md5_str}'.format(
                                    password=selected_bindhost.host_user.password,
                                    user=selected_bindhost.host_user.username,
                                    ip_addr=selected_bindhost.host.ip_addr,
                                    md5_str=md5_str)

                                # start session tracker script 调用shell脚本
                                session_tracker_script = settings.SESSION_TRACKER_SCRIPT
                                tracker_obj = subprocess.Popen("%s %s" % (session_tracker_script, md5_str),
                                                               shell=True, stdout=subprocess.PIPE,
                                                               stderr=subprocess.PIPE,
                                                               cwd=settings.BASE_DIR)

                                # create session log
                                models.SessionLog.objects.create(user=self.user, 
                                                                 bind_host=selected_bindhost,
                                                                 session_tag=md5_str)

                                ssh_instance = subprocess.run(login_cmd, shell=True)  # 执行命令
                                print("------------logout---------")
                                print("session tracker output:",
                                      tracker_obj.stdout.read().decode(),
                                      tracker_obj.stderr.read().decode())

                        if user_input2 == "b":
                            break


if __name__ == "__main__":
    # 下面三行实现了用户py文件调用django环境
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CrazyAss.settings")
    import django
    from django.conf import settings

    django.setup()
    from audit import models

    portal = UserPortal()
    portal.interactive()
