import os
import time
import json
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from typing import Optional

# Try to import routers with fallbacks
try:
    from app.routers import youtube
except ImportError:
    youtube = None

try:
    from app.routers import weather
except ImportError:
    weather = None

try:
    from app.routers import ev_stations
except ImportError:
    ev_stations = None

try:
    from app.routers import image_gen
except ImportError:
    image_gen = None

try:
    from app.routers import crypto
except ImportError:
    crypto = None
    
try:
    from app.routers import auth
except ImportError:
    auth = None

# Load environment variables from .env file
load_dotenv()

# Initialize the FastAPI app
app = FastAPI(title="OmniBot API", description="An API for OmniBot, a versatile chatbot that integrates multiple services.", version="1.0.0")

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the base directory to serve static files from
BASE_DIR = Path(__file__).resolve().parent.parent.parent
STATIC_DIR = BASE_DIR

# Mount static files
app.mount("/css", StaticFiles(directory=os.path.join(STATIC_DIR, "css")), name="css")
app.mount("/js", StaticFiles(directory=os.path.join(STATIC_DIR, "js")), name="js")
app.mount("/public", StaticFiles(directory=os.path.join(STATIC_DIR, "public")), name="public")

# Import and include routers
if youtube:
    app.include_router(youtube.router, prefix="/api/youtube", tags=["YouTube"])

if weather:
    app.include_router(weather.router, prefix="/api/weather", tags=["Weather"])

if ev_stations:
    app.include_router(ev_stations.router, prefix="/api/ev", tags=["EV Stations"])

if image_gen:
    app.include_router(image_gen.router, prefix="/api/image", tags=["Image Generation"])

if crypto:
    app.include_router(crypto.router, prefix="/api/crypto", tags=["Cryptocurrency"])
    
if auth:
    app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])

# Add health check endpoint
@app.get("/api/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "timestamp": time.time()}

# Serve index.html at the root
@app.get("/", tags=["Frontend"], response_class=HTMLResponse)
async def serve_homepage():
    try:
        html_file = os.path.join(STATIC_DIR, "index.html")
        with open(html_file, "r") as f:
            content = f.read()
        return HTMLResponse(content=content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to serve homepage: {str(e)}")

# Serve login.html
@app.get("/login", tags=["Authentication"], response_class=HTMLResponse)
async def serve_login_page():
    try:
        html_file = os.path.join(STATIC_DIR, "login.html")
        with open(html_file, "r") as f:
            content = f.read()
        return HTMLResponse(content=content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to serve login page: {str(e)}")

# Vercel serverless handler
@app.get("/{path:path}", include_in_schema=False)
async def catch_all(path: str, request: Request):
    # Try to serve static files
    file_path = os.path.join(STATIC_DIR, path)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(file_path)
        
    # Default to index.html for client-side routing
    html_file = os.path.join(STATIC_DIR, "index.html")
    with open(html_file, "r") as f:
        content = f.read()
    return HTMLResponse(content=content)

# Handler for Vercel serverless functions
handler = app 