from fastapi import APIRouter, HTTPException, Query
from models.genre import GenreRecommender
from models.popular import PopularRecommender
from models.latest import LatestRecommender
from models.album import AlbumRecommender
from models.artist import ArtistRecommender
from models.recommend import SearchRecommender
from models.quick_picks import QuickPicks

# Initialize routers and recommender classes
router = APIRouter()

# Initialize recommender classes
genre_recommender = GenreRecommender(data_file="music_data.csv")
popular_recommender = PopularRecommender(data_file="music_data.csv")
latest_recommender = LatestRecommender(data_file="music_data.csv")
album_recommender = AlbumRecommender(data_file="music_data.csv")
artist_recommender = ArtistRecommender(data_file="music_data.csv")
search_recommender = SearchRecommender(data_file="music_data.csv")
quick_picks = QuickPicks(data_file="music_data.csv")  # Initialize MoodRecommender

@router.get("/recommend")
async def recommend(query: str = Query(...)):
    try:
        recommendations = search_recommender.get_recommendations(query)
        if not recommendations:
            raise HTTPException(status_code=404, detail="No matching song, artist, or genre found")
        return {"recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/popular")
async def get_popular_music():
    try:
        popular_music = popular_recommender.get_popular_music()
        return {"popular_music": popular_music}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/latest")
async def get_latest_music():
    try:
        latest_music = latest_recommender.get_latest_music()
        return {"latest_music": latest_music}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/genre")
async def recommend_by_genre(selected_genres: str = Query(...)):
    genres = [genre.strip().lower() for genre in selected_genres.split(',')]
    try:
        recommendations = genre_recommender.recommend_by_genre(genres)
        if not recommendations:
            raise HTTPException(status_code=404, detail="No matching songs found for the selected genres")
        return {"recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/album")
async def recommend_by_album(album_name: str = Query(...)):
    try:
        recommendations = album_recommender.get_recommendations_by_album(album_name)
        if not recommendations:
            raise HTTPException(status_code=404, detail="No matching album found")
        return {"recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/artist")
async def recommend_by_artist(artist_name: str = Query(...)):
    try:
        recommendations = artist_recommender.get_recommendations_by_artist(artist_name)
        if not recommendations:
            raise HTTPException(status_code=404, detail="No matching artist found")
        return {"recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/quick_picks")
async def quick_picks():
    try:
        quick_picks_recommender = QuickPicks(data_file="music_data.csv")
        print("QuickPicks instance created.")
        recommendations = quick_picks_recommender.get_quick_picks()
        print("Recommendations retrieved.")
        return {"quick_picks": recommendations}
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
