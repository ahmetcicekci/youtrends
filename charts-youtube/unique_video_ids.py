import os
import json

BASE_DIR = "countries"
OUTPUT_FILE = "unique_video_ids.json"

unique_ids = set()

for country_code in os.listdir(BASE_DIR):
    country_path = os.path.join(BASE_DIR, country_code)
    video_ids_path = os.path.join(country_path, "video_ids")

    for filename in os.listdir(video_ids_path):
        if not filename.endswith(".json"):
            continue

        file_path = os.path.join(video_ids_path, filename)

        try:
            with open(file_path, "r") as f:
                ids = json.load(f)
                unique_ids.update(ids)
        except Exception as e:
            print(f"Error in {file_path}: {e}")

with open(OUTPUT_FILE, "w") as f:
    json.dump(list(unique_ids), f, indent=2)

print(f"\nDone. Found {len(unique_ids)} unique video IDs.")
print(f"Saved to {OUTPUT_FILE}")
