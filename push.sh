#!/bin/bash
cd "$(dirname "$0")"
git add .
read -p "输入提交说明: " msg
git commit -m "$msg"
git push
echo "✅ 推送完成"
