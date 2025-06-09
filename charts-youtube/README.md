In the initial phase of the project, we needed a large and diverse set of YouTube video IDs corresponding to songs. However, collecting these IDs from artist channels or playlists didn’t provide enough variety or quantity. These sources often focused on a specific language, genre, or region, and typically contained a limited number of items — failing to represent global trends at scale.

To overcome this problem, we leveraged [charts.youtube.com](https://charts.youtube.com/charts/TopSongs/global/weekly), which offers weekly rankings of the top 100 most streamed songs. These charts are available both globally and for individual countries, making them a rich and diverse source of popular music across different cultures and languages. We extracted the video IDs from these pages using **Selenium**, as the content is dynamically rendered and not available through static HTML.

The [`get_week_ids.py`](get_week_ids.py) script fetches the list of available week IDs for both the global chart and [15 selected country](get_week_ids.py#L14) charts. Since the number of historical weeks varies across regions, this step ensures that we dynamically retrieve all accessible time ranges for each region.

Then, the [`get_video_ids.py`](get_video_ids.py) script iterates through all country-level and global chart URLs using the previously collected week IDs. It extracts the top 100 songs from each chart page and saves the video IDs into JSON files.

Finally, the [`unique_video_ids.py`](unique_video_ids.py) script reads all collected JSON files and extracts a unique list of video IDs, as many songs appear across multiple weeks and countries.

In total, approximately 50,000 unique video IDs were collected from global and local charts across 15 countries.