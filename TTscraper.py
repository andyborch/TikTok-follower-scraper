import requests
import re
import csv

def get_tiktok_followers(url: str) -> int | None:
    """scrape TT profile and extract the follower count."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        html = response.text

        # Look for "followerCount":12345 in the HTML/JSON blob
        match = re.search(r'"followerCount":(\d+)', html)
        if match:
            return int(match.group(1))
        else:
            return None
    except Exception as e:
        print(f"error {url}: {e}")
        return None


def process_csv(input_file: str, output_file: str):
    #Read profile URLs from input CSV and write results with follower counts
    results = []

    with open(input_file, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            url = row[0].strip()
            followers = get_tiktok_followers(url)
            print(f"{url} → {followers}")
            results.append([url, followers])

    # write results to CSV
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["TikTok URL", "Followers"])
        writer.writerows(results)


if __name__ == "__main__":
    process_csv("input.csv", "output.csv")
