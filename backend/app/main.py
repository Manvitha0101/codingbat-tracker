from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routes import students, leaderboard
from app.jobs.scheduler import scheduler
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 1. Initialize FastAPI
app = FastAPI(
    title="Student Progress Tracker",
    description="Backend for monitoring CodingBat progress",
    version="1.0.0"
)

# 2. Add CORS Middleware (Crucial for React at port 3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Create Tables
Base.metadata.create_all(bind=engine)

# 4. Include Routers
app.include_router(students.router)
app.include_router(leaderboard.router)

@app.on_event("startup")
def start_scheduler():
    """Starts the scheduler and triggers the first scrape immediately"""
    if not scheduler.running:
        scheduler.start()
    
    # SAFELY trigger the job immediately
    job = scheduler.get_job('run_sync_scraper')
    if job:
        job.modify(next_run_time=datetime.now())
        logger.info("🚀 Scraper job triggered immediately on startup.")
    else:
        logger.warning("⚠️ Scraper job 'run_sync_scraper' not found in registry.")

@app.get("/")
def root():
    return {"message": "System is Online", "docs": "/docs"}