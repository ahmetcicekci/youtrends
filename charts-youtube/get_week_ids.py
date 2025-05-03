from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime
import json
import os

# === Config ===
CHROMEDRIVER_PATH = "/opt/homebrew/bin/chromedriver"
BASE_URL = "https://charts.youtube.com/charts/TopSongs/{country}/weekly"
COUNTRIES = ["global", "US", "GB", "DE", "JP", "FR", "IN", "BR", "KR", "MX", "CA", "TR", "AU", "AR", "IT", "ES"]

def parse_week_string(week_str):
    """
    Converts a string like "Mar 18 – Mar 24, 2016" into "20160324"
    """
    try:
        week_str = week_str.strip().replace("–", "-")
        parts = week_str.split("-")
        end_date_raw = parts[1].strip()  # "Mar 24, 2016"
        end_date_obj = datetime.strptime(end_date_raw, "%b %d, %Y")
        return end_date_obj.strftime("%Y%m%d")
    except Exception as e:
        # print(f"Error: {e} | week_str: {week_str}")
        return None


# === Start browser ===
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # run in background
driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=options)

try:
    for country_code in COUNTRIES:
        url = BASE_URL.format(country=country_code)
        driver.get(url)

        wait = WebDriverWait(driver, 15)
        week_elements = wait.until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "paper-item"))
        )

        week_labels = [el.text for el in week_elements]

        week_ids = []
        for label in week_labels:
            week_id = parse_week_string(label)
            if week_id:
                week_ids.append(week_id)

        out_dir = os.path.join("countries", country_code)
        os.makedirs(out_dir, exist_ok=True)
        out_file = os.path.join(out_dir, "week_ids.json")
        with open(out_file, "w") as f:
            json.dump(week_ids, f, indent=2)

        print(f"{country_code}: {len(week_ids)} week IDs saved to {out_file}")


finally:
    driver.quit()
