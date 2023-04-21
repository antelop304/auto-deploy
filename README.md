# auto-deploy-package

## window环境一键安装部署java web项目

> 效果为将所有的中间件与前后端程序一起打包exe文件，用户安装后，点击桌面exe启动程序，生成一个系统托盘，用户点击托盘可以退出程序。
- 因nacos-server和nginx在安装中文目录会有问题，故使用apache-zookeeper和caddy代替。
```
 打包软件为：Inno Setup
 安装所需中间件包含：mysql、java、apache-zookeeper[可用nacos-server代替]、caddy[可用nginx代替]、redis。
 系统托盘程序使用python编写，bat文件转exe文件使用 PyInstaller，打包后为Antelop.exe安装包，双击进行安装，如果安装环境未安装vc++ 2013，会预先进行安装，然后再进行程序安装。
 安装完成，会将程序的所有软件包解压到用户选择安装的目录
```
安装后目录结构：
```
  > initConfig.exe                      - 初始化配置
  > startup.exe                         - 启动程序
  > shutdownAll.exe                     - 关闭程序
  > unins000.dat
  > unins000.exe
  > apache-zookeeper                    - 注册中心
  > caddy                               - 接口代理
  > java
  > mysql                               - 数据库
  > redis
  > statics
    > logo.png                            - 系统托盘logo
  > packages                            - 程序包文件
    > front                               - 前端静态页面
    > back.jar
```

