@echo off
cd /d "%~dp0"
set /p msg=description: 
git add .
git commit -m "%msg%"
git push
echo done
pause
