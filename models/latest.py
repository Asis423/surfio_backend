import pandas as pd

class LatestRecommender:
    def __init__(self, data_file):
        self.data = pd.read_csv(data_file)

    def get_latest_music(self, top_n=15):
        """Return the top N latest songs with detailed information."""
        # Sort the data by 'Album Release Date' in descending order
        latest_music = self.data.sort_values(by='Album Release Date', ascending=False).head(top_n)

        # Format the latest music data to include additional fields
        return [
            {
                'Track Name': str(row['Track Name']),
                'Track URL': str(row.get('Track URL', '')),  # Adjust based on available data
                'Artist Name(s)': str(row['Artist Name(s)']),
                'Album Name': str(row['Album Name']),
                'Album Release Date': str(row['Album Release Date']),
                'Album Image URL': str(row.get('Album Image URL', '')),
                'Popularity': int(row['Popularity']),
                'Danceability': float(row['Danceability']),
                'Energy': float(row['Energy']),
                'Valence': float(row['Valence']),
                'Tempo': float(row['Tempo']),
                'Track Duration (ms)': int(row['Track Duration (ms)']),
            }
            for _, row in latest_music.iterrows()
        ]