# 软件以及端口配置
- 1.打包安装包工具：Inno Setup 6.2.2 [Inno Setup下载](https://jrsoftware.org/isdl.php)
  [vcredist_x64下载](https://aka.ms/vs/17/release/vc_redist.x86.exe)
```
  > 安装Inno Setup 软件后，项目打包脚本文件：auto-deploy.iss
  > 修改[Files]中的【Source】配置路径。默认安装中间件为：mysql、java、apache-zookeeper[可用nacos-server代替]、caddy[可用nginx代替]、redis
  > 安装完成执行软件配置 [Run] Filename: "{app}\initConfig.exe";
  > [Code]部分内容为默认安装mysql程序依赖vc++ 2013 redist x64
  > 打包软件目录结构为：
      > initConfig.exe                      - 初始化配置，通过script/initConfig.py生成
      > startup.exe                         - 启动程序，通过script/systemTray.py生成
      > shutdownAll.exe                     - 关闭程序，通过script/shutdownAll.py生成
      > vcredist_x64.exe                    - vc++ 2013
      > apache-zookeeper                    - 注册中心
        > conf
          > zoo.cfg
        > bin
          > zkServer.cmd
          > zkEnv.cmd
      > caddy                               - 接口代理
        > caddy.exe
        > Caddyfile
        > startup.bat
      > java
      > mysql                               - 数据库
        > my.ini
        > db
      > reids
        > redis-server.exe
        > redis.windows.conf
      > statics
        > logo.png                            - 系统托盘logo
      > packages                            - 程序包文件
        > front                                - 前端静态页面
        > back.jar
```  
- 2.mysql:
  mysql为绿色版本,需初始化默认数据库。 [下载地址](https://dev.mysql.com/downloads/mysql/5.7.html)
```
  > 端口：13100
  > 版本: 5.7.25
  > 默认数据库：back
  > 配置文件my.ini初始化：basedir、datadir配置项
```
<details><summary>点击查看my.ini配置</summary>

```properties
[mysql]
default-character-set=utf8
[mysqld]
port = 13100
basedir=D:/soft/mysql
datadir=D:/soft/mysql/db/
max_connections=200
character-set-server=utf8
default-storage-engine=INNODB
max_allowed_packet = 6M

sql_mode=STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION
```
</details>

- 3.1 zookeeper [下载地址](https://zookeeper.apache.org/releases.html) ，可用nacos-server代替，但是安装中文目录会有问题。
  修改配置文件：/bin/zkEnv.cmd，将【java】修改为【javaw】,支持后台启动
```
  > 端口：clientPort：13101
  > 版本：3.8.1
  > 配置文件zoo.cfg初始化
    > dataDir={app}/apache-zookeeper/data
    > dataLogDir={app}/apache-zookeeper/log
```

<details>
<summary>点击查看修改配置内容</summary>

修改部分内容为：
```shell
if not exist "%JAVA_HOME%"\bin\java.exe (
  echo Error: JAVA_HOME is incorrectly set: %JAVA_HOME%
  echo Expected to find java.exe here: %JAVA_HOME%\bin\java.exe
  goto :eof
)

REM strip off trailing \ from JAVA_HOME or java does not start
if "%JAVA_HOME:~-1%" EQU "\" set "JAVA_HOME=%JAVA_HOME:~0,-1%"
 
set JAVA="%JAVA_HOME%"\bin\java
```  
修改为
```shell
if not exist "%JAVA_HOME%"\bin\javaw.exe (
  echo Error: JAVA_HOME is incorrectly set: %JAVA_HOME%
  echo Expected to find javaw.exe here: %JAVA_HOME%\bin\javaw.exe
  goto :eof
)

REM strip off trailing \ from JAVA_HOME or java does not start
if "%JAVA_HOME:~-1%" EQU "\" set "JAVA_HOME=%JAVA_HOME:~0,-1%"
 
set JAVA="%JAVA_HOME%"\bin\javaw
```
</details>

- 3.2 nacos-server
```
  > 端口：clientPort：13101
  > 版本：2.0.4
  > 配置文件 conf/application.properties：
    > server.port=13101
    > db.url.0=jdbc:mysql://127.0.0.1:3306/config?characterEncoding=utf8&connectTimeout=1000&socketTimeout=3000&autoReconnect=true&useUnicode=true&useSSL=false&serverTimezone=UTC
    > db.user.0=antelop
    > db.password.0=antelop123.
```
修改配置文件：/bin/startup.cmd，将【java】修改为【javaw】,支持后台启动；
<details>
<summary>点击查看修改配置内容</summary>

修改部分内容为：
```shell
if not exist "%JAVA_HOME%\bin\java.exe" echo Please set the JAVA_HOME variable in your environment, We need java(x64)! jdk8 or later is better! & EXIT /B 1
set "JAVA=%JAVA_HOME%\bin\java.exe"
```
修改为：
```shell
if not exist "%JAVA_HOME%\bin\javaw.exe" echo Please set the JAVA_HOME variable in your environment, We need java(x64)! jdk8 or later is better! & EXIT /B 1
set "JAVA=%JAVA_HOME%\bin\javaw.exe"
```
</details>

- 4.redis [下载地址](https://github.com/tporadowski/redis/releases)
```
  > 端口: 13102
  > 版本：5.0.14
  > 密码：antelop123
  > 配置文件redis.windows.conf
    > port 13102
    > requirepass antelop123
```
- 5.1 caddy，前端项目接口代理，可用nginx代替，但是安装中文目录会有问题。
```
  > 端口: 前端：11042
  > 代理："/stage-api/*" ---> "localhost:14100"
  > 配置文件 Caddyfile
  > 启动文件 startup.bat
```
<details><summary>点击查看配置内容</summary>

配置文件 Caddyfile
```yaml
    :11042 {
      root ../packages/front
      file_server
      handle_path /stage-api/* {
          reverse_proxy localhost:14100
      }
    }
```
启动文件 startup.bat
```shell
    pushd D:\soft\caddy
    start /b caddy.exe run
```
</details>

- 5.2 nginx
```
  > 端口: 前端：11042
  > 代理："/stage-api/*" ---> "localhost:8080"
  > 配置文件 conf/nginx.conf
```
<details><summary>点击查看nginx.conf配置</summary>

```yaml
server {
      listen       1042;
      server_name  localhost;
      location / {
          root   html;
          index  index.html index.htm;
      }
      location /index/ {
          proxy_pass http://127.0.0.1:1042/;
      }
      location /stage-api/ {
          proxy_pass http://127.0.0.1:14100/; 
      }
  }
```
</details>

- 6.项目默认应用端口，
```
  > front: 14104
```
- 7.系统脚本 script
- 1. initConfig.py 初始化配置项
```
   mysql配置文件【my.ini】basedir、datadir配置项
   zookeeper配置文件【/conf/zoo.cfg】dataLogDir、dataDir配置项
   caddy配置文件【startup.bat】
```
- 2. systemTray.py 系统托盘程序
```
  步骤一：软件用到的端口是否被占用
  步骤二：创建系统托盘图标
  步骤三：启动所有应用软件以及程序包
  步骤四：尝试调用浏览器打开网页
```
- 3. shutdownAll.py 关闭程序
- 4. pyInstaller.bat 打包脚本
```
  > 需要安装 PyInstaller
  > 打包图标可以替换 statics/logo.png
```
