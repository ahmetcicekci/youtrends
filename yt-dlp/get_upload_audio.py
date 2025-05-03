import json
import os
import boto3
from yt_dlp import YoutubeDL

# === Config ===
INPUT_JSON = "../charts-youtube/unique_video_ids.json"
OUTPUT_DIR = "music-data/audio/"
S3_BUCKET = "youtrends-project"
S3_PREFIX = "music-data/audio/"

# === AWS Setup ===
s3 = boto3.client("s3")


def get_existing_video_ids(bucket, prefix):
    """Fetch existing video IDs from S3"""
    paginator = s3.get_paginator("list_objects_v2")
    existing_ids = set()

    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get("Contents", []):
            key = obj["Key"]
            if key.endswith(".mp3"):
                video_id = os.path.splitext(os.path.basename(key))[0]
                existing_ids.add(video_id)

    return existing_ids


def upload_to_s3(local_file, s3_key):
    """Upload local file to S3"""
    s3.upload_file(local_file, S3_BUCKET, s3_key)
    print(f"Uploaded to: s3://{S3_BUCKET}/{s3_key}")


def download_audio(video_id):
    """Download audio as MP3 using yt-dlp"""
    video_url = f"https://www.youtube.com/watch?v={video_id}"

    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "outtmpl": video_id, # will be saved as {video_id}.mp3
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "320",
            }
        ],
        # "sleep_interval_requests": 1,
        # "max_sleep_interval_requests": 3,
        # "retries": 10,
        # "fragment_retries": 5,
        # "concurrent_fragment_downloads": 1,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        print(f"Downloaded: {video_id}")
        return True
    except Exception as e:
        print(f"Failed: {video_id} — {e}")
        return False


def main():
    with open(INPUT_JSON, "r") as f:
        video_ids = json.load(f)

    existing_ids = get_existing_video_ids(S3_BUCKET, S3_PREFIX)
    print(f"Found {len(existing_ids)} files already in S3.")

    remaining_ids = [vid for vid in video_ids if vid not in existing_ids]
    print(f"{len(remaining_ids)} videos to download.")

    for video_id in remaining_ids:
        local_file = f"{video_id}.mp3"
        s3_key = f"{S3_PREFIX}{video_id}.mp3"

        if download_audio(video_id):
            if os.path.exists(local_file):
                upload_to_s3(local_file, s3_key)
                os.remove(local_file)
                print(f"🧹 Deleted local file: {local_file}")

    print("All tasks completed.")


if __name__ == "__main__":
    main()
