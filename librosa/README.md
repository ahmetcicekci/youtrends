This stage runs on **Amazon EMR**, leveraging **PySpark** for distributed processing and **Librosa** for audio analysis. The goal is to extract meaningful features from MP3 files stored in S3 and write them into a single Parquet file for downstream tasks such as similarity analysis or recommendation systems.

**Extracted Audio Features:**
- `tempo`: Estimated beats per minute (BPM), representing the speed of the track.
- `zcr_mean` (Zero-Crossing Rate): Measures how frequently the audio waveform crosses the zero axis — often associated with noisiness or sharpness.
- `spectral_centroid_mean`: Indicates where the "center of mass" of the frequency spectrum is located. Higher values suggest brighter sounds.
- `spectral_bandwidth_mean`: Measures the spread of the spectrum around its centroid. Related to timbral complexity.
- `spectral_rolloff_mean`: The frequency below which a specified percentage (usually 85%) of the total spectral energy lies. It helps detect the high-frequency content.
- `rms_mean` (Root Mean Square Energy): Represents the average power or loudness of the signal.
- `spectral_flatness_mean`: Indicates how noise-like a sound is. Higher flatness means the spectrum is flatter (more like white noise).
- `mfcc_mean`: (Mel-frequency cepstral coefficients): 13 coefficients summarizing the timbral texture of the audio — commonly used in speech and music classification.