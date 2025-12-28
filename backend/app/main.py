from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router

app = FastAPI(
    title="Titanic Survival Prediction API",
    description="Predict if a passenger survived the Titanic",
    version="1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, allow all. In prod, specify frontend domain.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)

# Serve Frontend (Monolithic Middleware)
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Adjust paths based on where main.py is run
# Assuming running from root or backend/
# We need to find 'frontend/dist'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIST = os.path.join(BASE_DIR, "../../frontend/dist")

if os.path.exists(FRONTEND_DIST):
    # Serve assets (JS/CSS)
    # Vite usually puts them in 'assets/'
    assets_dir = os.path.join(FRONTEND_DIST, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    # Serve other static files (favicon, etc) if needed, or just root
    # app.mount("/", StaticFiles(directory=FRONTEND_DIST, html=True), name="static") 
    # BUT, for SPA, we usually want to serve index.html for unknown routes
    
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        # Allow API routes to pass through (handled above by router)
        # If it's a file that exists, serve it
        file_path = os.path.join(FRONTEND_DIST, full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
             return FileResponse(file_path)
        
        # Otherwise serve index.html
        return FileResponse(os.path.join(FRONTEND_DIST, "index.html"))
else:
    print(f"Frontend build not found at {FRONTEND_DIST}. Running API only.")
