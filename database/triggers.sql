-- ============================================
-- Triggers — gestion automatique de la disponibilité des livres
-- ============================================

-- Avant un nouvel emprunt : vérifier la disponibilité puis décrémenter le stock
CREATE OR REPLACE FUNCTION trg_fn_emprunt_livre()
RETURNS TRIGGER AS $$
DECLARE
    v_dispo INTEGER;
BEGIN
    SELECT quantite_disponible INTO v_dispo FROM books WHERE id = NEW.book_id FOR UPDATE;

    IF v_dispo IS NULL THEN
        RAISE EXCEPTION 'Livre % introuvable', NEW.book_id;
    END IF;

    IF v_dispo <= 0 THEN
        RAISE EXCEPTION 'Aucun exemplaire disponible pour le livre %', NEW.book_id;
    END IF;

    UPDATE books SET quantite_disponible = quantite_disponible - 1 WHERE id = NEW.book_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_avant_emprunt ON borrowings;
CREATE TRIGGER trg_avant_emprunt
    BEFORE INSERT ON borrowings
    FOR EACH ROW
    EXECUTE FUNCTION trg_fn_emprunt_livre();


-- Quand un emprunt passe à 'retourne' : réincrémenter le stock disponible
CREATE OR REPLACE FUNCTION trg_fn_retour_livre()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.statut = 'retourne' AND OLD.statut <> 'retourne' THEN
        UPDATE books SET quantite_disponible = quantite_disponible + 1 WHERE id = NEW.book_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_apres_retour ON borrowings;
CREATE TRIGGER trg_apres_retour
    BEFORE UPDATE ON borrowings
    FOR EACH ROW
    EXECUTE FUNCTION trg_fn_retour_livre();