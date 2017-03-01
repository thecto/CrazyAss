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
    strace



演示步骤：
    使用公共账号登录堡垒机
    ssh crazyass@192.168.31.21  #密码123456

    然后输入django中的个人账户进入跳板机
    Username:chen@126.com
    Password:Chen1234
    welcome login...


使用strace捕获用户输入的命令：
sudo strace -f -p 2095 -ttt -o xx.log
    -f:跟踪-p后面的当前程序，以及其创建的子程序的系统调用，一般与-p结合使用
    -p:pid
    -o:将跟踪到的系统调用输出到文件中，默认输出到屏幕上
    -ttt:以毫秒形式显示时间戳

编译openssh-server，给其添加增加一个选项：
    sudo apt-get install zlib1g
    sudo apt-get install zlib1g-dev
    sudo apt-get install libssl-dev

    修改ssh.c
        while ((opt = getopt(ac, av, "1246ab:c:e:fgi:kl:m:no:p:qstvxz:"
	    "ACD:E:F:GI:J:KL:MNO:PQ:R:S:TVw:W:XYyZ:")) != -1) {
		switch (opt) {
            case 'Z':
            fprintf(stdout,"session_tag: %s\n", optarg);
            break;
        }

    sudo chmod +x configure mkinstalldirs
    ./configure --prefix=/usr/local/openssh7
    make && sudo make install

修改sudo配置文件，使crazyass用户可以在sudo时不用输入密码
    sudo vim /etc/sudoers
        %crazyass ALL=NOPASSWD:ALL #/usr/bin/strace,/usr/bin/python3
        %crazyass ALL=NOPASSWD:/usr/bin/strace



测试：
chen@ubuntu:/home/crazyass/CrazyAss$ sudo runuser -l crazyass -c 'python3.5 CrazyAss/manage.py runserver 0.0.0.0:9000'
因为启动crazyass时会自动调用那个脚本，就需要在其他用户下执行crazyass 下的程序

