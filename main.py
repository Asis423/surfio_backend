from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.music_controller import router as music_router
from controllers.auth_controller import router as auth_router

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed to restrict origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check route
@app.get("/")
async def health_check():
    """Check if the API is working."""
    return {"status": "API is working!"}

# Include the music-related routes
app.include_router(music_router, prefix="/music")
