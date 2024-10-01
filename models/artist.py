import pandas as pd

class ArtistRecommender:
    def __init__(self, data_file):
        self.data = pd.read_csv(data_file)

    def get_recommendations_by_artist(self, artist_name, top_n=10):
        return self.data[self.data['Artist Name(s)'].str.contains(artist_name, case=False)].head(top_n)
