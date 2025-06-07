This repository contains the audio pipeline developed as part of the term project for the course **BVA504E - Big Data Technologies and Applications**, offered within the **ITU Big Data & Business Analytics Master's Program**.

The overall objective of the project is to analyze trending YouTube music data and extract meaningful insights through large-scale processing. This includes collecting song metadata, audio content, and applying various analytical techniques such as similarity analysis and recommendation.

This component specifically implements the **audio ingestion and feature extraction layer** of the project. It covers: 
- the retrieval of trending video IDs ([`charts-youtube/`](charts-youtube/))
- downloading corresponding MP3 audio files and uploading them to cloud storage Amazon S3 ([`yt-dlp/`](yt-dlp/))
- extracting relevant audio features using **Librosa** and distributed processing via **Apache Spark** ([`librosa/`](librosa/))

The resulting features will be used in downstream analysis and modeling stages.

