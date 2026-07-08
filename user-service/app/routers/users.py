from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..dependencies import get_db

router = APIRouter(prefix="/users", tags=["Utilisateurs"])


@router.post("", response_model=schemas.UserOut, status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code=409, detail="Un utilisateur avec cet email existe déjà")
    return crud.create_user(db, user)


@router.get("", response_model=list[schemas.UserOut])
def list_users(skip: int = 0, limit: int = 100, role: Optional[str] = None, db: Session = Depends(get_db)):
    return crud.list_users(db, skip=skip, limit=limit, role_nom=role)


@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Consultation du profil utilisateur."""
    db_user = crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    return db_user


@router.put("/{user_id}", response_model=schemas.UserOut)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db, user_id, user)
    if not db_user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    return db_user


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    return None