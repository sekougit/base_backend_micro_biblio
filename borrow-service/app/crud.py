from datetime import datetime, timedelta, timezone
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from . import models


def _effective_status(loan: models.Borrowing) -> str:
    if loan.statut == "retourne":
        return "retourne"
    now = datetime.now(timezone.utc)
    due = loan.date_retour_prevue
    if due.tzinfo is None:
        due = due.replace(tzinfo=timezone.utc)
    return "en_retard" if due < now else "en_cours"


def to_out(loan: models.Borrowing) -> dict:
    return {
        "id": loan.id,
        "book_id": loan.book_id,
        "user_id": loan.user_id,
        "date_emprunt": loan.date_emprunt,
        "date_retour_prevue": loan.date_retour_prevue,
        "date_retour_effective": loan.date_retour_effective,
        "statut": _effective_status(loan),
    }


def create_borrowing(db: Session, book_id: int, user_id: int, duree_jours: int):
    """L'INSERT déclenche le trigger PostgreSQL trg_avant_emprunt qui vérifie
    la disponibilité et décrémente automatiquement books.quantite_disponible."""
    loan = models.Borrowing(
        book_id=book_id,
        user_id=user_id,
        date_retour_prevue=datetime.now(timezone.utc) + timedelta(days=duree_jours),
        statut="en_cours",
    )
    db.add(loan)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise ValueError(str(e.orig)) from e
    db.refresh(loan)
    return loan


def list_borrowings(db: Session, user_id: int | None = None, book_id: int | None = None):
    query = db.query(models.Borrowing)
    if user_id is not None:
        query = query.filter(models.Borrowing.user_id == user_id)
    if book_id is not None:
        query = query.filter(models.Borrowing.book_id == book_id)
    return query.order_by(models.Borrowing.id.desc()).all()


def get_borrowing(db: Session, loan_id: int):
    return db.query(models.Borrowing).filter(models.Borrowing.id == loan_id).first()


def return_borrowing(db: Session, loan_id: int):
    """Le passage à statut='retourne' déclenche trg_apres_retour qui
    réincrémente automatiquement books.quantite_disponible."""
    loan = get_borrowing(db, loan_id)
    if not loan:
        return None
    if loan.statut == "retourne":
        return "already_returned"
    loan.statut = "retourne"
    loan.date_retour_effective = datetime.now(timezone.utc)
    db.commit()
    db.refresh(loan)
    return loan