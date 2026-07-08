from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import users, roles
from .config import settings

app = FastAPI(title="DIT Library - User Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(roles.router)


@app.get("/health")
def health():
    return {"status": "ok", "service": settings.service_name}