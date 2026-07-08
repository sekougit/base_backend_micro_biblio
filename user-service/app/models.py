from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    nom = Column(String(50), unique=True, nullable=False)
    description = Column(String(255))

    users = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    matricule = Column(String(50), unique=True, nullable=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    date_creation = Column(DateTime(timezone=True), server_default=func.now())

    role = relationship("Role", back_populates="users")