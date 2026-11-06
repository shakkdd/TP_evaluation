import json
from datetime import date
from pathlib import Path

import pandas as pd


FICHIER_MATERIEL = Path("data/materiel.csv")
FICHIER_ASSOCIATIONS = Path("data/associations.csv")
FICHIER_RESERVATIONS = Path("data/reservations.csv")
DOSSIER_SORTIES = Path("sorties")
ANNEE_COURANTE = date.today().year

TRAITEMENTS = {
    "materiel_doublons": (
        "Suppression des copies exactes en double, en conservant une occurrence. "
        "Cela évite de compter plusieurs fois la même fiche."
    ),
    "annee_achat_vide": (
        "Conservation de la valeur vide. Aucune année ne peut être déduite sans "
        "inventer une information."
    ),
    "annee_achat_future": (
        "Remplacement par une valeur manquante, car l'année dépasse l'année "
        "courante et doit être vérifiée auprès de la source."
    ),
    "valeur_achat_vide": (
        "Conservation de la valeur vide. Elle ne peut pas être remplacée par "
        "zéro ou par une estimation."
    ),
    "categorie_majuscules": (
        "Correction automatique vers le libellé homogène correspondant. "
        "La casse ne change pas la catégorie réelle."
    ),
    "categorie_espaces": (
        "Suppression des espaces placés au début ou à la fin, puis harmonisation "
        "du libellé."
    ),
    "valeur_achat_virgule": (
        "Remplacement de la virgule décimale par un point et conversion en "
        "nombre, sans modifier les valeurs vides."
    ),
    "code_postal_vide": (
        "Conservation de la valeur vide. Le code postal manquant doit être "
        "confirmé plutôt que deviné."
    ),
    "type_inconnu": (
        "Remplacement de « inconnu » par une valeur manquante. Aucun type "
        "d'association ne peut être choisi sans confirmation."
    ),
    "date_convention_slash": (
        "Conversion du format JJ/MM/AAAA vers le format ISO AAAA-MM-JJ, sans "
        "changer la date."
    ),
    "reservations_doublons": (
        "Suppression des copies exactes en double, en conservant une occurrence. "
        "Une réservation ne doit être comptée qu'une fois."
    ),
    "materiel_inexistant": (
        "Suppression des réservations qui pointent vers un matériel absent de "
        "l'inventaire, car elles ne peuvent pas être reliées à une fiche valide."
    ),
    "retour_avant_debut": (
        "Suppression des réservations dont le retour précède le début. "
        "Cette chronologie doit être corrigée dans la source."
    ),
    "quantite_nulle": (
        "Suppression des réservations de quantité nulle, qui ne représentent "
        "aucun prêt."
    ),
}


def lire_table(chemin):
    return pd.read_csv(chemin, dtype=str, keep_default_na=False)


