from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..dependencies import get_db

router = APIRouter(prefix="/authors", tags=["Auteurs"])


@router.get("", response_model=list[schemas.AuthorOut])
def list_authors(db: Session = Depends(get_db)):
    return crud.list_authors(db)


@router.post("", response_model=schemas.AuthorOut, status_code=201)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db, author)