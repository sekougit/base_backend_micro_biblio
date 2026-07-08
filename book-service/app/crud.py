from sqlalchemy import or_
from sqlalchemy.orm import Session
from . import models, schemas


# --- Books ---
def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def get_book_by_isbn(db: Session, isbn: str):
    return db.query(models.Book).filter(models.Book.isbn == isbn).first()


def list_books(db: Session, skip: int = 0, limit: int = 100, q: str | None = None):
    query = db.query(models.Book)
    if q:
        like = f"%{q}%"
        query = query.join(models.Book.authors, isouter=True).filter(
            or_(
                models.Book.titre.ilike(like),
                models.Book.isbn.ilike(like),
                models.Author.nom.ilike(like),
                models.Author.prenom.ilike(like),
            )
        ).distinct()
    return query.order_by(models.Book.id).offset(skip).limit(limit).all()


def _attach_authors(db: Session, book: models.Book, author_ids: list[int]):
    if author_ids is None:
        return
    authors = db.query(models.Author).filter(models.Author.id.in_(author_ids)).all()
    book.authors = authors


def create_book(db: Session, book: schemas.BookCreate):
    data = book.model_dump(exclude={"author_ids"})
    db_book = models.Book(**data, quantite_disponible=book.quantite_totale)
    db.add(db_book)
    db.flush()
    _attach_authors(db, db_book, book.author_ids)
    db.commit()
    db.refresh(db_book)
    return db_book


def update_book(db: Session, book_id: int, book: schemas.BookUpdate):
    db_book = get_book(db, book_id)
    if not db_book:
        return None
    data = book.model_dump(exclude_unset=True, exclude={"author_ids"})
    for key, value in data.items():
        setattr(db_book, key, value)
    if book.author_ids is not None:
        _attach_authors(db, db_book, book.author_ids)
    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int):
    db_book = get_book(db, book_id)
    if not db_book:
        return None
    db.delete(db_book)
    db.commit()
    return db_book


def update_availability(db: Session, book_id: int, delta: int):
    db_book = get_book(db, book_id)
    if not db_book:
        return None
    new_qty = db_book.quantite_disponible + delta
    if new_qty < 0 or new_qty > db_book.quantite_totale:
        return "invalid"
    db_book.quantite_disponible = new_qty
    db.commit()
    db.refresh(db_book)
    return db_book


# --- Categories ---
def list_categories(db: Session):
    return db.query(models.Category).order_by(models.Category.nom).all()


def create_category(db: Session, category: schemas.CategoryCreate):
    db_cat = models.Category(**category.model_dump())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat


# --- Publishers ---
def list_publishers(db: Session):
    return db.query(models.Publisher).order_by(models.Publisher.nom).all()


def create_publisher(db: Session, publisher: schemas.PublisherCreate):
    db_pub = models.Publisher(**publisher.model_dump())
    db.add(db_pub)
    db.commit()
    db.refresh(db_pub)
    return db_pub


# --- Authors ---
def list_authors(db: Session):
    return db.query(models.Author).order_by(models.Author.nom).all()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(**author.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author