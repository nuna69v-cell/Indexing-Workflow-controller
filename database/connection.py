class DummySession:
    def close(self):
        pass

def SessionLocal():
    return DummySession()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
