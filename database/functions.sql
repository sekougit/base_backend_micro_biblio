-- ============================================
-- Fonctions PostgreSQL
-- ============================================

-- Retourne le nombre d'exemplaires disponibles d'un livre
CREATE OR REPLACE FUNCTION fn_quantite_disponible(p_book_id INTEGER)
RETURNS INTEGER AS $$
DECLARE
    v_qte INTEGER;
BEGIN
    SELECT quantite_disponible INTO v_qte FROM books WHERE id = p_book_id;
    RETURN COALESCE(v_qte, 0);
END;
$$ LANGUAGE plpgsql STABLE;


-- Retourne vrai si un emprunt donné est actuellement en retard
CREATE OR REPLACE FUNCTION fn_est_en_retard(p_borrowing_id INTEGER)
RETURNS BOOLEAN AS $$
DECLARE
    v_statut VARCHAR(20);
    v_date_prevue TIMESTAMPTZ;
BEGIN
    SELECT statut, date_retour_prevue INTO v_statut, v_date_prevue
    FROM borrowings WHERE id = p_borrowing_id;

    IF v_statut = 'retourne' THEN
        RETURN FALSE;
    END IF;

    RETURN v_date_prevue < NOW();
END;
$$ LANGUAGE plpgsql STABLE;


-- Nombre total d'emprunts en retard, à un instant T
CREATE OR REPLACE FUNCTION fn_nombre_retards()
RETURNS INTEGER AS $$
DECLARE
    v_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO v_count
    FROM borrowings
    WHERE statut = 'en_cours' AND date_retour_prevue < NOW();
    RETURN v_count;
END;
$$ LANGUAGE plpgsql STABLE;