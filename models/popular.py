import pandas as pd

class PopularRecommender:
    def __init__(self, data_file):
        self.data = pd.read_csv(data_file)

    def get_popular_music(self, top_n=15):
        """Return the top N most popular songs with detailed information."""
        popular_music = self.data.nlargest(top_n, 'Popularity')

        # Format the popular music data to include additional fields
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
            for _, row in popular_music.iterrows()
        ]
