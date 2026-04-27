#!/usr/bin/env python3
"""Headless browser fetcher using Playwright"""

import asyncio
import sys
from playwright.async_api import async_playwright

async def fetch(url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, wait_until='networkidle')
        content = await page.content()
        title = await page.title()
        await browser.close()
        return title, content

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python browser_fetch.py <url>")
        sys.exit(1)
    
    url = sys.argv[1]
    title, content = asyncio.run(fetch(url))
    print(f"Title: {title}")
    print(f"Content length: {len(content)}")
    print(content[:5000])
