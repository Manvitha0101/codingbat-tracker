import pandas as pd
from app.database import SessionLocal, engine
from app.models import Student, Base

def seed_database():
    # This creates the tables in Postgres if they don't exist
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        # Reading your specific CSV format
        df = pd.read_csv("users.csv")
        
        for _, row in df.iterrows():
            raw_id = str(row['USERID'])
            profile_url = row['PROFILELINK']
            
            # Logic to split "24251a1206-manvitha" into ID and Name
            if "-" in raw_id:
                student_id, name = raw_id.split("-", 1)
            else:
                student_id, name = raw_id, "Unknown"

            # Avoid duplicates
            exists = db.query(Student).filter(Student.student_id == student_id).first()
            if not exists:
                new_student = Student(
                    student_id=student_id,
                    name=name.capitalize(),
                    codingbat_url=profile_url
                )
                db.add(new_student)
        
        db.commit()
        print(f"✅ Successfully loaded {len(df)} students into the database.")
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()