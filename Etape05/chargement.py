import csv
import json
import logging
import os
import time
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Callable

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, text
from sqlalchemy.exc import SQLAlchemyError


RACINE = Path(__file__).resolve().parent.parent
FICHIER_ENV = RACINE / ".env"
FICHIER_SITES = RACINE / "data" / "sites.csv"
FICHIER_MATERIEL = RACINE / "sorties" / "materiel_propre.csv"
FICHIER_ASSOCIATIONS = RACINE / "sorties" / "associations_propre.csv"
FICHIER_RESERVATIONS = RACINE / "sorties" / "reservations_propre.csv"
FICHIER_REJETS = RACINE / "sorties" / "rejets_chargement.csv"
TAILLE_LOT = 500

LOGGER = logging.getLogger("ccfl.chargement")

LIGNES_INSERTION = {
    "site": """
        INSERT INTO site (
            code_site, nom, commune, annee_ouverture, surface_m2
        ) VALUES (
            :code_site, :nom, :commune, :annee_ouverture, :surface_m2
        )
    """,
    "materiel": """
        INSERT INTO materiel (
            id_materiel, reference, designation, categorie, etat,
            annee_achat, code_site, valeur_achat
        ) VALUES (
            :id_materiel, :reference, :designation, :categorie, :etat,
            :annee_achat, :code_site, :valeur_achat
        )
    """,
    "association": """
        INSERT INTO association (
            id_association, nom, type_association, commune, code_postal,
            date_convention, code_site, convention_active
        ) VALUES (
            :id_association, :nom, :type_association, :commune, :code_postal,
            :date_convention, :code_site, :convention_active
        )
    """,
    "reservation": """
        INSERT INTO reservation (
            id_reservation, id_materiel, id_association, code_site, quantite,
            date_debut, date_fin_prevue, date_retour_reelle
        ) VALUES (
            :id_reservation, :id_materiel, :id_association, :code_site,
            :quantite, :date_debut, :date_fin_prevue, :date_retour_reelle
        )
    """,
}


@dataclass
class ResultatTable:
    table: str
    lues: int
    inserees: int
    rejetees: int
    duree_secondes: float


LigneCSV = dict[str, str | None]
Convertisseur = Callable[[LigneCSV], dict[str, Any]]


def configurer_journalisation():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def creer_engine():
    load_dotenv(FICHIER_ENV)
    port = int(os.getenv("CCFL_DB_PORT", "5432"))
    url = URL.create(
        "postgresql+psycopg2",
        username=os.getenv("CCFL_DB_USER") or None,
        password=os.getenv("CCFL_DB_PASSWORD") or None,
        host=os.getenv("CCFL_DB_HOST", "localhost"),
        port=port,
        database=os.getenv("CCFL_DB_NAME", "ccfl"),
    )
    return create_engine(url, pool_pre_ping=True)


def lire_csv(chemin):
    with chemin.open("r", encoding="utf-8", newline="") as fichier:
        return [dict(ligne) for ligne in csv.DictReader(fichier)]


def valeur_obligatoire(ligne, colonne):
    valeur = ligne.get(colonne)
    if valeur is None or valeur.strip() == "":
        raise ValueError(f"La colonne {colonne} est obligatoire.")
    return valeur.strip()


def valeur_optionnelle(ligne, colonne):
    valeur = ligne.get(colonne)
    if valeur is None or valeur.strip() == "":
        return None
    return valeur.strip()


def entier(ligne, colonne):
    return int(valeur_obligatoire(ligne, colonne))


def entier_optionnel(ligne, colonne):
    valeur = valeur_optionnelle(ligne, colonne)
    return int(valeur) if valeur is not None else None


def decimal_optionnel(ligne, colonne):
    valeur = valeur_optionnelle(ligne, colonne)
    if valeur is None:
        return None
    try:
        return Decimal(valeur.replace(",", "."))
    except InvalidOperation as exc:
        raise ValueError(f"La colonne {colonne} n'est pas un nombre.") from exc


