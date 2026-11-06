import csv

FICHIER_SITES = "data/sites.csv"
FICHIER_MATERIEL = "data/materiel.csv"
FICHIER_ASSOCIATIONS = "data/associations.csv"
FICHIER_RESERVATIONS = "data/reservations.csv"
ANNEE_REFERENCE = 2026


def lire_csv(chemin):
    with open(chemin, encoding="utf-8", newline="") as fichier:
        return list(csv.DictReader(fichier))


def compter_par(lignes, colonne):
    comptes = {}
    for ligne in lignes:
        valeur = ligne[colonne]
        comptes[valeur] = comptes.get(valeur, 0) + 1
    return comptes


def total_par(lignes, colonne_groupe, colonne_valeur):
    totaux = {}
    for ligne in lignes:
        groupe = ligne[colonne_groupe]
        totaux[groupe] = totaux.get(groupe, 0) + int(ligne[colonne_valeur])
    return totaux


class Site:
    def __init__(self, code_site, nom, commune, annee_ouverture, surface_m2):
        self.code_site = code_site
        self.nom = nom
        self.commune = commune
        self.annee_ouverture = int(annee_ouverture)
        self.surface_m2 = int(surface_m2)

    def anciennete(self, annee_reference):
        return annee_reference - self.annee_ouverture

    def __str__(self):
        return (
            f"{self.code_site} - {self.nom} ({self.commune}), "
            f"{self.surface_m2} m2"
        )


def reservations_en_cours(reservations):
    return [
        reservation
        for reservation in reservations
        if reservation["date_retour_reelle"] == ""
    ]


def afficher_par_ordre_decroissant(titre, valeurs):
    print(titre)
    for valeur, nombre in sorted(
        valeurs.items(), key=lambda element: element[1], reverse=True
    ):
        print(f"  {valeur} : {nombre}")


def main():
    sites_lignes = lire_csv(FICHIER_SITES)
    materiel = lire_csv(FICHIER_MATERIEL)
    associations = lire_csv(FICHIER_ASSOCIATIONS)
    reservations = lire_csv(FICHIER_RESERVATIONS)

    print(f"Nombre de lignes dans sites.csv : {len(sites_lignes)}")
    print(f"Nombre de lignes dans materiel.csv : {len(materiel)}")
    print(f"Nombre de lignes dans associations.csv : {len(associations)}")
    print(f"Nombre de lignes dans reservations.csv : {len(reservations)}")

    print("Sites et ancienneté en 2026 :")
    for ligne in sites_lignes:
        site = Site(**ligne)
        print(f"  {site} - ancienneté : {site.anciennete(ANNEE_REFERENCE)} ans")

    afficher_par_ordre_decroissant(
        f"Nombre de réservations par code_site : {compter_par(reservations, "code_site")}",
    )
    afficher_par_ordre_decroissant(
        f"Quantité totale réservée par code_site : {total_par(reservations, "code_site", "quantite")}",
    )
    afficher_par_ordre_decroissant(
        f"Nombre de matériels par état : {compter_par(materiel, "etat")}",
    )
    print(
        f"Nombre de catégories distinctes dans materiel.csv : {len(compter_par(materiel, 'categorie'))}"
    )
    print(
        f"Nombre de réservations en cours : {len(reservations_en_cours(reservations))}"
    )


if __name__ == "__main__":
    main()
