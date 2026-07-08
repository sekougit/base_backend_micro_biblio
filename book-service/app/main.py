from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import books, authors, categories, publishers
from .config import settings

app = FastAPI(title="DIT Library - Book Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(books.router)
app.include_router(authors.router)
app.include_router(categories.router)
app.include_router(publishers.router)


@app.get("/health")
def health():
    return {"status": "ok", "service": settings.service_name}