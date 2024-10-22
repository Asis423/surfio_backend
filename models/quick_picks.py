import pandas as pd
import random
from fastapi import HTTPException

class QuickPicks:
    def __init__(self, data_file: str):
<<<<<<< HEAD
        self.data = pd.read_csv(data_file)
=======
        self.data = pd.read_csv( data_file)
>>>>>>> 7a52392 (backend updated)
        
        # Predefined mood strings
        self.moods = [
            "happy",
            "sad",
            "energetic",
            "relaxed",
            "romantic",
            "party",
            "chill",
            "motivational"
        ]

    def get_random_mood(self):
        return random.choice(self.moods)

    def recommend_based_on_mood(self, mood):
        # Define mood thresholds for various attributes
        mood_thresholds = {
            "happy": (0.7, 0.8, 0.6),       # Danceability, Energy, Valence
            "sad": (0.3, 0.2, 0.4),         # Low Danceability, Low Energy, Low Valence
            "energetic": (0.8, 0.9, 0.7),   # High Danceability, High Energy, High Valence
            "relaxed": (0.4, 0.5, 0.5),     # Moderate Danceability, Moderate Energy, Moderate Valence
            "romantic": (0.6, 0.5, 0.8),    # Moderate Danceability, Moderate Energy, High Valence
            "party": (0.8, 0.9, 0.6),       # High Danceability, High Energy, Moderate Valence
            "chill": (0.5, 0.4, 0.3),       # Moderate Danceability, Low Energy, Low Valence
            "motivational": (0.6, 0.7, 0.7), # Moderate Danceability, High Energy, High Valence
        }
        
        danceability_threshold, energy_threshold, valence_threshold = mood_thresholds.get(mood, (0.5, 0.5, 0.5))

        filtered_songs = self.data[
            (self.data['Danceability'] >= danceability_threshold) &
            (self.data['Energy'] >= energy_threshold) &
            (self.data['Valence'] >= valence_threshold)  # Use Valence to filter songs
        ]

        # Randomly sample songs from the filtered DataFrame
        if not filtered_songs.empty:
            n_recommendations = min(10, len(filtered_songs))  # Ensure we don't sample more than available songs
            recommendations = filtered_songs.sample(n=n_recommendations).to_dict(orient='records')
            return [
                {
                    'Track Name': str(row['Track Name']),
                    'Track URL': str(row.get('Track URL', '')),
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
                for row in recommendations
            ]
        else:
            raise HTTPException(status_code=404, detail="No songs found for the current mood.")
    
    def get_quick_picks(self):
        # Get a random mood
        random_mood = self.get_random_mood()
        # Get recommendations based on the random mood
        return self.recommend_based_on_mood(random_mood)