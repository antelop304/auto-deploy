import os
currentPath = os.getcwd()
newLineList = []
# init mysql config
with open(f'{currentPath}/mysql/my.ini', 'r') as file:
    lineList = file.readlines()
    for line in lineList:
      if ('basedir' in line):
        line = f'basedir={currentPath}\\mysql\r\n'
      elif('datadir' in line):
        line = f'datadir={currentPath}\\mysql\\db\r\n'
      newLineList.append(line)

with open(f'{currentPath}/mysql/my.ini', 'w') as file:
   file.writelines(newLineList)

# init zookeeper config
newLineList = []
with open(f'{currentPath}/apache-zookeeper/conf/zoo.cfg', 'r', encoding= 'ANSI') as file:
    lineList = file.readlines()
    for line in lineList:
      if ('dataLogDir' in line):
        line = f'dataLogDir={currentPath}\\apache-zookeeper\\log\r\n'.replace('\\', '/')
      elif('dataDir' in line):
        line = f'dataDir={currentPath}\\apache-zookeeper\\data\r\n'.replace('\\', '/')
      newLineList.append(line)

with open(f'{currentPath}/apache-zookeeper/conf/zoo.cfg', 'w') as file:
   file.writelines(newLineList)

# init caddy config
with open(f'{currentPath}/caddy/startup.bat', 'w', encoding= 'ANSI') as file:
   newLineList = [
      f'pushd {currentPath}\\caddy\r\n',
      'start /b caddy.exe run']
   file.writelines(newLineList)
