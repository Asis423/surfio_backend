import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class SearchRecommender:
    def __init__(self, data_file):
        # Load data and initialize model (similar to the MusicRecommenderFromScratch class)
        self.data = pd.read_csv(data_file)
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.data['combined_textual_features'] = self.data.apply(
            lambda row: f"{row['Track Name']} {row['Artist Name(s)']} {row['Artist Genres']} {row['Album Name']}".lower(),
            axis=1
        )
        self.tfidf_matrix = self.vectorizer.fit_transform(self.data['combined_textual_features'])

        numerical_features = ['Danceability', 'Energy', 'Tempo', 'Valence', 'Loudness', 'Popularity']
        self.scaler = MinMaxScaler()
        self.numerical_matrix = self.scaler.fit_transform(self.data[numerical_features].fillna(0))

    def get_recommendations(self, query, top_n=15):
        """Implement the search-based recommendations using combined similarity metrics."""
        query = query.lower()
        query_vector = self.vectorizer.transform([query])

        # Calculate cosine similarity for textual and numerical features
        text_similarity = cosine_similarity(query_vector, self.tfidf_matrix)
        query_num = np.zeros((1, self.numerical_matrix.shape[1]))  # Default numerical query vector
        num_similarity = cosine_similarity(query_num, self.numerical_matrix)

        combined_similarity = 0.7 * text_similarity + 0.3 * num_similarity
        similarity_scores = list(enumerate(combined_similarity[0]))
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

        # Return top_n recommendations, similar to MusicRecommenderFromScratch
        recommendations = []
        seen_tracks = set()
        for idx, score in similarity_scores:
            track_name = str(self.data.iloc[idx]['Track Name'])
            if track_name not in seen_tracks:
                seen_tracks.add(track_name)
                recommendations.append({
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
            if len(recommendations) >= top_n:
                break

        return recommendations
