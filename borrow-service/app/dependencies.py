from .database import SessionLocal


def get_db():
    """Fournit une session DB par requête, fermée automatiquement à la fin."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()