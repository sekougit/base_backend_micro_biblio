from sqlalchemy import (
    Column, Integer, String, Text, DateTime, ForeignKey, Table, CheckConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

# Table d'association many-to-many livres <-> auteurs
book_authors = Table(
    "book_authors",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("books.id", ondelete="CASCADE"), primary_key=True),
    Column("author_id", Integer, ForeignKey("authors.id", ondelete="CASCADE"), primary_key=True),
)


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    nom = Column(String(100), unique=True, nullable=False)
    description = Column(Text)

    books = relationship("Book", back_populates="category")


class Publisher(Base):
    __tablename__ = "publishers"

    id = Column(Integer, primary_key=True)
    nom = Column(String(150), nullable=False)
    adresse = Column(String(255))
    site_web = Column(String(255))

    books = relationship("Book", back_populates="publisher")


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    bio = Column(Text)

    books = relationship("Book", secondary=book_authors, back_populates="authors")


class Book(Base):
    __tablename__ = "books"
    __table_args__ = (
        CheckConstraint("quantite_disponible <= quantite_totale", name="ck_dispo_le_totale"),
    )

    id = Column(Integer, primary_key=True)
    titre = Column(String(255), nullable=False, index=True)
    isbn = Column(String(20), unique=True, nullable=False, index=True)
    annee_publication = Column(Integer, nullable=True)
    quantite_totale = Column(Integer, nullable=False, default=1)
    quantite_disponible = Column(Integer, nullable=False, default=1)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    publisher_id = Column(Integer, ForeignKey("publishers.id"), nullable=True)
    date_ajout = Column(DateTime(timezone=True), server_default=func.now())

    category = relationship("Category", back_populates="books")
    publisher = relationship("Publisher", back_populates="books")
    authors = relationship("Author", secondary=book_authors, back_populates="books")