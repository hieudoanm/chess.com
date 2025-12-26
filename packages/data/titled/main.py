import requests
from pathlib import Path
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import pandas as pd

# from tqdm.notebook import tqdm

TITLES: list[str] = ["GM", "IM", "FM", "CM", "NM", "WGM", "WIM", "WFM", "WCM", "WNM"]
USER_AGENT = "ArithmeticErrorMozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:127.0) Gecko/20100101 Firefox/127.0"

titled_players: list[dict] = []
for title in TITLES:
    url = f"https://api.chess.com/pub/titled/{title}"
    response = requests.get(url, headers={"User-Agent": USER_AGENT})
    data: dict = response.json()
    usernames: list[str] = data.get("players", [])
    json_file_path = f"./json/titles/{title}.json"
    json_file = open(json_file_path, "w")
    json.dump(usernames, json_file, indent=2)


usernames = []
titles_dir = Path("./json/titles")

for title in TITLES:
    json_file_path = titles_dir / f"{title}.json"

    try:
        # Skip missing files
        if not json_file_path.exists():
            print(f"⚠️ File not found: {json_file_path}")
            continue

        # Skip empty files
        if json_file_path.stat().st_size == 0:
            print(f"⚠️ Empty file skipped: {json_file_path}")
            continue

        # Load JSON safely
        with open(json_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                usernames.extend(data)
            else:
                print(f"⚠️ Non-list JSON skipped: {json_file_path}")

    except json.JSONDecodeError:
        print(f"❌ Invalid JSON in file: {json_file_path}")
        continue

# Write merged JSON
output_path = titles_dir / "all.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(usernames, f, indent=2, ensure_ascii=False)

print("✅ Done! Merged usernames written to all.json")


USER_AGENT = "ArithmeticErrorMozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:127.0) Gecko/20100101 Firefox/127.0"
json_file_path = "./json/titles/all.json"
json_file = open(json_file_path, "r")
usernames: list[str] = json.load(json_file)
usernames.reverse()


def get_player(username: str):
    player_url = f"https://api.chess.com/pub/player/{username}"
    player_stats_url = f"https://api.chess.com/pub/player/{username}/stats"
    player_response = requests.get(player_url, headers={"User-Agent": USER_AGENT})
    player: dict = player_response.json()
    player_stats_response = requests.get(
        player_stats_url, headers={"User-Agent": USER_AGENT}
    )
    player_stats: dict = player_stats_response.json()
    player_id = player.get("player_id", 0)
    player_json_file_path = f"./json/players/{player_id}.json"
    player_json_file = open(player_json_file_path, "w")
    json.dump({**player, **player_stats}, player_json_file, indent=2)


if __name__ == "__main__":
    cpu_cores: int = os.cpu_count()
    max_workers: int = cpu_cores * 2
    print(cpu_cores, max_workers)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(get_player, username): username for username in usernames
        }

        # Use tqdm to display a progress bar
        for future in as_completed(futures):
            future.result()


folder_path = "./json/players"
data_frames = []

for file_name in os.listdir(folder_path):
    if file_name.endswith(".json"):
        json_file_path = os.path.join(folder_path, file_name)
        json_file = open(json_file_path, "r")
        data = json.load(json_file)
        df = pd.json_normalize(data)
        data_frames.append(df)

combined_df = pd.concat(data_frames, ignore_index=True)
combined_df.to_csv("./csv/players.csv", index=False)
