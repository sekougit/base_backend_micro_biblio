from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class BorrowingCreate(BaseModel):
    book_id: int
    user_id: int
    duree_jours: int = Field(default=14, ge=1, le=90)


class BorrowingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    book_id: int
    user_id: int
    date_emprunt: datetime
    date_retour_prevue: datetime
    date_retour_effective: Optional[datetime]
    statut: str  # en_cours | retourne | en_retard (calculé)