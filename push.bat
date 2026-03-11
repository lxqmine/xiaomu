@echo off
cd /d "%~dp0"
set /p msg=输入提交说明: 
git add .
git commit -m "%msg%"
git push
echo 推送完成
pause
