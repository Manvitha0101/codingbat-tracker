import asyncio
from apscheduler.schedulers.background import BackgroundScheduler
from app.database import SessionLocal
from app.models import Student, ProgressSnapshot
from app.services.scraper import scrape_codingbat_profile

def run_sync_scraper():
    """Wrapper to run the async scraper and SAVE data to PostgreSQL"""
    db = SessionLocal()
    try:
        # 1. Get all students from the database
        students = db.query(Student).all()
        print(f"🔄 Starting background scrape for {len(students)} students...")
        
        # Create a temporary event loop for the background thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        for student in students:
            # 2. Get the new count from CodingBat
            result = loop.run_until_complete(scrape_codingbat_profile(student.codingbat_url))
            
            if result and result["success"]:
                new_count = result["solved_count"]
                
                # 3. UPDATE the Student record explicitly
                student.total_solved = new_count
                db.add(student) # Tells SQLAlchemy to 'watch' this change
                
                # 4. Add the historical snapshot
                new_snapshot = ProgressSnapshot(
                    student_id=student.id,
                    solved_count=new_count
                )
                db.add(new_snapshot)
                
                # This print helps you see it working in the terminal
                print(f"📊 DEBUG: {student.name} -> Solved: {new_count}")

        # 5. COMMIT ALL CHANGES (This is the most important line)
        db.commit()
        print("✅ DATABASE UPDATED: All student records synced successfully.")

    except Exception as e:
        print(f"❌ Scheduler Error: {e}")
        db.rollback()
    finally:
        db.close()

scheduler = BackgroundScheduler()
# Fixed ID and set to 10 minutes as requested
scheduler.add_job(
    run_sync_scraper, 
    'interval', 
    minutes=10, 
    id='run_sync_scraper'
)