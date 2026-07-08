-- ============================================
-- Données initiales
-- ============================================

CREATE EXTENSION IF NOT EXISTS pg_trgm;

INSERT INTO roles (nom, description) VALUES
    ('etudiant', 'Étudiant inscrit au DIT'),
    ('professeur', 'Enseignant du DIT'),
    ('personnel_administratif', 'Personnel administratif du DIT')
ON CONFLICT (nom) DO NOTHING;

INSERT INTO categories (nom, description) VALUES
    ('Informatique', 'Ouvrages liés au développement, réseaux, systèmes'),
    ('Mathématiques', 'Algèbre, analyse, statistiques'),
    ('Sciences de gestion', 'Management, économie, comptabilité'),
    ('Littérature', 'Romans, essais, poésie'),
    ('Langues', 'Apprentissage et linguistique')
ON CONFLICT (nom) DO NOTHING;

INSERT INTO publishers (nom, adresse, site_web) VALUES
    ('O''Reilly Media', 'Sebastopol, USA', 'https://oreilly.com'),
    ('Eyrolles', 'Paris, France', 'https://editions-eyrolles.com'),
    ('Dunod', 'Paris, France', 'https://dunod.com')
ON CONFLICT DO NOTHING;