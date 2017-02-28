管理员用户:
启动django服务：python3.5 manage.py runserver 0.0.0.0:800
入口：http://127.0.0.1:8000/admin/或者python3.5 CrazyAss/user_enterpoint.py
账户/密码：chen@126.com/Chen1234

代码必须运行在linux主机上

linux上需要执行的命令：
    sudo adduser crazyass
    vim .bashrc
        # for crazyass only
        python3.5 CrazyAss/user_enterpoint.py
        lougout

    pip3 install django
    (注意：如果当时使用用户chen安装python包，则所有包安装在/home/chen/.local/lib/python3.5/site-packages/，
    而我们这里使用用户crazyass执行代码，所以只需要将/home/chen/.local/拷贝到/home/crazyass/并修改权限即可)

需要安装的程序：
    sshpass



演示步骤：
    使用公共账号登录堡垒机
    ssh crazyass@192.168.31.21  #密码123456

    然后输入django中的个人账户进入跳板机
    Username:chen@126.com
    Password:Chen1234
    welcome login...