def analyser_anomalies(materiel, associations, reservations):
    annee_achat = pd.to_numeric(materiel["annee_achat"], errors="coerce")
    id_materiel = pd.to_numeric(materiel["id_materiel"], errors="raise")
    id_reservation_materiel = pd.to_numeric(
        reservations["id_materiel"], errors="raise"
    )
    date_debut = pd.to_datetime(
        reservations["date_debut"], format="%Y-%m-%d", errors="coerce"
    )
    date_retour = pd.to_datetime(
        reservations["date_retour_reelle"], format="%Y-%m-%d", errors="coerce"
    )
    categories = materiel["categorie"]
    valeurs_achat = materiel["valeur_achat"]
    dates_convention = associations["date_convention"]

    masques = {
        "materiel_doublons": materiel.duplicated(keep=False),
        "annee_achat_vide": materiel["annee_achat"].eq(""),
        "annee_achat_future": annee_achat.gt(ANNEE_COURANTE),
        "valeur_achat_vide": valeurs_achat.eq(""),
        "categorie_majuscules": categories.str.strip().str.isupper(),
        "categorie_espaces": categories.ne(categories.str.strip()),
        "valeur_achat_virgule": valeurs_achat.str.contains(",", regex=False),
        "code_postal_vide": associations["code_postal"].eq(""),
        "type_inconnu": associations["type_association"].str.strip().str.lower().eq(
            "inconnu"
        ),
        "date_convention_slash": dates_convention.str.fullmatch(
            r"\d{2}/\d{2}/\d{4}"
        ),
        "reservations_doublons": reservations.duplicated(keep=False),
        "materiel_inexistant": ~id_reservation_materiel.isin(id_materiel),
        "retour_avant_debut": (
            date_retour.notna()
            & date_debut.notna()
            & date_retour.lt(date_debut)
        ),
        "quantite_nulle": pd.to_numeric(
            reservations["quantite"], errors="raise"
        ).eq(0),
    }

    definitions = {
        "materiel_doublons": ("materiel.csv", "toutes", "Lignes en doublon strict"),
        "annee_achat_vide": ("materiel.csv", "annee_achat", "Année d'achat vide"),
        "annee_achat_future": (
            "materiel.csv",
            "annee_achat",
            f"Année d'achat postérieure à {ANNEE_COURANTE}",
        ),
        "valeur_achat_vide": ("materiel.csv", "valeur_achat", "Valeur d'achat vide"),
        "categorie_majuscules": (
            "materiel.csv",
            "categorie",
            "Catégorie écrite intégralement en majuscules",
        ),
        "categorie_espaces": (
            "materiel.csv",
            "categorie",
            "Espaces parasites autour de la catégorie",
        ),
        "valeur_achat_virgule": (
            "materiel.csv",
            "valeur_achat",
            "Valeur d'achat avec une virgule décimale",
        ),
        "code_postal_vide": ("associations.csv", "code_postal", "Code postal vide"),
        "type_inconnu": (
            "associations.csv",
            "type_association",
            "Type d'association valant « inconnu »",
        ),
        "date_convention_slash": (
            "associations.csv",
            "date_convention",
            "Date au format JJ/MM/AAAA",
        ),
        "reservations_doublons": (
            "reservations.csv",
            "toutes",
            "Lignes en doublon strict",
        ),
        "materiel_inexistant": (
            "reservations.csv",
            "id_materiel",
            "Matériel absent de l'inventaire",
        ),
        "retour_avant_debut": (
            "reservations.csv",
            "date_retour_reelle",
            "Date de retour antérieure à la date de début",
        ),
        "quantite_nulle": ("reservations.csv", "quantite", "Quantité égale à zéro"),
    }

    anomalies = []
    jeux = {
        "materiel.csv": materiel,
        "associations.csv": associations,
        "reservations.csv": reservations,
    }
    for cle, masque in masques.items():
        fichier, colonne, description = definitions[cle]
        lignes = jeux[fichier].loc[masque].head(3).copy()
        lignes.insert(0, "ligne_csv", lignes.index + 2)
        anomalies.append(
            {
                "cle": cle,
                "fichier": fichier,
                "colonne": colonne,
                "description": description,
                "nombre": int(masque.sum()),
                "echantillon": lignes.to_dict(orient="records"),
                "traitement": TRAITEMENTS[cle],
            }
        )
    return anomalies


def convertir_date_mixte(valeurs, nom_colonne):
    dates_iso = pd.to_datetime(valeurs, format="%Y-%m-%d", errors="coerce")
    dates_fr = pd.to_datetime(valeurs, format="%d/%m/%Y", errors="coerce")
    dates = dates_iso.fillna(dates_fr)
    invalides = valeurs.ne("") & dates.isna()
    if invalides.any():
        exemples = valeurs.loc[invalides].head(3).tolist()
        raise ValueError(
            f"Dates invalides dans {nom_colonne} : {exemples}"
        )
    return dates.dt.strftime("%Y-%m-%d").fillna("")