def date_obligatoire(ligne, colonne):
    valeur = valeur_obligatoire(ligne, colonne)
    try:
        return date.fromisoformat(valeur)
    except ValueError as exc:
        raise ValueError(f"La colonne {colonne} n'est pas une date ISO.") from exc


def date_optionnelle(ligne, colonne):
    valeur = valeur_optionnelle(ligne, colonne)
    if valeur is None:
        return None
    try:
        return date.fromisoformat(valeur)
    except ValueError as exc:
        raise ValueError(f"La colonne {colonne} n'est pas une date ISO.") from exc


def convertir_site(ligne):
    return {
        "code_site": valeur_obligatoire(ligne, "code_site"),
        "nom": valeur_obligatoire(ligne, "nom"),
        "commune": valeur_obligatoire(ligne, "commune"),
        "annee_ouverture": entier(ligne, "annee_ouverture"),
        "surface_m2": entier(ligne, "surface_m2"),
    }


def convertir_materiel(ligne):
    return {
        "id_materiel": entier(ligne, "id_materiel"),
        "reference": valeur_obligatoire(ligne, "reference"),
        "designation": valeur_obligatoire(ligne, "designation"),
        "categorie": valeur_obligatoire(ligne, "categorie"),
        "etat": valeur_obligatoire(ligne, "etat"),
        "annee_achat": entier_optionnel(ligne, "annee_achat"),
        "code_site": valeur_obligatoire(ligne, "code_site"),
        "valeur_achat": decimal_optionnel(ligne, "valeur_achat"),
    }


def convertir_association(ligne):
    convention_active = valeur_obligatoire(ligne, "convention_active").lower()
    if convention_active not in {"oui", "non"}:
        raise ValueError("convention_active doit valoir « oui » ou « non ».")
    return {
        "id_association": entier(ligne, "id_association"),
        "nom": valeur_obligatoire(ligne, "nom"),
        "type_association": valeur_optionnelle(ligne, "type_association"),
        "commune": valeur_obligatoire(ligne, "commune"),
        "code_postal": valeur_optionnelle(ligne, "code_postal"),
        "date_convention": date_obligatoire(ligne, "date_convention"),
        "code_site": valeur_obligatoire(ligne, "code_site"),
        "convention_active": convention_active == "oui",
    }


def convertir_reservation(ligne):
    return {
        "id_reservation": valeur_obligatoire(ligne, "id_reservation"),
        "id_materiel": entier(ligne, "id_materiel"),
        "id_association": entier(ligne, "id_association"),
        "code_site": valeur_obligatoire(ligne, "code_site"),
        "quantite": entier(ligne, "quantite"),
        "date_debut": date_obligatoire(ligne, "date_debut"),
        "date_fin_prevue": date_obligatoire(ligne, "date_fin_prevue"),
        "date_retour_reelle": date_optionnelle(ligne, "date_retour_reelle"),
    }


def enregistrer_rejet(rejets, table, numero_ligne, ligne, motif):
    rejets.append(
        {
            "table": table,
            "ligne_csv": str(numero_ligne),
            "donnees": json.dumps(ligne, ensure_ascii=False),
            "motif_rejet": motif.replace("\n", " ")[:1000],
        }
    )


def inserer_par_lots(conn, table, requete, lignes, rejets):
    inserees = 0
    for debut in range(0, len(lignes), TAILLE_LOT):
        lot = lignes[debut : debut + TAILLE_LOT]
        try:
            with conn.begin_nested():
                conn.execute(text(requete), [donnees for _, _, donnees in lot])
            inserees += len(lot)
        except SQLAlchemyError as erreur_lot:
            LOGGER.warning(
                "Échec d'un lot de %d lignes pour %s ; nouvelle tentative ligne "
                "par ligne : %s",
                len(lot),
                table,
                str(erreur_lot).splitlines()[0],
            )
            for numero_ligne, ligne_source, donnees in lot:
                try:
                    with conn.begin_nested():
                        conn.execute(text(requete), donnees)
                    inserees += 1
                except SQLAlchemyError as erreur_ligne:
                    enregistrer_rejet(
                        rejets,
                        table,
                        numero_ligne,
                        ligne_source,
                        str(erreur_ligne),
                    )
    return inserees


