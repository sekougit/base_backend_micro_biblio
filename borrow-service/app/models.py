from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.sql import func
from .database import Base


class Borrowing(Base):
    __tablename__ = "borrowings"

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    date_emprunt = Column(DateTime(timezone=True), server_default=func.now())
    date_retour_prevue = Column(DateTime(timezone=True), nullable=False)
    date_retour_effective = Column(DateTime(timezone=True), nullable=True)
    statut = Column(String(20), nullable=False, default="en_cours")