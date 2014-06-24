@echo off
set srcFile="%~dp0\csdnblog_publish.py"
set linkFile="%~dp0\csdnblog_publish.py.lnk"
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = %linkFile% >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = %srcFile% >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs
cscript CreateShortcut.vbs
del CreateShortcut.vbs

set path1="C:\Users\All Users\Microsoft\Windows\Start Menu\Programs\Startup\"
set path2="C:\Users\%USERNAME%\Microsoft\Windows\Start Menu\Programs\Startup\"
set path3="C:\Documents and Settings\All Users\「开始」菜单\程序\启动\"
set path4="C:\Documents and Settings\%USERNAME%\「开始」菜单\程序\启动\"
if exist %path1% (
	copy %linkFile% %path1%
	echo successfully1
	exit
)
if exist %path2% (
	copy %linkFile% %path2%
	echo successfully2
	exit
)    
if exist %path3% (
	copy %linkFile% %path3%
	echo successfully3
	exit
)
if exist %path4% (
	copy %linkFile% %path4%
	echo successfully4
	exit
)
echo failed
pause