def charger_table(conn, table, chemin, convertir, rejets,):
    debut = time.perf_counter()
    lignes_source = lire_csv(chemin)
    lignes_pretes: list[tuple[int, LigneCSV, dict[str, Any]]] = []
    for numero_ligne, ligne in enumerate(lignes_source, start=2):
        try:
            lignes_pretes.append((numero_ligne, ligne, convertir(ligne)))
        except (KeyError, TypeError, ValueError, InvalidOperation) as erreur:
            enregistrer_rejet(
                rejets, table, numero_ligne, ligne, str(erreur)
            )

    inserees = inserer_par_lots(
        conn,
        table,
        LIGNES_INSERTION[table],
        lignes_pretes,
        rejets,
    )
    duree = time.perf_counter() - debut
    resultat = ResultatTable(
        table=table,
        lues=len(lignes_source),
        inserees=inserees,
        rejetees=len(lignes_source) - inserees,
        duree_secondes=duree,
    )
    LOGGER.info(
        "%s : lues=%d, insérées=%d, rejetées=%d, durée=%.2fs",
        resultat.table,
        resultat.lues,
        resultat.inserees,
        resultat.rejetees,
        resultat.duree_secondes,
    )
    return resultat


def vider_tables(conn):
    for table in ("reservation", "materiel", "association", "site"):
        conn.execute(text(f"DELETE FROM {table}"))


def charger_sites(conn, rejets):
    return charger_table(conn, "site", FICHIER_SITES, convertir_site, rejets)


def charger_materiel(conn, rejets):
    return charger_table(
        conn, "materiel", FICHIER_MATERIEL, convertir_materiel, rejets
    )


def charger_associations(conn, rejets):
    return charger_table(
        conn,
        "association",
        FICHIER_ASSOCIATIONS,
        convertir_association,
        rejets,
    )


def charger_reservations(conn, rejets):
    return charger_table(
        conn,
        "reservation",
        FICHIER_RESERVATIONS,
        convertir_reservation,
        rejets,
    )


def ecrire_rejets(rejets):
    FICHIER_REJETS.parent.mkdir(parents=True, exist_ok=True)
    if not rejets:
        if FICHIER_REJETS.exists():
            FICHIER_REJETS.unlink()
        return

    colonnes = ("table", "ligne_csv", "donnees", "motif_rejet")
    with FICHIER_REJETS.open("w", encoding="utf-8", newline="") as fichier:
        writer = csv.DictWriter(fichier, fieldnames=colonnes)
        writer.writeheader()
        writer.writerows(rejets)


def main():
    configurer_journalisation()
    engine = creer_engine()
    rejets: list[dict[str, str]] = []
    resultats: list[ResultatTable] = []
    debut = time.perf_counter()

    try:
        with engine.begin() as conn:
            vider_tables(conn)
            resultats.append(charger_sites(conn, rejets))
            resultats.append(charger_materiel(conn, rejets))
            resultats.append(charger_associations(conn, rejets))
            resultats.append(charger_reservations(conn, rejets))
    finally:
        engine.dispose()

    ecrire_rejets(rejets)
    LOGGER.info(
        "Bilan : lues=%d, insérées=%d, rejetées=%d, durée=%.2fs",
        sum(resultat.lues for resultat in resultats),
        sum(resultat.inserees for resultat in resultats),
        len(rejets),
        time.perf_counter() - debut,
    )
    if rejets:
        LOGGER.warning(
            "%d ligne(s) refusée(s) ; détails dans %s",
            len(rejets),
            FICHIER_REJETS,
        )
    else:
        LOGGER.info("Aucune ligne rejetée.")


if __name__ == "__main__":
    main()
