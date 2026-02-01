# InstaTrace  
**Private Instagram Post URL Extractor (Only Collab Posts)**

<p align="center">
  <img src="https://img.shields.io/badge/status-inconsistent-orange?style=for-the-badge&logo=instagram&logoColor=white&labelColor=000" alt="Status: Inconsistent">
  <img src="https://img.shields.io/badge/python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/for%20research%20only-important?style=for-the-badge&color=purple" alt="For research only">
</p>

**⚠️ IMPORTANT LEGAL & ETHICAL NOTICE**  
This tool demonstrates behavior related to collab posts.  


**Behavior is highly inconsistent**:
- Works on some private accounts with public collabs  
- Does **not** work on most other private accounts  
- May return nothing, partial data, or only public-visible content  

**Use exclusively for:**

- Educational purposes  
- Security research  
- Testing **your own** test accounts  
- Analyzing unexpected platform behavior  

**Never use this tool against accounts you do not own or have explicit written permission to test.**

## Observed Behavior (February 2026)

The tool sometimes still manages to retrieve direct image URLs from private accounts **when those accounts have collaborated posts** (joint posts / co-authored posts) with public accounts.

Possible explanations (unconfirmed):

- Residual caching or CDN exposure of collab-related assets  
- Different rendering paths for profiles with joint content  
- Instagram not applying the same strict privacy filter to collab metadata  
- Edge-case differences in how the web client embeds JSON for certain account states  

**Important:**  
This is **not** a confirmed active vulnerability.  
It is **inconsistent** and **unreliable**.  
Many private accounts (even with collabs) return **NOT VULNERABLE** or no private data.

## What the tool attempts to do

1. Fetch the profile page using mobile-emulating headers  
2. Search for embedded JSON blocks that may contain timeline data  
3. Extract image candidates (different resolutions) if found  
4. Save direct CDN URLs to `{username}_urls.txt`

## Features

- Clear verdict: **VULNERABLE** / **NOT VULNERABLE** / partial results  
- Saves found image URLs grouped by post with resolutions  
- Output file: `username_urls.txt`

## I'm not responsible for anything

## Requirements

Python 3.8 or newer

```bash
pip install -r requirements.txt
