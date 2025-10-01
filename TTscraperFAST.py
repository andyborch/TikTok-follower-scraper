import requests
import re
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_tiktok_followers(url: str) -> tuple[str, int | None]:
    """Scrape TikTok profile page and extract follower count."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        html = response.text

        # Look for "followerCount":12345
        match = re.search(r'"followerCount":(\d+)', html)
        followers = int(match.group(1)) if match else None
        return url, followers
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return url, None


def process_txt(input_file: str, output_file: str, max_workers: int = 10):
    urls = []

    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            if "Username:" not in line:
                continue
            username = line.strip().split("Username:")[-1].strip()
            if not username:
                continue
            url = f"https://www.tiktok.com/@{username}"
            urls.append(url)

    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(get_tiktok_followers, url): url for url in urls}
        for future in as_completed(future_to_url):
            url, followers = future.result()
            print(f"{url} → {followers}")
            results.append([url, followers])

    #CSV writin
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["TikTok URL", "Followers"])
        writer.writerows(results)


if __name__ == "__main__":
    process_txt("Follower.txt", "output.csv", max_workers=20)
