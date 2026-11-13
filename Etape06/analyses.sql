-- Question 1 — Par site : réservations, quantité totale et associations distinctes.
SELECT
    s.code_site,
    s.nom,
    COUNT(r.id_reservation) AS nombre_reservations,
    COALESCE(SUM(r.quantite), 0) AS quantite_totale,
    COUNT(DISTINCT r.id_association) AS nombre_associations
FROM site AS s
LEFT JOIN reservation AS r
    ON r.code_site = s.code_site
GROUP BY s.code_site, s.nom
ORDER BY nombre_reservations DESC, s.code_site;
-- Nombre de lignes obtenues : 5.

-- Question 2 — Nombre de réservations par mois de début, au format AAAA-MM.
SELECT
    TO_CHAR(r.date_debut, 'YYYY-MM') AS mois,
    COUNT(r.id_reservation) AS nombre_reservations
FROM reservation AS r
GROUP BY TO_CHAR(r.date_debut, 'YYYY-MM')
ORDER BY mois;
-- Nombre de lignes obtenues : 13.

-- Question 3 — Les dix matériels les plus réservés.
SELECT
    m.id_materiel,
    m.designation,
    m.categorie,
    COUNT(r.id_reservation) AS nombre_reservations
FROM reservation AS r
JOIN materiel AS m
    ON m.id_materiel = r.id_materiel
GROUP BY m.id_materiel, m.designation, m.categorie
ORDER BY nombre_reservations DESC, m.id_materiel
LIMIT 10;
-- Nombre de lignes obtenues : 10.

-- Question 4 — Taux de retard global et par site, uniquement sur les prêts clos.
SELECT
    CASE
        WHEN GROUPING(s.code_site) = 1 THEN 'GLOBAL'
        ELSE MIN(s.code_site)::text
    END AS code_site,
    CASE
        WHEN GROUPING(s.code_site) = 1 THEN 'Tous les sites'
        ELSE MAX(s.nom)
    END AS nom,
    COUNT(r.id_reservation) AS reservations_closes,
    ROUND(
        100.0
        * COUNT(r.id_reservation) FILTER (
            WHERE r.date_retour_reelle > r.date_fin_prevue
        )
        / NULLIF(COUNT(r.id_reservation), 0),
        2
    ) AS taux_retard_pct
FROM site AS s
LEFT JOIN reservation AS r
    ON r.code_site = s.code_site
    AND r.date_retour_reelle IS NOT NULL
GROUP BY GROUPING SETS ((s.code_site), ())
ORDER BY GROUPING(s.code_site) DESC, code_site;
-- Nombre de lignes obtenues : 6 (global et cinq sites).
-- Taux global vérifié sur les CSV nettoyés : 32,41 %.

-- Question 5 — Catégories dont le nombre de réservations dépasse la moyenne.
WITH reservations_par_categorie AS (
    SELECT
        m.categorie,
        COUNT(r.id_reservation) AS nombre_reservations
    FROM materiel AS m
    LEFT JOIN reservation AS r
        ON r.id_materiel = m.id_materiel
    GROUP BY m.categorie
)
SELECT
    categorie,
    nombre_reservations
FROM reservations_par_categorie
WHERE nombre_reservations > (
    SELECT AVG(nombre_reservations)
    FROM reservations_par_categorie
)
ORDER BY nombre_reservations DESC, categorie;
-- Nombre de lignes obtenues : 2.

-- Question 6 — Matériel le plus réservé par site, départagé par id_materiel.
WITH reservations_par_materiel AS (
    SELECT
        r.code_site,
        m.id_materiel,
        m.designation,
        COUNT(r.id_reservation) AS nombre_reservations
    FROM reservation AS r
    JOIN materiel AS m
        ON m.id_materiel = r.id_materiel
    GROUP BY r.code_site, m.id_materiel, m.designation
),
classement AS (
    SELECT
        code_site,
        id_materiel,
        designation,
        nombre_reservations,
        ROW_NUMBER() OVER (
            PARTITION BY code_site
            ORDER BY nombre_reservations DESC, id_materiel
        ) AS rang
    FROM reservations_par_materiel
)
SELECT
    s.code_site,
    s.nom,
    c.id_materiel,
    c.designation,
    COALESCE(c.nombre_reservations, 0) AS nombre_reservations
FROM site AS s
LEFT JOIN classement AS c
    ON c.code_site = s.code_site
    AND c.rang = 1
ORDER BY s.code_site;
-- Nombre de lignes obtenues : 5.

-- Question 7 — Durée réelle moyenne, globalement puis par catégorie, sur les prêts clos.
SELECT
    CASE
        WHEN GROUPING(m.categorie) = 1 THEN 'GLOBAL'
        ELSE m.categorie
    END AS categorie,
    ROUND(
        AVG((r.date_retour_reelle - r.date_debut)::numeric),
        1
    ) AS duree_moyenne_jours
FROM reservation AS r
JOIN materiel AS m
    ON m.id_materiel = r.id_materiel
WHERE r.date_retour_reelle IS NOT NULL
GROUP BY GROUPING SETS ((), (m.categorie))
ORDER BY GROUPING(m.categorie) DESC, duree_moyenne_jours DESC, categorie;
-- Nombre de lignes obtenues : 7 (global et six catégories).

-- Coût : les requêtes 3 et 6 regroupent les réservations par matériel.
-- La requête 6 ajoute un classement par fenêtre pour chaque site.
-- La requête 4 parcourt les prêts clos et calcule les retards par site.
-- Les requêtes 5 et 7 joignent et agrègent les réservations par catégorie.