from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RoleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nom: str
    description: Optional[str] = None


class UserBase(BaseModel):
    nom: str = Field(..., min_length=1, max_length=100)
    prenom: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    matricule: Optional[str] = None
    role_id: int


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    nom: Optional[str] = None
    prenom: Optional[str] = None
    email: Optional[EmailStr] = None
    matricule: Optional[str] = None
    role_id: Optional[int] = None


class UserOut(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    date_creation: datetime
    role: Optional[RoleOut] = None