from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.music_controller import router as music_router
<<<<<<< HEAD
=======
from controllers.auth_controller import router as auth_router
>>>>>>> 7a52392 (backend updated)

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
<<<<<<< HEAD
=======

# Include the authentication-related routes
app.include_router(auth_router, prefix="/auth")
>>>>>>> 7a52392 (backend updated)
