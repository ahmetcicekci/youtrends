from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
import json
from urllib.parse import urlparse, parse_qs

# === Config ===
CHROMEDRIVER_PATH = "/opt/homebrew/bin/chromedriver"
BASE_URL = "https://charts.youtube.com/charts/TopSongs/{country}/weekly/"
COUNTRIES = ["global", "US", "GB", "DE", "JP", "FR", "IN", "BR", "KR", "MX", "CA", "TR", "AU", "AR", "IT", "ES"]

# === Start browser ===
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # run in background
driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=options)

try:
    for country_code in COUNTRIES:
        print(f"\nProcessing country: {country_code}")

        base_path = os.path.join("countries", country_code)
        week_ids_path = os.path.join(base_path, "week_ids.json")
        output_dir = os.path.join(base_path, "video_ids")
        os.makedirs(output_dir, exist_ok=True)

        with open(week_ids_path, "r") as f:
            week_ids = json.load(f)

        for week_id in week_ids:
            output_path = os.path.join(output_dir, f"{week_id}.json")
            if os.path.exists(output_path):
                print(f"Skipping existing: {country_code} {week_id}")
                continue

            print(f"Fetching: {country_code} {week_id} ...")

            week_url = BASE_URL.format(country=country_code) + week_id
            driver.get(week_url)

            try:
                wait = WebDriverWait(driver, 15)
                song_rows = wait.until(
                    EC.presence_of_all_elements_located((By.TAG_NAME, "ytmc-entry-row"))
                )
            except Exception as e:
                print(f"Failed to load song rows for: {country_code} {week_id} | {e}")
                continue

            video_ids = []

            for row in song_rows:
                try:
                    shadow_root = driver.execute_script(
                        "return arguments[0].shadowRoot", row
                    )
                    entity_title = shadow_root.find_element(By.ID, "entity-title")
                    endpoint_data = entity_title.get_attribute("endpoint")
                    youtube_url = (
                        json.loads(endpoint_data).get("urlEndpoint", {}).get("url")
                    )
                    parsed_url = urlparse(youtube_url)
                    video_id = parse_qs(parsed_url.query).get("v", [None])[0]

                    if video_id:
                        video_ids.append(video_id)

                except Exception as e:
                    print(f"Error while parsing a song row: {e}")

            with open(output_path, "w") as f:
                json.dump(video_ids, f, indent=2)

            print(f"Saved {len(video_ids)} video IDs to {output_path}")

finally:
    driver.quit()
