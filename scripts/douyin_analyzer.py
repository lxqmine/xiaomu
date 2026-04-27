#!/usr/bin/env python3
"""
抖音博主深度分析工具
用法: python douyin_analyzer.py <博主名或主页链接>
"""

import sys
import re
import json
import requests
from datetime import datetime

TAVILY_KEY = "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"

def search_creator(keyword):
    """搜索博主信息"""
    url = "https://api.tavily.com/search"
    data = {
        "api_key": TAVILY_KEY,
        "query": f"抖音 {keyword} 博主 主页 粉丝",
        "search_depth": "advanced",
        "max_results": 8
    }
    try:
        r = requests.post(url, json=data, timeout=20).json()
        return r.get("results", [])
    except Exception as e:
        return []

def search_videos(keyword, limit=10):
    """搜索博主视频"""
    url = "https://api.tavily.com/search"
    data = {
        "api_key": TAVILY_KEY,
        "query": f"抖音 {keyword} 视频",
        "search_depth": "advanced",
        "max_results": limit
    }
    try:
        r = requests.post(url, json=data, timeout=20).json()
        return r.get("results", [])
    except:
        return []

def analyze_creator(name):
    """分析博主"""
    print(f"🔍 正在分析博主: {name}\n")
    print("="*50)
    
    # 1. 搜索博主信息
    print("\n📊 博主信息\n")
    creator_results = search_creator(name)
    if creator_results:
        for i, item in enumerate(creator_results[:3], 1):
            print(f"{i}. {item.get('title', '无标题')}")
            content = item.get('content', '')[:300]
            print(f"   {content}")
            print(f"   🔗 {item.get('url', '')}\n")
    else:
        print("   未找到博主信息")
    
    # 2. 搜索视频内容
    print("\n🎬 相关视频\n")
    video_results = search_videos(name, 5)
    if video_results:
        for i, item in enumerate(video_results, 1):
            print(f"{i}. {item.get('title', '无标题')}")
            content = item.get('content', '')[:200]
            print(f"   {content}")
            print(f"   🔗 {item.get('url', '')}\n")
    else:
        print("   未找到相关视频")
    
    # 3. 输出分析建议
    print("\n" + "="*50)
    print("📝 分析建议\n")
    print("基于搜索结果，建议关注：")
    print("1. 博主内容定位和风格")
    print("2. 高播放量视频的共同特点")
    print("3. 评论区互动（需要打开链接查看）")
    print("4. 更新频率和发布时间规律")
    
    print("\n💡 如需深度分析，请提供：")
    print("   - 具体视频链接")
    print("   - 想分析的角度（内容/风格/互动/变现）")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\n📌 示例:")
        print("  python douyin_analyzer.py 葵木君")
        print("  python douyin_analyzer.py 'https://www.douyin.com/user/xxx'")
        return
    
    keyword = " ".join(sys.argv[1:])
    analyze_creator(keyword)

if __name__ == "__main__":
    main()