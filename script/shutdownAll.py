import os
import subprocess

currentPath = os.getcwd()

def runCmds(cmds):
  for cmd in cmds:
    print(cmd)
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

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

shutdownAll()
