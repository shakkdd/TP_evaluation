from pathlib import Path
import pandas as pd

df_sites = pd.read_csv("data/sites.csv")
df_materiel = pd.read_csv("data/materiel.csv")
df_associations = pd.read_csv("data/associations.csv")
df_reservations = pd.read_csv(
    "data/reservations.csv",
    parse_dates=["date_debut", "date_fin_prevue", "date_retour_reelle"],
)

print(df_materiel.shape)
print(df_materiel.info())
print(df_materiel.isna().sum()) 

print(df_reservations.shape)
print(df_reservations.info())
print(df_reservations.isna().sum())

#la colonne n'est pas numérique car certaines valeurs sont vides
#et d'autres mal écrits, il y a une "," à la place d'un "."
#qui convertit automatiquement la valeur en str et non en float
#on va donc appliquer une fonction pour convetir le tout en float
#elle reçoit chaque cellule, remplace la virgule décimale, 
#convertit la valeur en float 
#et préserve les valeurs manquantes sous forme de NaN
def correct_float(valeur):
    if pd.isna(valeur):
        return float("nan")
    return float(str(valeur).replace(",", "."))


df_materiel["valeur_achat"] = df_materiel["valeur_achat"].apply(correct_float)

#print(df_materiel.info())

top_10_materiels = df_materiel.nlargest(10, "valeur_achat")[
    ["reference", "designation", "categorie", "valeur_achat"]
]
print("Les 10 matériels les plus chers :\n",top_10_materiels)

materiels_par_categorie = (
    df_materiel["categorie"].value_counts().rename_axis("categorie").reset_index(name="nombre")
)
print("Nombre de matériels par catégorie :\n",materiels_par_categorie)

reservations_par_site = (
    df_reservations.groupby("code_site")
    .agg(
        nombre_reservations=("id_reservation", "count"),
        quantite_totale=("quantite", "sum"),
    )
    .sort_values("nombre_reservations", ascending=False).reset_index()
)
print("Nombre de réservations et quantité totale par site :\n",reservations_par_site)

df_complet = (
    df_reservations.merge(
        df_materiel,
        on="id_materiel",
        how="left",
        indicator=True,
    )
    .merge(
        df_associations,
        on="id_association",
        how="left",
    )
)
nombre_sans_materiel = df_complet["reference"].isna().sum()

print(f"Nombre de lignes de df_complet : {len(df_complet)}")
print(f"Nombre de lignes sans matériel correspondant : {nombre_sans_materiel}")

top10_materiel = (
    df_complet.groupby(["id_materiel", "designation"], as_index=False)
    .agg(
        nombre_reservations=("id_reservation", "nunique")
    )
    .sort_values("nombre_reservations", ascending=False)
    .head(10)
)
print("Top 10 des matériels les plus réservés :\n", top10_materiel)
print(top10_materiel)

fichier_top10 = Path("sorties/top10_materiel.csv")
fichier_top10.parent.mkdir(parents=True, exist_ok=True)
top10_materiel.to_csv(fichier_top10, index=False, encoding="utf-8")
