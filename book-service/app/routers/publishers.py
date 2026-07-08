from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..dependencies import get_db

router = APIRouter(prefix="/publishers", tags=["Éditeurs"])


@router.get("", response_model=list[schemas.PublisherOut])
def list_publishers(db: Session = Depends(get_db)):
    return crud.list_publishers(db)


@router.post("", response_model=schemas.PublisherOut, status_code=201)
def create_publisher(publisher: schemas.PublisherCreate, db: Session = Depends(get_db)):
    return crud.create_publisher(db, publisher)