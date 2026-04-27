#!/usr/bin/env python3
"""
抖音视频分析工具
用法: python douyin_fetch.py <视频链接或ID>
"""

import sys
import re
import json
import requests

TAVILY_KEY = "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"

def extract_video_id(url_or_id):
    """从URL提取视频ID"""
    # 直接是ID
    if url_or_id.isdigit():
        return url_or_id
    
    # 从URL提取
    patterns = [
        r'video/(\d+)',
        r'aweme_id=(\d+)',
        r'/(\d{19})',
    ]
    for p in patterns:
        m = re.search(p, url_or_id)
        if m:
            return m.group(1)
    return None

def fetch_douyin_info(video_id):
    """获取抖音视频信息（通过搜索）"""
    url = "https://api.tavily.com/search"
    data = {
        "api_key": TAVILY_KEY,
        "query": f"抖音视频 {video_id}",
        "max_results": 3
    }
    try:
        r = requests.post(url, json=data, timeout=15).json()
        results = r.get("results", [])
        if results:
            output = f"🎬 抖音视频搜索结果\n\n"
            for i, item in enumerate(results, 1):
                output += f"{i}. {item.get('title', '无标题')}\n"
                output += f"   {item.get('content', '无描述')[:200]}\n"
                output += f"   🔗 {item.get('url', '')}\n\n"
            return output
    except Exception as e:
        return f"❌ 搜索失败: {e}"
    
    return "❌ 未找到相关信息"

def search_douyin_user(keyword):
    """搜索抖音博主"""
    url = "https://api.tavily.com/search"
    data = {
        "api_key": TAVILY_KEY,
        "query": f"抖音 {keyword} 博主",
        "max_results": 5
    }
    try:
        r = requests.post(url, json=data, timeout=15).json()
        results = r.get("results", [])
        if not results:
            return "❌ 未找到相关博主"
        
        output = f"🔍 抖音博主搜索: {keyword}\n\n"
        for i, item in enumerate(results, 1):
            output += f"{i}. {item.get('title', '无标题')}\n"
            output += f"   {item.get('content', '无描述')[:200]}\n"
            output += f"   🔗 {item.get('url', '')}\n\n"
        return output
    except Exception as e:
        return f"❌ 搜索失败: {e}"

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\n📌 示例:")
        print("  python douyin_fetch.py <视频链接或ID>")
        print("  python douyin_fetch.py search <博主关键词>")
        return
    
    cmd = sys.argv[1].lower()
    
    if cmd == "search" and len(sys.argv) > 2:
        keyword = " ".join(sys.argv[2:])
        print(search_douyin_user(keyword))
    else:
        # 尝试提取视频ID
        video_id = extract_video_id(sys.argv[1])
        if video_id:
            print(fetch_douyin_info(video_id))
        else:
            print("❌ 无法识别的视频链接或ID")

if __name__ == "__main__":
    main()