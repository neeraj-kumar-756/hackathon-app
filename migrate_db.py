from app import create_app
from app.models.model import db
from sqlalchemy import text

app = create_app()

with app.app_context():
    print("Running database migrations...")
    db.create_all()
    
    # Auto-update schema to add new columns if they are missing
    try:
        with db.engine.connect() as conn:
            conn.execute(text("ALTER TABLE employees ADD COLUMN IF NOT EXISTS pan VARCHAR(20)"))
            conn.execute(text("ALTER TABLE employees ADD COLUMN IF NOT EXISTS uan VARCHAR(20)"))
            conn.execute(text("ALTER TABLE employees ADD COLUMN IF NOT EXISTS pf_number VARCHAR(20)"))
            conn.execute(text("ALTER TABLE employees ADD COLUMN IF NOT EXISTS esi_number VARCHAR(20)"))
            conn.execute(text("ALTER TABLE employees ADD COLUMN IF NOT EXISTS department VARCHAR(50)"))
            conn.execute(text("ALTER TABLE payrolls ADD COLUMN IF NOT EXISTS attendance_days INTEGER DEFAULT 0"))
            conn.execute(text("ALTER TABLE companies ADD COLUMN IF NOT EXISTS pt_circle VARCHAR(50)"))
            
            # Note: This syntax is for PostgreSQL.
            # conn.execute(text("ALTER TABLE payrolls ALTER COLUMN attendance_days TYPE FLOAT")) 
            
            conn.commit()
            print("Schema updated successfully.")
    except Exception as e:
        print(f"Schema update note: {e}")