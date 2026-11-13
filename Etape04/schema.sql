-- À exécuter dans la base ccfl, créée au préalable avec : createdb ccfl
-- Exemple depuis la racine : psql -d ccfl -f Etape04/schema.sql

DROP TABLE IF EXISTS reservation;
DROP TABLE IF EXISTS association;
DROP TABLE IF EXISTS materiel;
DROP TABLE IF EXISTS site;

CREATE TABLE site (
    code_site CHAR(7) PRIMARY KEY,
    nom VARCHAR(120) NOT NULL,
    commune VARCHAR(80) NOT NULL,
    annee_ouverture SMALLINT NOT NULL,
    surface_m2 INTEGER NOT NULL
);

CREATE TABLE materiel (
    id_materiel INTEGER PRIMARY KEY,
    reference VARCHAR(8) NOT NULL,
    designation VARCHAR(120) NOT NULL,
    categorie VARCHAR(40) NOT NULL,
    etat VARCHAR(20) NOT NULL,
    annee_achat SMALLINT,
    code_site CHAR(7) NOT NULL,
    valeur_achat NUMERIC(8, 2),
    CONSTRAINT fk_materiel_site
        FOREIGN KEY (code_site) REFERENCES site (code_site)
);

CREATE TABLE association (
    id_association INTEGER PRIMARY KEY,
    nom VARCHAR(150) NOT NULL,
    type_association VARCHAR(30),
    commune VARCHAR(80) NOT NULL,
    code_postal CHAR(5),
    date_convention DATE NOT NULL,
    code_site CHAR(7) NOT NULL,
    convention_active BOOLEAN NOT NULL,
    CONSTRAINT fk_association_site
        FOREIGN KEY (code_site) REFERENCES site (code_site)
);

CREATE TABLE reservation (
    id_reservation CHAR(7) PRIMARY KEY,
    id_materiel INTEGER NOT NULL,
    id_association INTEGER NOT NULL,
    code_site CHAR(7) NOT NULL,
    quantite INTEGER NOT NULL,
    date_debut DATE NOT NULL,
    date_fin_prevue DATE NOT NULL,
    date_retour_reelle DATE,
    CONSTRAINT fk_reservation_materiel
        FOREIGN KEY (id_materiel) REFERENCES materiel (id_materiel),
    CONSTRAINT fk_reservation_association
        FOREIGN KEY (id_association) REFERENCES association (id_association),
    CONSTRAINT fk_reservation_site
        FOREIGN KEY (code_site) REFERENCES site (code_site),
    CONSTRAINT ck_reservation_dates
        CHECK (date_fin_prevue >= date_debut),
    CONSTRAINT ck_reservation_quantite
        CHECK (quantite > 0)
);