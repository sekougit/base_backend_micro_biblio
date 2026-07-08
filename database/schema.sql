-- ============================================
-- Schéma de la base de données — Bibliothèque DIT
-- ============================================

CREATE TABLE IF NOT EXISTS roles (
    id          SERIAL PRIMARY KEY,
    nom         VARCHAR(50) UNIQUE NOT NULL,
    description VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS users (
    id             SERIAL PRIMARY KEY,
    nom            VARCHAR(100) NOT NULL,
    prenom         VARCHAR(100) NOT NULL,
    email          VARCHAR(255) UNIQUE NOT NULL,
    matricule      VARCHAR(50) UNIQUE,
    role_id        INTEGER NOT NULL REFERENCES roles(id) ON DELETE RESTRICT,
    date_creation  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS categories (
    id          SERIAL PRIMARY KEY,
    nom         VARCHAR(100) UNIQUE NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS publishers (
    id       SERIAL PRIMARY KEY,
    nom      VARCHAR(150) NOT NULL,
    adresse  VARCHAR(255),
    site_web VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS authors (
    id     SERIAL PRIMARY KEY,
    nom    VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    bio    TEXT
);

CREATE TABLE IF NOT EXISTS books (
    id                   SERIAL PRIMARY KEY,
    titre                VARCHAR(255) NOT NULL,
    isbn                 VARCHAR(20) UNIQUE NOT NULL,
    annee_publication    INTEGER,
    quantite_totale      INTEGER NOT NULL DEFAULT 1 CHECK (quantite_totale >= 0),
    quantite_disponible  INTEGER NOT NULL DEFAULT 1 CHECK (quantite_disponible >= 0),
    category_id          INTEGER REFERENCES categories(id) ON DELETE SET NULL,
    publisher_id         INTEGER REFERENCES publishers(id) ON DELETE SET NULL,
    date_ajout           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT ck_dispo_le_totale CHECK (quantite_disponible <= quantite_totale)
);

CREATE INDEX IF NOT EXISTS idx_books_titre ON books USING gin (titre gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_books_isbn  ON books (isbn);

CREATE TABLE IF NOT EXISTS book_authors (
    book_id   INTEGER NOT NULL REFERENCES books(id) ON DELETE CASCADE,
    author_id INTEGER NOT NULL REFERENCES authors(id) ON DELETE CASCADE,
    PRIMARY KEY (book_id, author_id)
);

CREATE TABLE IF NOT EXISTS borrowings (
    id                     SERIAL PRIMARY KEY,
    book_id                INTEGER NOT NULL REFERENCES books(id) ON DELETE RESTRICT,
    user_id                INTEGER NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    date_emprunt           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    date_retour_prevue     TIMESTAMPTZ NOT NULL,
    date_retour_effective  TIMESTAMPTZ,
    statut                 VARCHAR(20) NOT NULL DEFAULT 'en_cours'
                            CHECK (statut IN ('en_cours', 'retourne'))
);

CREATE INDEX IF NOT EXISTS idx_borrowings_user ON borrowings (user_id);
CREATE INDEX IF NOT EXISTS idx_borrowings_book ON borrowings (book_id);
CREATE INDEX IF NOT EXISTS idx_borrowings_statut ON borrowings (statut);