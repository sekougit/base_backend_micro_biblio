from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..dependencies import get_db

router = APIRouter(prefix="/categories", tags=["Catégories"])


@router.get("", response_model=list[schemas.CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return crud.list_categories(db)


@router.post("", response_model=schemas.CategoryOut, status_code=201)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    return crud.create_category(db, category)