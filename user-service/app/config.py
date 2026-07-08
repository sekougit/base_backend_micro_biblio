import os
from pydantic_settings import BaseSettings

# Forcer l'encodage UTF-8 pour éviter les erreurs de décodage
os.environ['PGCLIENTENCODING'] = 'UTF8'

#  PostgreSQL  en local
#SQLALCHEMY_DATABASE_URL = "postgresql://admin:admin123@localhost:5432/dbdit"

# Postgres conteneurise
SQLALCHEMY_DATABASE_URL = "postgresql://admin:admin123@postgres_server:5432/dbdit"

#  PostgreSQL  en deploiement avec Docker Compose
#SQLALCHEMY_DATABASE_URL = "postgresql://admin:admin123@db-service:5432/dbemploye"


class Settings(BaseSettings):
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql://dit_user:dit_password@postgres:5432/library_db",
    )
    service_name: str = "user-service"


settings = Settings()