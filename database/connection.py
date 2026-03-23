from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# This is a dummy for the test
engine = create_engine("sqlite:///:memory:")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
