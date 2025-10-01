import requests
import re
import csv

def get_tiktok_followers(url: str) -> int | None:
    """Scrape TT page and get follower count"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        html = response.text

        # look for "followerCount":12345 in the HTML/JSON blob
        match = re.search(r'"followerCount":(\d+)', html)
        if match:
            return int(match.group(1))
        else:
            return None
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


def process_txt(input_file: str, output_file: str):
    """read TT usernames from Follower.txt and write results with follower counts."""
    results = []

    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            if "Username:" not in line:
                continue
            username = line.strip().split("Username:")[-1].strip()
            if not username:
                continue
            url = f"https://www.tiktok.com/@{username}"
            followers = get_tiktok_followers(url)
            print(f"{url} → {followers}")
            results.append([url, followers])

    #  CSV writin
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["TikTok URL", "Followers"])
        writer.writerows(results)


if __name__ == "__main__":
    process_txt("Follower.txt", "output.csv")
