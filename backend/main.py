from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import Base, engine
from backend.routes import pipeline_routes
from backend.csv_cleaner import routes as csv_routes


# --------------------------------------------------
# Create FastAPI application
# --------------------------------------------------

app = FastAPI(
    title="DataPulse API",
    description="Data Pipeline Management API",
    version="1.0.0"
)
app.include_router(
    csv_routes.router
)

# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://datapulse-phi.vercel.app",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
),


# --------------------------------------------------
# Create database tables
# --------------------------------------------------

Base.metadata.create_all(bind=engine)


# --------------------------------------------------
# Routes
# --------------------------------------------------

app.include_router(
    pipeline_routes.router,
    prefix="/pipelines",
    tags=["Pipelines"]
)


# --------------------------------------------------
# Root endpoint
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "DataPulse API is running",
        "status": "success"
    }