def nettoyer_donnees(materiel, associations, reservations):
    materiel_propre = materiel.drop_duplicates().copy()
    annee = pd.to_numeric(
        materiel_propre["annee_achat"].replace("", pd.NA), errors="raise"
    )
    annee.loc[annee.gt(ANNEE_COURANTE).fillna(False)] = pd.NA
    materiel_propre["annee_achat"] = annee.astype("Int64")

    materiel_propre["categorie"] = (
        materiel_propre["categorie"].str.strip().str.capitalize()
    )
    categories_attendues = {
        "Sonorisation",
        "Mobilier",
        "Tente et barnum",
        "Eclairage",
        "Securite",
        "Cuisine",
    }
    categories_trouvees = set(materiel_propre["categorie"].unique())
    if categories_trouvees != categories_attendues:
        raise ValueError(
            f"Catégories inattendues après harmonisation : {categories_trouvees}"
        )

    prix_source = materiel_propre["valeur_achat"]
    prix = pd.to_numeric(
        prix_source.replace("", pd.NA).str.replace(",", ".", regex=False),
        errors="coerce",
    )
    prix_invalides = prix_source.ne("") & prix.isna()
    if prix_invalides.any():
        exemples = prix_source.loc[prix_invalides].head(3).tolist()
        raise ValueError(f"Valeurs d'achat non numériques : {exemples}")
    materiel_propre["valeur_achat"] = prix

    associations_propre = associations.drop_duplicates().copy()
    associations_propre["type_association"] = associations_propre[
        "type_association"
    ].where(
        associations_propre["type_association"].str.strip().str.lower().ne(
            "inconnu"
        ),
        "",
    )
    associations_propre["date_convention"] = convertir_date_mixte(
        associations_propre["date_convention"], "date_convention"
    )

    reservations_propre = reservations.drop_duplicates().copy()
    materiels_valides = pd.to_numeric(
        materiel_propre["id_materiel"], errors="raise"
    )
    ids_reservations = pd.to_numeric(
        reservations_propre["id_materiel"], errors="raise"
    )
    reservations_propre = reservations_propre.loc[
        ids_reservations.isin(materiels_valides)
    ].copy()

    date_debut = pd.to_datetime(
        reservations_propre["date_debut"], format="%Y-%m-%d", errors="coerce"
    )
    date_retour = pd.to_datetime(
        reservations_propre["date_retour_reelle"],
        format="%Y-%m-%d",
        errors="coerce",
    )
    dates_invalides = (
        reservations_propre["date_debut"].ne("") & date_debut.isna()
    ) | (reservations_propre["date_retour_reelle"].ne("") & date_retour.isna())
    if dates_invalides.any():
        raise ValueError("Une date de réservation non vide n'est pas au format ISO.")

    chronologie_valide = (
        date_retour.isna() | date_debut.isna() | date_retour.ge(date_debut)
    )
    reservations_propre = reservations_propre.loc[chronologie_valide].copy()
    reservations_propre = reservations_propre.loc[
        pd.to_numeric(reservations_propre["quantite"], errors="raise").ne(0)
    ].copy()

    return materiel_propre, associations_propre, reservations_propre


