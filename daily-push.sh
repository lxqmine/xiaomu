#!/bin/bash
cd /root/.openclaw/workspace
DATE=$(date +%Y-%m-%d)

git add .
git commit -m "daily update: $DATE"
git push origin master