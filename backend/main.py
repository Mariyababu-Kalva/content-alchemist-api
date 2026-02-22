from fastapi import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import summarize
from backend.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.version
)

# This forces all incoming HTTP requests to redirect to HTTPS automatically
app.add_middleware(HTTPSRedirectMiddleware)

# Configure CORS so Streamlit app can still talk to the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace "*" with specific UI domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(summarize.router)

@app.get('/')
def read_root():
    return {
        "status": "online",
        "app_name": settings.app_name,
        "version": settings.version
    }