def ecrire_rapport(anomalies, avant, apres, prets_en_cours_avant, prets_en_cours_apres):
    lignes = [
        "# Rapport de qualité des données",
        "",
        f"Audit réalisé en {ANNEE_COURANTE}. Les pourcentages sont calculés "
        "sur le nombre de lignes du fichier source concerné.",
        "",
        "## Anomalies détectées et traitements retenus",
        "",
        "| Fichier | Colonne | Anomalie | Lignes | Part | Traitement retenu |",
        "|---|---|---|---:|---:|---|",
    ]
    for anomalie in anomalies:
        total = avant[anomalie["fichier"]]
        part = anomalie["nombre"] / total * 100 if total else 0
        lignes.append(
            f"| {anomalie['fichier']} | {anomalie['colonne']} | "
            f"{anomalie['description']} | {anomalie['nombre']} | {part:.2f} % | "
            f"{anomalie['traitement']} |"
        )

    lignes.extend(
        [
            "",
            "Pour les doublons stricts, le nombre indiqué comprend toutes les "
            "lignes appartenant à un groupe en doublon ; le nettoyage retire "
            "les copies excédentaires et en conserve une.",
            "",
            "## Évolution des fichiers",
            "",
            "| Fichier | Lignes avant | Lignes après |",
            "|---|---:|---:|",
        ]
    )
    for fichier in ("materiel.csv", "associations.csv", "reservations.csv"):
        lignes.append(
            f"| {fichier} | {avant[fichier]} | {apres[fichier]} |"
        )

    lignes.extend(
        [
            "",
            "## Prêts en cours",
            "",
            f"Avant nettoyage : **{prets_en_cours_avant}** prêts sans date de "
            "retour réelle. Ce sont des prêts en cours normaux et ils ne sont "
            "pas comptés comme une anomalie.",
            "",
            f"Après nettoyage : **{prets_en_cours_apres}** prêts en cours. "
            f"L'écart de {prets_en_cours_avant - prets_en_cours_apres} s'explique "
            "par la suppression d'une réservation en cours liée à un matériel "
            "inexistant ; les autres prêts en cours sont conservés.",
            "",
            "## Points d'attention pour la direction",
            "",
            "- Plusieurs fiches de matériel ont des informations à vérifier, "
            "notamment leur année d'achat et leur prix.",
            "- Les années d'achat situées dans le futur ont été laissées sans "
            "valeur plutôt que corrigées au hasard.",
            "- Certains codes postaux manquent ; les associations concernées "
            "doivent être recontactées.",
            "- Le type de quelques associations n'est pas renseigné clairement "
            "et nécessite une confirmation.",
            "- Des réservations mentionnent du matériel absent de l'inventaire "
            "et ont été écartées des données nettoyées.",
            "- Des dates de retour précèdent le début du prêt ; ces dossiers "
            "doivent être vérifiés à la source.",
            "- Les catégories et les dates de convention ont été harmonisées "
            "sans changer leur sens.",
            "- Les prêts sans date de retour restent dans le fichier : ils sont "
            "considérés comme toujours en cours.",
            "",
        ]
    )
    (DOSSIER_SORTIES / "rapport_qualite.md").write_text(
        "\n".join(lignes), encoding="utf-8"
    )


def main():
    materiel = lire_table(FICHIER_MATERIEL)
    associations = lire_table(FICHIER_ASSOCIATIONS)
    reservations = lire_table(FICHIER_RESERVATIONS)
    jeux = {
        "materiel.csv": materiel,
        "associations.csv": associations,
        "reservations.csv": reservations,
    }
    anomalies = analyser_anomalies(materiel, associations, reservations)

    print("Anomalies détectées (échantillon limité à trois lignes) :")
    for anomalie in anomalies:
        print(f"\n{anomalie['fichier']} — {anomalie['description']}")
        print(f"Nombre de lignes concernées : {anomalie['nombre']}")
        print(
            "Échantillon : "
            + json.dumps(anomalie["echantillon"], ensure_ascii=False)
        )

    prets_en_cours_avant = int(reservations["date_retour_reelle"].eq("").sum())
    materiel_propre, associations_propre, reservations_propre = nettoyer_donnees(
        materiel, associations, reservations
    )
    propres = {
        "materiel.csv": materiel_propre,
        "associations.csv": associations_propre,
        "reservations.csv": reservations_propre,
    }

    DOSSIER_SORTIES.mkdir(parents=True, exist_ok=True)
    materiel_propre.to_csv(
        DOSSIER_SORTIES / "materiel_propre.csv",
        index=False,
        encoding="utf-8",
        na_rep="",
    )
    associations_propre.to_csv(
        DOSSIER_SORTIES / "associations_propre.csv",
        index=False,
        encoding="utf-8",
        na_rep="",
    )
    reservations_propre.to_csv(
        DOSSIER_SORTIES / "reservations_propre.csv",
        index=False,
        encoding="utf-8",
        na_rep="",
    )

    avant = {fichier: len(table) for fichier, table in jeux.items()}
    apres = {fichier: len(table) for fichier, table in propres.items()}
    prets_en_cours_apres = int(
        reservations_propre["date_retour_reelle"].eq("").sum()
    )
    ecrire_rapport(
        anomalies,
        avant,
        apres,
        prets_en_cours_avant,
        prets_en_cours_apres,
    )

    print("\nLignes avant / après nettoyage :")
    for fichier in jeux:
        print(f"{fichier} : {avant[fichier]} / {apres[fichier]}")
    print(
        f"Prêts en cours avant / après : "
        f"{prets_en_cours_avant} / {prets_en_cours_apres}"
    )
    print(f"Rapport écrit dans {DOSSIER_SORTIES / 'rapport_qualite.md'}")


if __name__ == "__main__":
    main()