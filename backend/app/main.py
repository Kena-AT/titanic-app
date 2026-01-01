import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
# Going up two levels to reach the true project root (app -> backend -> root)
project_root = os.path.dirname(os.path.dirname(current_dir))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Also add the backend directory to sys.path to support 'import app' for unpickling
backend_dir = os.path.dirname(current_dir)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Fallback alias for unpickler
try:
    import app
except ImportError:
    pass

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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)

# Serve Frontend (Monolithic Middleware)
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# frontend/dist is sibling to app/
FRONTEND_DIST = os.path.join(project_root, "frontend/dist")

if os.path.exists(FRONTEND_DIST):
    assets_dir = os.path.join(FRONTEND_DIST, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")
    
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        file_path = os.path.join(FRONTEND_DIST, full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
             return FileResponse(file_path)
        
        # Otherwise serve index.html
        return FileResponse(os.path.join(FRONTEND_DIST, "index.html"))
else:
    print(f"Frontend build not found at {FRONTEND_DIST}. Running API only.")
