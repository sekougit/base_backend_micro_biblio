from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


# --- Category ---
class CategoryBase(BaseModel):
    nom: str
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryOut(CategoryBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


# --- Publisher ---
class PublisherBase(BaseModel):
    nom: str
    adresse: Optional[str] = None
    site_web: Optional[str] = None


class PublisherCreate(PublisherBase):
    pass


class PublisherOut(PublisherBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


# --- Author ---
class AuthorBase(BaseModel):
    nom: str
    prenom: str
    bio: Optional[str] = None


class AuthorCreate(AuthorBase):
    pass


class AuthorOut(AuthorBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


# --- Book ---
class BookBase(BaseModel):
    titre: str = Field(..., min_length=1, max_length=255)
    isbn: str = Field(..., min_length=3, max_length=20)
    annee_publication: Optional[int] = None
    quantite_totale: int = Field(default=1, ge=1)
    category_id: Optional[int] = None
    publisher_id: Optional[int] = None


class BookCreate(BookBase):
    author_ids: list[int] = []


class BookUpdate(BaseModel):
    titre: Optional[str] = None
    isbn: Optional[str] = None
    annee_publication: Optional[int] = None
    quantite_totale: Optional[int] = None
    category_id: Optional[int] = None
    publisher_id: Optional[int] = None
    author_ids: Optional[list[int]] = None


class BookOut(BookBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    quantite_disponible: int
    date_ajout: datetime
    category: Optional[CategoryOut] = None
    publisher: Optional[PublisherOut] = None
    authors: list[AuthorOut] = []


class AvailabilityUpdate(BaseModel):
    delta: int  # -1 emprunt, +1 retour (endpoint de secours, le trigger DB gère déjà le cas normal)