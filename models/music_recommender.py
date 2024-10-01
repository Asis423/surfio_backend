import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class MusicRecommenderFromScratch:
    def __init__(self, data_file):
        # Load the CSV dataset and preprocess it during startup
        self.data = pd.read_csv(data_file)

        # Combine relevant textual features: song title, artist name(s), genres, album name
        self.data['combined_textual_features'] = self.data.apply(
            lambda row: f"{row['Track Name']} {row['Artist Name(s)']} {row['Artist Genres']} {row['Album Name']}".lower(),
            axis=1
        )

        # Precompute the TF-IDF vectors and normalize numerical features for all songs
        self.precompute_vectors()

    def precompute_vectors(self):
        """Precompute TF-IDF vectors for textual features and scale numerical features."""
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.vectorizer.fit_transform(self.data['combined_textual_features'])

        numerical_features = ['Danceability', 'Energy', 'Tempo', 'Valence', 'Loudness', 'Popularity']
        scaler = MinMaxScaler()
        self.numerical_matrix = scaler.fit_transform(self.data[numerical_features].fillna(0))

    def get_recommendations(self, query, top_n=15):
        """Find song recommendations based on cosine similarity of both textual and numerical features."""
        query = query.lower()
        query_vector = self.vectorizer.transform([query])

        text_similarity = cosine_similarity(query_vector, self.tfidf_matrix)
        query_num = np.zeros((1, self.numerical_matrix.shape[1]))
        num_similarity = cosine_similarity(query_num, self.numerical_matrix)

        combined_similarity = 0.7 * text_similarity + 0.3 * num_similarity
        similarity_scores = list(enumerate(combined_similarity[0]))
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

        # Filter out duplicates
        seen_tracks = set()
        top_recommendations = []
        for idx, score in similarity_scores:
            track_name = str(self.data.iloc[idx]['Track Name'])
            if track_name not in seen_tracks:
                seen_tracks.add(track_name)
                top_recommendations.append({
                    'Track Name': track_name,
                    'Track URL': str(self.data.iloc[idx]['Track URL']),
                    'Artist Name(s)': str(self.data.iloc[idx]['Artist Name(s)']),
                    'Album Name': str(self.data.iloc[idx]['Album Name']),
                    'Album Release Date': str(self.data.iloc[idx]['Album Release Date']),
                    'Album Image URL': str(self.data.iloc[idx]['Album Image URL']),
                    'Popularity': int(self.data.iloc[idx]['Popularity']),
                    'Danceability': float(self.data.iloc[idx]['Danceability']),
                    'Energy': float(self.data.iloc[idx]['Energy']),
                    'Valence': float(self.data.iloc[idx]['Valence']),
                    'Tempo': float(self.data.iloc[idx]['Tempo']),
                    'Track Duration (ms)': int(self.data.iloc[idx]['Track Duration (ms)']),
                })
            if len(top_recommendations) >= top_n:
                break

        return top_recommendations

    def get_popular_music(self, top_n=10):
        """Get the top N most popular music tracks."""
        popular_music = self.data.nlargest(top_n, 'Popularity')
        return self._format_music_list(popular_music)

    def get_latest_music(self, top_n=10):
        """Get the top N latest music tracks based on album release date."""
        latest_music = self.data.sort_values(by='Album Release Date', ascending=False).head(top_n)
        return self._format_music_list(latest_music)

    def get_recommendations_by_genre(self, selected_genres, top_n=15):
        """Recommend songs based on selected genres, prioritizing popular songs."""
        selected_genres = [genre.lower() for genre in selected_genres]
        filtered_data = self.data[self.data['Artist Genres'].str.lower().str.contains('|'.join(selected_genres), na=False)]

        if filtered_data.empty:
            return []

        filtered_data['combined_textual_features'] = filtered_data.apply(
            lambda row: f"{row['Track Name']} {row['Artist Name(s)']} {row['Artist Genres']} {row['Album Name']}".lower(),
            axis=1
        )
        
        tfidf_matrix = self.vectorizer.transform(filtered_data['combined_textual_features'])
        cosine_similarity_scores = cosine_similarity(tfidf_matrix)

        popularity_scores = filtered_data['Popularity'].values
        normalized_popularity = (popularity_scores - popularity_scores.min()) / (popularity_scores.max() - popularity_scores.min())
        combined_scores = 0.7 * cosine_similarity_scores + 0.3 * normalized_popularity.reshape(-1, 1)

        similarity_scores = list(enumerate(combined_scores[0]))
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

        # Filter out duplicates
        seen_tracks = set()
        top_recommendations = []
        for idx, score in similarity_scores:
            track_name = str(filtered_data.iloc[idx]['Track Name'])
            if track_name not in seen_tracks:
                seen_tracks.add(track_name)
                top_recommendations.append({
                    'Track Name': track_name,
                    'Track URL': str(self.data.iloc[idx]['Track URL']),
                    'Artist Name(s)': str(filtered_data.iloc[idx]['Artist Name(s)']),
                    'Album Name': str(filtered_data.iloc[idx]['Album Name']),
                    'Album Release Date': str(filtered_data.iloc[idx]['Album Release Date']),
                    'Album Image URL': str(filtered_data.iloc[idx]['Album Image URL']),
                    'Popularity': int(filtered_data.iloc[idx]['Popularity']),
                    'Danceability': float(filtered_data.iloc[idx]['Danceability']),
                    'Energy': float(filtered_data.iloc[idx]['Energy']),
                    'Valence': float(filtered_data.iloc[idx]['Valence']),
                    'Tempo': float(filtered_data.iloc[idx]['Tempo']),
                    'Track Duration (ms)': int(self.data.iloc[idx]['Track Duration (ms)']),
                })
            if len(top_recommendations) >= top_n:
                break

        return top_recommendations

    def _format_music_list(self, music_list):
        """Helper function to format music list for popular and latest music."""
        return [
            {
                'Track Name': str(row['Track Name']),
                'Track URL': str(self.data.iloc[idx]['Track URL']),
                'Artist Name(s)': str(row['Artist Name(s)']),
                'Album Name': str(row['Album Name']),
                'Album Release Date': str(row['Album Release Date']),
                'Album Image URL': str(row['Album Image URL']),
                'Popularity': int(row['Popularity']),
                'Track Duration (ms)': int(self.data.iloc[idx]['Track Duration (ms)']),
            }
            for _, row in music_list.iterrows()
        ]
