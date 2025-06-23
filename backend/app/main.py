from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .core.database import init_db

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Admin Panel API for Logbiz HR Recruitment"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    print("🚀 Starting Logbiz Admin Panel API...")
    init_db()
    print("✅ Database initialized")

@app.get("/")
async def root():
    return {
        "message": "Welcome to Logbiz Admin Panel API",
        "version": settings.VERSION,
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 