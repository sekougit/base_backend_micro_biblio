from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import clients, crud
from ..schemas import BorrowingCreate, BorrowingOut
from ..dependencies import get_db

router = APIRouter(prefix="/borrowings", tags=["Emprunts"])


@router.post("", response_model=BorrowingOut, status_code=201)
async def create_borrowing(payload: BorrowingCreate, db: Session = Depends(get_db)):
    """Emprunter un livre : vérifie l'utilisateur et le livre via REST
    auprès de user-service et book-service, puis insère l'emprunt
    (le trigger DB gère la décrémentation du stock)."""
    user = await clients.get_user(payload.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    book = await clients.get_book(payload.book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Livre introuvable")
    if book["quantite_disponible"] <= 0:
        raise HTTPException(status_code=409, detail="Aucun exemplaire disponible")

    try:
        loan = crud.create_borrowing(db, payload.book_id, payload.user_id, payload.duree_jours)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=f"Emprunt refusé par la base : {e}")

    return crud.to_out(loan)


@router.get("", response_model=list[BorrowingOut])
def list_borrowings(
    user_id: Optional[int] = None,
    book_id: Optional[int] = None,
    en_retard: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    """Historique des emprunts avec détection des retards via ?en_retard=true."""
    loans = [crud.to_out(l) for l in crud.list_borrowings(db, user_id, book_id)]
    if en_retard is True:
        loans = [l for l in loans if l["statut"] == "en_retard"]
    elif en_retard is False:
        loans = [l for l in loans if l["statut"] != "en_retard"]
    return loans


@router.get("/{loan_id}", response_model=BorrowingOut)
def get_borrowing(loan_id: int, db: Session = Depends(get_db)):
    loan = crud.get_borrowing(db, loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Emprunt introuvable")
    return crud.to_out(loan)


@router.patch("/{loan_id}/return", response_model=BorrowingOut)
def return_borrowing(loan_id: int, db: Session = Depends(get_db)):
    """Retourner un livre (le trigger DB réincrémente le stock automatiquement)."""
    result = crud.return_borrowing(db, loan_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Emprunt introuvable")
    if result == "already_returned":
        raise HTTPException(status_code=409, detail="Ce livre a déjà été retourné")
    return crud.to_out(result)