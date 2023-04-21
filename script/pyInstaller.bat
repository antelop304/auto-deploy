echo build  initConfig.exe......
python -m PyInstaller -Fw initConfig.py -i statics\logo.png -n initConfig --distpath out

echo build  initConfig.exe......
python -m PyInstaller -Fw systemTray.py -i statics\logo.png -n startup --distpath out

echo build initConfig.exe......
python -m PyInstaller -Fw shutdownAll.py -i statics\logo.png -n shutdownAll --distpath out

echo succeed!!
pause
