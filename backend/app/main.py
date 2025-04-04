from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import uvicorn
from dotenv import load_dotenv

# Import routers with error handling
# Initialize empty router variables
youtube = None
weather = None
ev_stations = None
image_gen = None
crypto = None
auth = None

# Try to import routers, but continue if some fail
try:
    from app.routers import youtube
except ImportError as e:
    print(f"Warning: YouTube router not loaded: {e}")

try:
    from app.routers import weather
except ImportError as e:
    print(f"Warning: Weather router not loaded: {e}")

try:
    from app.routers import ev_stations
except ImportError as e:
    print(f"Warning: EV Stations router not loaded: {e}")

try:
    from app.routers import image_gen
except ImportError as e:
    print(f"Warning: Image Generation router not loaded: {e}")

try:
    from app.routers import crypto
except ImportError as e:
    print(f"Warning: Crypto router not loaded: {e}")

try:
    from app.routers import auth
except ImportError as e:
    print(f"Warning: Authentication router not loaded: {e}")

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="OmniBot API",
    description="Backend API for OmniBot - The AI Swiss Army Knife",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers if available
if youtube and hasattr(youtube, 'router'):
    app.include_router(youtube.router, prefix="/api/youtube", tags=["YouTube"])
if weather and hasattr(weather, 'router'):
    app.include_router(weather.router, prefix="/api/weather", tags=["Weather"])
if ev_stations and hasattr(ev_stations, 'router'):
    app.include_router(ev_stations.router, prefix="/api/ev-stations", tags=["EV Stations"])
if image_gen and hasattr(image_gen, 'router'):
    app.include_router(image_gen.router, prefix="/api/images", tags=["Image Generation"])
if crypto and hasattr(crypto, 'router'):
    app.include_router(crypto.router, prefix="/api/crypto", tags=["Cryptocurrency"])
if auth and hasattr(auth, 'router'):
    app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])

# Serve static files (frontend)
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
app.mount("/css", StaticFiles(directory=os.path.join(static_dir, "css")), name="css")
app.mount("/js", StaticFiles(directory=os.path.join(static_dir, "js")), name="js")
app.mount("/public", StaticFiles(directory=os.path.join(static_dir, "public")), name="public")

@app.get("/", tags=["Root"])
async def serve_frontend():
    """Serve the frontend HTML."""
    return FileResponse(os.path.join(static_dir, "index.html"))

@app.get("/login", tags=["Authentication"])
async def serve_login():
    """Serve the login page."""
    return FileResponse(os.path.join(static_dir, "login.html"))

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "OmniBot API is running!"}

if __name__ == "__main__":
    # Run the app with uvicorn when this file is executed directly
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True) 