#!/usr/bin/env python3
"""
视频分析工具 - 一键获取视频信息
用法: python video_fetch.py <平台> <链接/ID>
"""

import sys
import json
import subprocess
import requests

TAVILY_KEY = "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"

def fetch_bilibili(bvid):
    """获取B站视频信息"""
    url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
    headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://www.bilibili.com"}
    r = requests.get(url, headers=headers, timeout=10).json()
    data = r.get("data", {})
    if not data:
        return "❌ 获取失败"
    
    return f"""
🎬 {data.get('title', '无标题')}
👤 {data.get('owner', {}).get('name', '未知')}
⏱️ {data.get('duration', 0)//60}分钟
👁️ {data.get('stat', {}).get('view', 0):,} 次播放
👍 {data.get('stat', {}).get('like', 0):,} 次点赞
📅 {data.get('pubdate', 0)}
🔗 https://www.bilibili.com/video/{bvid}
"""

def search_video(keyword):
    """搜索视频"""
    url = "https://api.tavily.com/search"
    data = {
        "api_key": TAVILY_KEY,
        "query": keyword,
        "max_results": 5
    }
    r = requests.post(url, json=data, timeout=15).json()
    results = r.get("results", [])
    
    if not results:
        return "❌ 未找到相关视频"
    
    output = f"🔍 搜索结果: {keyword}\n\n"
    for i, item in enumerate(results, 1):
        output += f"{i}. {item.get('title', '无标题')}\n"
        output += f"   {item.get('content', '无描述')[:150]}...\n"
        output += f"   🔗 {item.get('url', '')}\n\n"
    return output

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\n📌 示例:")
        print("  python video_fetch.py bilibili BV1WT4y1s7u4")
        print("  python video_fetch.py search 狗总 黄金")
        return
    
    cmd = sys.argv[1].lower()
    
    if cmd == "bilibili" and len(sys.argv) > 2:
        print(fetch_bilibili(sys.argv[2]))
    elif cmd == "search" and len(sys.argv) > 2:
        keyword = " ".join(sys.argv[2:])
        print(search_video(keyword))
    else:
        print(__doc__)

if __name__ == "__main__":
    main()