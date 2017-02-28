# CrazyAss
## 使用python开发的跳板机程序

### 环境：
    ubuntu 16.04 server
    sudo apt-get install sshpass
    pip3 install django
    （注意：如果当时使用用户chen安装python包，则所有包安装在/home/chen/.local/lib/python3.5/site-packages/，
    而我们这里使用用户crazyass执行代码，所以只需要将/home/chen/.local/拷贝到/home/crazyass/并修改权限即可。）
    
    sudo adduser crazyass
    su - crazyass  ##密码123456
    git clone https://github.com/thecto/CrazyAss.git
    vim .bashrc
        # for crazyass only
        python3.5 CrazyAss/user_enterpoint.py
        lougout

### TODO
    输入审计
    批量命令输入/文件上传下载
    前端可视化
