from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..dependencies import get_db

router = APIRouter(prefix="/roles", tags=["Rôles"])


@router.get("", response_model=list[schemas.RoleOut])
def list_roles(db: Session = Depends(get_db)):
    """Liste les types d'utilisateurs (étudiant, professeur, personnel administratif)."""
    return crud.list_roles(db)