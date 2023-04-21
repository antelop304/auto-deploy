import os
import pystray
import time
import subprocess
import threading
from PIL import Image
import win32api
import win32con
import win32gui
import socket
from sys import exit
import webbrowser

msgtitle = "提醒"
# 软件所有端口
soft_ports = [13100, 13101, 13102, 11042, 14104]
currentPath = os.getcwd()
javaFilePath = currentPath + '/java/bin/javaw.exe'

def runCmds(cmds):
  for cmd in cmds:
    print(cmd)
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def startJavaHomePath():
  cmds = [
    f'SETX JAVA_HOME {currentPath}\\java',
    f'SET Classpath=%JAVA_HOME%/lib/tools.jar;%JAVA_HOME%/lib/dt.jar;',
    f'SET Path=%JAVA_HOME%/bin']
  runCmds(cmds)

def startMySql():
  cmds = [
    'staring 1-4 mysql',
    f'start /b {currentPath}/mysql/bin/mysqld --defaults-file={currentPath}/mysql/my.ini --console']
  runCmds(cmds)

def startRedis():
  cmds = [
     'echo staring 2-4 redis',
     f'start /b {currentPath}/redis/redis-server.exe {currentPath}/redis/redis.windows.conf']
  runCmds(cmds)

def startNacos():
  cmds = [
     'echo staring 3-4 nacos',
     f'start /b {currentPath}/nacos-server/bin/startup.cmd -m standalone']
  runCmds(cmds)

def startZookeeper():
  cmds = [
     'echo staring 3-4 zookeeper',
     f'start /b {currentPath}/apache-zookeeper/bin/zkServer.cmd']
  runCmds(cmds)

def startNginx():
  cmds = [
     'echo staring 4-4 nginx',
     f'start /b {currentPath}/nginx/nginx.exe -c {currentPath}/nginx/conf/nginx.conf -p {currentPath}/nginx/']
  runCmds(cmds)

def startCaddy():
  cmds = [
     'echo staring 4-4 caddy',
     f'start /b {currentPath}/caddy/startup.bat']
  runCmds(cmds)

def startPackages():
  cmds = [
    f'start {javaFilePath} -Xms512m -Xmx512m -jar {currentPath}/packages/back.jar > {currentPath}/packages/logs/back.txt 2>&1 &']
  runCmds(cmds)

def startupAll():
  # REM 1.base soft: start mysql, redis, nacos, nginx
  startJavaHomePath()
  startZookeeper()
  startMySql()
  startRedis()
  time.sleep(15)
  # startNacos()
  # time.sleep(10)
  # startNginx()
  startCaddy()
  # REM 2.packages
  startPackages()
  print('echo startup all done')

def shutdownAll():
  cmds = [
    'echo killing packages',
    'taskkill /f /im javaw.exe',
    'echo killing redis,nginx,nacos,mysql',
    'taskkill /f /im redis-server.exe',
    # 'taskkill /f /im nginx.exe',
    'taskkill /f /im caddy.exe',
    'taskkill /f /im mysqld.exe',
    # f'start /b {currentPath}/nacos-server/bin/shutdown.cmd'
    ]
  runCmds(cmds)
  print('echo all done')

def on_quit_clicked():
    # 点击退出菜单项时调用的函数
    shutdownAll()
    icon.stop()

def on_open_clicked():
    # 点击打开菜单项时调用的函数
    shutdownAll()
    startupAll()

# 提示信息框
def popMsg(content):
  win32api.MessageBox(0, content, msgtitle, win32con.MB_ICONASTERISK)

# 关闭提示框
def closeMesgBox(title):
  hwnd = win32gui.FindWindow(None, msgtitle)
  if hwnd:
      try:
          win32gui.EndDialog(hwnd, win32con.IDCLOSE)
      except Exception as e:
          print("dialog[{}]close fail：{}".format(title, e))

# 检查端口是否被占用
def check_port_in_use(port, host='127.0.0.1'):
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((host, int(port)))
        return True
    except socket.error:
        return False
    finally:
        if s:
           s.close()

# 步骤一：软件用到的端口是否被占用
usedPorts = []
for port in soft_ports:
  if(check_port_in_use(port)):
      usedPorts.append(port)

if(len(usedPorts) > 0):
    popMsg(f'端口：{usedPorts}被占用，请关闭后重试！')
    exit()

# 步骤二：创建系统托盘图标
menu = (pystray.MenuItem('重启', on_open_clicked),
        pystray.MenuItem('退出', on_quit_clicked))
image = Image.open('statics/logo.png') # 替换成你要使用的托盘图标路径
icon = pystray.Icon('systemTool', image, 'antelop', menu)
# 注册托盘图标的点击事件
print('icon done')

# 启动托盘
threading.Thread(target=icon.run).start()
threading.Thread(target=lambda: popMsg("启动中......"), daemon=True).start()

# 步骤三：启动所有应用软件以及程序包
startupAll()
time.sleep(60)
print('startupAll done')

closeMesgBox(msgtitle)
# threading.Thread(target=lambda: popMsg("启动成功！"), daemon=True).start()

# 步骤四：尝试调用浏览器打开网页
try:
  webbrowser.open("http://localhost:11042/")
except webbrowser.Error:
  print("打开默认浏览器失败，请手动打开。")
  threading.Thread(target=lambda: popMsg("启动成功！"), daemon=True).start()
