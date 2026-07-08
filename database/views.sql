-- ============================================
-- Vues SQL
-- ============================================

-- Catalogue complet avec catégorie, éditeur et auteurs agrégés
CREATE OR REPLACE VIEW vue_catalogue AS
SELECT
    b.id,
    b.titre,
    b.isbn,
    b.annee_publication,
    b.quantite_totale,
    b.quantite_disponible,
    c.nom AS categorie,
    p.nom AS editeur,
    STRING_AGG(DISTINCT a.prenom || ' ' || a.nom, ', ') AS auteurs
FROM books b
LEFT JOIN categories c ON c.id = b.category_id
LEFT JOIN publishers p ON p.id = b.publisher_id
LEFT JOIN book_authors ba ON ba.book_id = b.id
LEFT JOIN authors a ON a.id = ba.author_id
GROUP BY b.id, c.nom, p.nom;


-- Emprunts actuellement en retard, avec infos usager et livre
CREATE OR REPLACE VIEW vue_emprunts_retard AS
SELECT
    br.id AS emprunt_id,
    u.id AS user_id,
    u.nom || ' ' || u.prenom AS usager,
    u.email,
    bo.id AS book_id,
    bo.titre,
    br.date_emprunt,
    br.date_retour_prevue,
    NOW() - br.date_retour_prevue AS retard
FROM borrowings br
JOIN users u ON u.id = br.user_id
JOIN books bo ON bo.id = br.book_id
WHERE br.statut = 'en_cours' AND br.date_retour_prevue < NOW();


-- Statistiques globales
CREATE OR REPLACE VIEW vue_statistiques AS
SELECT
    (SELECT COUNT(*) FROM books) AS total_livres,
    (SELECT COALESCE(SUM(quantite_totale),0) FROM books) AS total_exemplaires,
    (SELECT COUNT(*) FROM users) AS total_usagers,
    (SELECT COUNT(*) FROM borrowings WHERE statut = 'en_cours') AS emprunts_en_cours,
    (SELECT fn_nombre_retards()) AS emprunts_en_retard;