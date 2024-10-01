import pandas as pd

class AlbumRecommender:
    def __init__(self, data_file):
        self.data = pd.read_csv(data_file)

    def get_recommendations_by_album(self, album_name, top_n=10):
        return self.data[self.data['Album Name'].str.contains(album_name, case=False)].head(top_n)
