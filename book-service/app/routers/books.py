from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..dependencies import get_db

router = APIRouter(prefix="/books", tags=["Livres"])


@router.post("", response_model=schemas.BookOut, status_code=201)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    if crud.get_book_by_isbn(db, book.isbn):
        raise HTTPException(status_code=409, detail="Un livre avec cet ISBN existe déjà")
    return crud.create_book(db, book)


@router.get("", response_model=list[schemas.BookOut])
def list_books(skip: int = 0, limit: int = 100, q: Optional[str] = None, db: Session = Depends(get_db)):
    """Liste des livres. Recherche par titre, auteur ou ISBN via ?q="""
    return crud.list_books(db, skip=skip, limit=limit, q=q)


@router.get("/{book_id}", response_model=schemas.BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Livre introuvable")
    return db_book


@router.put("/{book_id}", response_model=schemas.BookOut)
def update_book(book_id: int, book: schemas.BookUpdate, db: Session = Depends(get_db)):
    db_book = crud.update_book(db, book_id, book)
    if not db_book:
        raise HTTPException(status_code=404, detail="Livre introuvable")
    return db_book


@router.delete("/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.delete_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Livre introuvable")
    return None


@router.patch("/{book_id}/availability", response_model=schemas.BookOut)
def update_availability(book_id: int, payload: schemas.AvailabilityUpdate, db: Session = Depends(get_db)):
    """Endpoint de secours : normalement le trigger DB gère déjà la disponibilité
    lors d'un emprunt/retour, mais ceci reste utile pour des corrections manuelles."""
    result = crud.update_availability(db, book_id, payload.delta)
    if result is None:
        raise HTTPException(status_code=404, detail="Livre introuvable")
    if result == "invalid":
        raise HTTPException(status_code=400, detail="Quantité disponible invalide")
    return result