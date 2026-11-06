# Jeu de données — Prêt de matériel aux associations (CCFL)

> Document remis aux apprenants avec l'énoncé du TP.

La Communauté de communes Flandre Lys (CCFL) prête du matériel (sonorisation,
mobilier, barnums, éclairage, sécurité, cuisine) aux associations de son
territoire depuis cinq pôles de retrait. Les quatre fichiers sont des
extractions brutes de l'outil de gestion : ils contiennent des anomalies
réelles, que vous aurez à détecter, quantifier et traiter. Vous ne les
modifiez jamais : vous les lisez, et vous écrivez vos résultats dans
`sorties/`.

Tous les fichiers : séparateur `,`, encodage UTF-8, une ligne d'en-tête.

## sites.csv (5 lignes)

| Colonne | Type attendu | Description |
|---|---|---|
| code_site | texte, 7 caractères | Identifiant du pôle (`POL-HAZ`, `POL-BAI`, `POL-MER`, `POL-EST`, `POL-NIE`) |
| nom | texte | Nom du pôle |
| commune | texte | Commune |
| annee_ouverture | entier | Année d'ouverture |
| surface_m2 | entier | Surface de stockage |

## materiel.csv (367 lignes)

| Colonne | Type attendu | Description |
|---|---|---|
| id_materiel | entier | Identifiant |
| reference | texte | Référence d'inventaire `MAT-0001` |
| designation | texte | Désignation |
| categorie | texte | Six catégories attendues : Sonorisation, Mobilier, Tente et barnum, Eclairage, Securite, Cuisine |
| etat | texte | `neuf`, `bon`, `moyen`, `a reviser` |
| annee_achat | entier | Année d'achat |
| code_site | texte | Pôle où le matériel est stocké |
| valeur_achat | décimal | Valeur d'achat en euros |

## associations.csv (210 lignes)

| Colonne | Type attendu | Description |
|---|---|---|
| id_association | entier | Identifiant |
| nom | texte | Nom de l'association |
| type_association | texte | `sportive`, `culturelle`, `sociale`, `festive`, `scolaire` |
| commune | texte | Commune du siège |
| code_postal | texte | Code postal |
| date_convention | date ISO `AAAA-MM-JJ` | Date de signature de la convention de prêt |
| code_site | texte | Pôle de rattachement de l'association |
| convention_active | texte | `oui` / `non` |

## reservations.csv (4 618 lignes)

| Colonne | Type attendu | Description |
|---|---|---|
| id_reservation | texte, 7 caractères | Identifiant `R250000` |
| id_materiel | entier | Matériel réservé |
| id_association | entier | Association emprunteuse |
| code_site | texte | Pôle où le retrait a lieu (celui de l'association) |
| quantite | entier | Quantité empruntée |
| date_debut | date ISO | Début du prêt |
| date_fin_prevue | date ISO | Date de retour prévue |
| date_retour_reelle | date ISO ou vide | Date de retour effective ; **vide tant que le matériel n'est pas rendu** |

Période couverte : octobre 2025 à octobre 2026. Une réservation sans date de
retour réelle est un prêt en cours : c'est une situation normale, pas une
erreur.
