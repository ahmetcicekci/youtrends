import logging
import os
import tempfile

import boto3
import librosa
import numpy as np
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import ArrayType, FloatType, StringType, StructField, StructType

logging.basicConfig(level=logging.INFO)


def extract_features_with_librosa(s3_path: str):
    try:
        parts = s3_path.replace("s3a://", "").split("/", 1)
        bucket = parts[0]
        key = parts[1]

        video_id = key.split("/")[-1].replace(".mp3", "")

        s3 = boto3.client("s3")
        with tempfile.NamedTemporaryFile(suffix=".mp3") as tmp:
            s3.download_fileobj(bucket, key, tmp)
            tmp.seek(0)
            y, sr = librosa.load(tmp.name)

            # Basic features
            tempo = float(librosa.feature.tempo(y=y, sr=sr)[0])
            zcr = float(np.mean(librosa.feature.zero_crossing_rate(y)))
            centroid = float(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)))
            bandwidth = float(np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr)))
            rolloff = float(np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr)))
            rms = float(np.mean(librosa.feature.rms(y=y)))
            flatness = float(np.mean(librosa.feature.spectral_flatness(y=y)))

            # MFCCs (13)
            mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
            mfcc_mean = [float(np.mean(x)) for x in mfcc]

            return video_id, tempo, zcr, centroid, bandwidth, rolloff, rms, flatness, mfcc_mean
    except Exception as e:
        print(f"Error processing {s3_path}: {e}")
        return None


schema = StructType(
    [
        StructField("video_id", StringType(), True),
        StructField("tempo", FloatType(), True),
        StructField("zcr_mean", FloatType(), True),
        StructField("spectral_centroid_mean", FloatType(), True),
        StructField("spectral_bandwidth_mean", FloatType(), True),
        StructField("spectral_rolloff_mean", FloatType(), True),
        StructField("rms_mean", FloatType(), True),
        StructField("spectral_flatness_mean", FloatType(), True),
        StructField("mfcc_mean", ArrayType(FloatType()), True),
    ]
)


spark = (
    SparkSession.builder.appName("MP3_Tempo_Extraction")
    .master("local[*]")
    .config(
        "spark.hadoop.fs.s3a.aws.credentials.provider",
        "com.amazonaws.auth.DefaultAWSCredentialsProviderChain",
    )
    .getOrCreate()
)

df = (
    spark.read.format("binaryFile")
    .option("pathGlobFilter", "*.mp3")
    .load("s3a://youtrends-project/music-data/audio/")
    .select("path")
)  # path only

features_udf = udf(extract_features_with_librosa, schema)
result_df = df.withColumn("features", features_udf(df["path"])).select("features.*")

result_df.coalesce(1).write.mode("overwrite").parquet(
    "s3a://youtrends-project/music-data/audio-features/"
)
