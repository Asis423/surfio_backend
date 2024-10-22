import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class GenreRecommender:
    def __init__(self, data_file):
        self.data = pd.read_csv(data_file)
        self.vectorizer = TfidfVectorizer(stop_words='english')

    def recommend_by_genre(self, selected_genres, top_n=15):
        selected_genres = [genre.lower() for genre in selected_genres]
        filtered_data = self.data[self.data['Artist Genres'].str.lower().str.contains('|'.join(selected_genres), na=False)]
        if filtered_data.empty:
            return []

        tfidf_matrix = self.vectorizer.fit_transform(filtered_data['Track Name'])
        cosine_similarity_scores = cosine_similarity(tfidf_matrix)

        popularity_scores = filtered_data['Popularity'].values
        combined_scores = 0.7 * cosine_similarity_scores + 0.3 * popularity_scores.reshape(-1, 1)

        return self._get_recommendations(filtered_data, combined_scores, top_n)

    def _get_recommendations(self, data, scores, top_n):
        return [
            {
                'Track Name': row['Track Name'],
                'Artist Name(s)': row['Artist Name(s)'],
                'Album Name': row['Album Name'],
                'Popularity': row['Popularity']
            }
<<<<<<< HEAD
            for row in data.nlargest(top_n, 'Popularity').itertuples()
        ]
=======
            for _, row in data.nlargest(top_n, 'Popularity').iterrows()
        ]

>>>>>>> 7a52392 (backend updated)
