---
name: video-analyzer
description: 视频内容分析工具。支持抓取视频文案、评论、下载视频、提取关键帧。适用于抖音、B站、YouTube等平台。触发词：分析视频、视频内容、提取视频。
---

# 视频分析工具

## 能力范围

| 能力 | 状态 | 说明 |
|------|------|------|
| 抓取视频文案/简介 | ✅ | 通过搜索 API 获取 |
| 抓取评论热评 | ⚠️ | 部分平台可获取 |
| 下载视频 | ⚠️ | 需要公开链接，抖音需登录 |
| 提取视频帧 | ✅ | 使用 ffmpeg |
| 分析视频画面 | ❌ | 我是文字模型 |

## 工作流程

### Step 1: 获取视频信息

**策略 A — 搜索 API（首选）**
```bash
curl -s "https://api.tavily.com/search" \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "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",
    "query": "视频标题或关键词",
    "search_depth": "basic"
  }'
```

**策略 B — yt-dlp 下载**
```bash
# B站 / YouTube
yt-dlp "https://www.bilibili.com/video/BV1xxx" -o "video.mp4"

# 抖音（需登录 cookie，较复杂）
yt-dlp --cookies cookies.txt "抖音视频链接" -o "douyin.mp4"
```

### Step 2: 提取视频帧（如果下载成功）

```bash
# 提取关键帧
mkdir -p frames
ffmpeg -i video.mp4 -vf "select='eq(pict_type,I)',scale=640:-1" -vsync vfr frames/frame_%03d.jpg

# 或每隔 N 秒提取一帧
ffmpeg -i video.mp4 -vf "fps=1/5,scale=640:-1" frames/frame_%03d.jpg
```

### Step 3: 获取视频文案

**抖音视频文案提取（通过搜索）**
- 搜索博主名 + 视频关键词
- 从搜索结果中提取标题、描述

**B站视频信息**
```bash
# 通过 API 获取
curl -s "https://api.bilibili.com/x/web-interface/view?bvid=BV1xxx" | jq .
```

## 输出格式

```
🎬 视频分析报告

---

**基本信息**
- 标题：_______
- 作者：_______
- 平台：_______
- 时长：_______
- 播放量：_______

**文案内容**
[视频描述/字幕]

**关键帧**（如果提取成功）
- 帧1：[描述]
- 帧2：[描述]

**评论区热点**（如果可获取）
- 热评1
- 热评2

**内容分析**
[AI 分析]
```

## 注意事项

- 抖音、快手等平台有反爬机制，直接下载困难
- 建议优先通过搜索 API 获取文案信息
- B站、YouTube 相对开放，可用 yt-dlp 下载
- 下载的视频存放在 `~/.openclaw/workspace/videos/`
