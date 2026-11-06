# TP d'évaluation — Pilotage du prêt de matériel aux associations (CCFL)

Cursus PRF Concepteur développeur en science de la donnée (Data Analyst 02)
Titre professionnel RNCP39103 — M2i Villeneuve d'Ascq

---

## Cadre du TP

**Objet :** 
Ce TP reprend, sur un nouveau cas métier, la chaîne travaillée lors du TP de révision des 23 et 24 septembre dernier : Python de base, pandas, qualité des données, modélisation, chargement PostgreSQL, SQL d'analyse. Il sert à mesurer votre progression depuis septembre. Le principe est le même : des étapes de difficulté croissante, chacune avec ses livrables et ses points de vérification.


**Durée :** 
Deux demi-journées, de 09h00 à 12h00 les 06/11/26 et 13/11/26.

**Modalités :** 
 - Travail **individuel, en autonomie complète** : aucun formateur n'est présent, aucune correction collective n'aura lieu. Une correction vous sera transmise une fois le tp terminé.
- Vous avancez à votre rythme, étape après étape, et vous déposez chaque étape dans votre dépôt git. 
- La documentation officielle des outils est autorisée.
Les assistants d'intelligence artificielle, les échanges de code entre stagiaires et la reprise d'un code qui n'est pas le vôtre sont interdits :
l'objectif est de mesurer votre niveau réel, pas celui de la salle.

**Outils requis :**

| Outil | Version attendue | Usage |
|---|---|---|
| Python | 3.12 | Toutes les étapes |
| pandas | 2.x ou 3.x | Étapes 2, 3, 5 |
| PostgreSQL | 14 ou supérieur | Étapes 4 à 7 |
| Un client SQL | pgAdmin, DBeaver ou `psql` | Étapes 4 à 6 |
| SQLAlchemy 2, psycopg | récents | Étapes 5 et 7 |
| Streamlit | récent | Étape 7 (bonus) |
| Un éditeur | VS Code ou PyCharm | Tout le TP |


**Données fournies :** 

Quatre fichiers CSV dans `data/`, décrits dans
`data/README-donnees.md`. Vous ne les modifiez jamais.

| Fichier | Lignes de données | Colonnes |
|---|---|---|
| `data/sites.csv` | 5 | `code_site`, `nom`, `commune`, `annee_ouverture`, `surface_m2` |
| `data/materiel.csv` | 367 | `id_materiel`, `reference`, `designation`, `categorie`, `etat`, `annee_achat`, `code_site`, `valeur_achat` |
| `data/associations.csv` | 210 | `id_association`, `nom`, `type_association`, `commune`, `code_postal`, `date_convention`, `code_site`, `convention_active` |
| `data/reservations.csv` | 4618 | `id_reservation`, `id_materiel`, `id_association`, `code_site`, `quantite`, `date_debut`, `date_fin_prevue`, `date_retour_reelle` |

Tous les chemins que vous écrivez dans votre code sont **relatifs à la racine du projet** (ex: `data/materiel.csv`), jamais absolus. Tous vos scripts se lancent depuis cette racine (ex: `etape01/exploration.py`).

**Organisation des étapes :** 

| Date | Étape |
|---|---|
| 06/11/26 | Installation, lecture de l'énoncé, création de l'arborescence | 
|  | Étape 1 — Python de base | 
|  | Étape 2 — pandas | 
|  | Étape 3 — Qualité des données | 
|  | Auto-évaluation et dépôt intermédiaire | 
| 13/11/26 | Étape 4 — Modélisation et DDL |
|  | Étape 5 — Chargement en base |
|  | Étape 6 — SQL d'analyse | 
|  | Étape 7 (BONUS) — Catague Streamlit | 
|  | Auto-évaluation et dépôt final | 

L'étape 7 (catalogue Streamlit) est un **bonus** : elle ne se tente que si
les six premières sont terminées et déposées.


**Arborescence de travail :**

Créez cette arborescence dès le début du tp et respectez-la : les noms de fichiers
attendus à chaque étape en dépendent.

```
tp-ccfl/
  data/                 (les 4 CSV fournis, jamais modifiés)
  etape01/
  etape02/
  etape03/
  etape04/
  etape05/
  etape06/
  etape07/
  sorties/              (tous les fichiers produits : CSV, rapports)
  auto-evaluation.md    (renseigne votre évaluation de votre avancement)
  README.md             (indique en dix lignes comment lancer chaque étape :
                        création de la base, variables d'env, ordre des scripts)
```

**Règles de rendu de tp :**

Vous devez créer un dépôt git **public** dans le quel vous déposez chaque étape de votre tp.

1. **À chaque étape terminée commitez immédiatement** et déposez dans votre dépôt git une archive `NOM_Prenom_etapeNN.zip` contenant votre dossier `tp-ccfl/` complet dans son état du moment. **L'heure des commits fait foi de l'avancement** et sera utilisée pour juger votre avancement. **Faites donc attention le faire à chaque étape.**
2. Créez en début de journée un fichier `auto-evaluation.md`que vous dans lequel vous renseignerez votre avancement à la fin de chaque étape réalisée. Il devra avoir la structure suivante : 

    ```
    # Auto-évaluation — NOM Prénom

    ## Étapes

    | Étape | État (terminée / partielle / non abordée) | Points de vérification obtenus | Ce qui a bloqué | Temps réel passé par étape |
    |---|---|---|---|---|
    | 1 | | | | |
    | 2 | | | | |
    | 3 | | | | |
    | 4 | | | | |
    | 5 | | | | |
    | 6 | | | | |
    | 7 | | | | |

    ## Ce que je sais faire mieux qu'en septembre
    (3 lignes)

    ## Ce qui me résiste encore
    (3 lignes)

    ```
    

3. **À 12h00 au plus tard** sur chacune des 2 demie-journées prévues pour le tp, déposez une archive `NOM_Prenom_final_ddmmyy.zip` avec votre dossier complet (remplacez ddmmyy par la date du jour) et le fichier `auto-evaluation.md` renseigné.
4. Si vous bloquez trop longtemps sur une étape, notez où vous en êtes dans `auto-evaluation.md` et passez à la suivante : les étapes 4 et 6 ne dépendent pas de la réussite complète de l'étape 3, et l'étape 5 peut s'appuyer sur des fichiers nettoyés partiellement.
5. Ne remplacez jamais votre code par un code qui n'est pas le vôtre, même après chaque demie-journée : les archives d'étape servent de référence à l'évaluation.
6. **Votre dépôt doit être propre :** pas d'environnement virtuel, pas de cache Python, pas
de mot de passe dans le code.


**Ce qui est évalué :** 

Les étapes que vous avez terminées, la justesse des résultats, la qualité du code (fonctions, noms, chemins relatifs, absence de secret en dur) et votre auto-évaluation. Une étape commencée et honnêtement décrite dans l'auto-évaluation vaut mieux qu'une étape recopiée.



---

## Contexte du tp et mise en situation

### Le commanditaire

La **Communauté de communes Flandre Lys (CCFL)** prête du matériel aux associations de ses communes : sonorisation, mobilier, barnums et tentes, éclairage, matériel de sécurité, matériel de cuisine. Le matériel est stocké dans cinq pôles de retrait (noms tels qu'ils figurent dans les fichiers, sans accent) :

| Code site | Nom | Commune | Ouverture | Surface |
|---|---|---|---|---|
| `POL-HAZ` | Pole technique d'Hazebrouck | Hazebrouck | 2009 | 1800 m2 |
| `POL-BAI` | Atelier municipal de Bailleul | Bailleul | 1996 | 950 m2 |
| `POL-MER` | Depot intercommunal de Merville | Merville | 2014 | 1200 m2 |
| `POL-EST` | Reserve d'Estaires | Estaires | 2001 | 600 m2 |
| `POL-NIE` | Magasin de Nieppe | Nieppe | 2018 | 450 m2 |

Chaque association signe une convention et se rattache à un pôle, où elle retire et rend le matériel. Le service est géré depuis un logiciel ancien, avec une saisie différente selon les pôles.

### La demande

Vous intervenez comme développeur data pour la direction des services techniques. La commande : **construire le socle de données qui permettra de piloter le service de prêt**, et répondre à quatre questions.

1. Comment évolue le nombre de réservations, mois par mois ?
2. Quels matériels sont les plus demandés, et dans quel pôle ?
3. Quelle part du matériel revient en retard, et où ?
4. Quelle est la valeur du parc stocké dans chaque pôle ?

### Le brief du directeur

Extraits de la réunion de cadrage avec M. Karim Vanhoutte, directeur des
services techniques.

> « Je sais que les données sont sales. Les pôles n'ont pas tous saisi les catégories de la même façon, il y a eu une reprise à la main en 2024, et personne n'a jamais vérifié. Je ne veux pas d'un chiffre propre qui cache la poussière : dites-moi ce que vous avez corrigé, ce que vous avez écarté, et pourquoi. »

> « Un matériel qui n'est pas encore rendu, ce n'est pas une erreur, c'est un prêt en cours. Si vous me les enlevez, mon stock disponible est faux. »

> « Je veux une base unique, des chiffres que je peux redemander par une requête, et à terme un écran pour que les agents des pôles consultent le parc sans passer par l'ancien logiciel. »

### Les contraintes

- **Lisibilité.** Un développeur à mi-temps reprendra votre outil une fois que vous l'aurez développé. Pensez à factoriser votre code, à donner des noms explicites et à créer un README.
- **Aucun secret en dur.** Les paramètres de connexion à la base doivent passer par des variables d'environnement.
- **Qualité des données.** Les quatre fichiers contiennent des anomalies réelles. Les détecter, les quantifier et décider de leur traitement fait partie du travail demandé.


---

## Étape 1 — Python de base : lire les données sans pandas


### Objectif

Lecture de fichiers CSV avec le module `csv`, listes et dictionnaires, fonctions qui renvoient une valeur, comptages avec `collections.Counter`, une classe simple, un bloc principal. Aucun import de pandas n'est autorisé à cette étape.

### Consignes

1. Créez le fichier `etape01/exploration.py`.
2. Écrivez une fonction `lire_csv(chemin)` qui ouvre un fichier CSV en UTF-8, le lit avec `csv.DictReader` et **renvoie** une liste de dictionnaires. Elle doit fonctionner pour les quatre fichiers sans modification.
3. Écrivez une fonction `compter_par(lignes, colonne)` qui renvoie un dictionnaire associant chaque valeur distincte de `colonne` à son nombre d'occurrences.
4. Écrivez une fonction `total_par(lignes, colonne_groupe, colonne_valeur)` qui renvoie, pour chaque valeur distincte de `colonne_groupe`, la somme des valeurs entières de `colonne_valeur`. Vous l'utiliserez pour les quantités réservées par site.
5. Écrivez une classe `Site` avec les attributs `code_site`, `nom`, `commune`, `annee_ouverture`, `surface_m2` (les deux derniers convertis en entiers à la construction). Ajoutez-lui :
   - une méthode `anciennete(annee_reference)` qui renvoie le nombre d'années écoulées depuis l'ouverture 
   - une méthode `__str__` qui renvoie une ligne lisible, par exemple `POL-HAZ - Pole technique d'Hazebrouck (Hazebrouck), 1800 m2`
6. Écrivez une fonction `reservations_en_cours(reservations)` qui renvoie la liste des réservations dont `date_retour_reelle` est vide. Une réservation sans date de retour réelle est un prêt **en cours**, ce n'est pas une erreur.
7. Dans un bloc `if __name__ == "__main__":`, appelez une fonction `main()` qui affiche, dans cet ordre et avec un libellé pour chaque valeur :
   - le nombre de lignes de chacun des quatre fichiers 
   - les cinq objets `Site` avec leur ancienneté calculée pour 2026 
   - le nombre de réservations par `code_site`, trié du plus grand au plus petit 
   - la quantité totale réservée par `code_site`, triée du plus grand au plus petit
   - le nombre de matériels par `etat`
   - le nombre de valeurs distinctes de `categorie` dans `materiel.csv`
   - le nombre de réservations en cours
8. Aucune valeur en dur dans les fonctions : les chemins sont des constantes déclarées en haut du module, relatives à la racine du projet.

### Livrable

`etape01/exploration.py`

### Points de vérification (à vérifiez vous-même)

- Le comptage des lignes doit donner exactement : 5 sites, 367 matériels, 210 associations, 4618 réservations
- Les réservations par site doivent donner `POL-HAZ` en tête avec 1869 réservations, et la somme des cinq valeurs vaut 4618
- Le nombre de matériels à l'état `bon` est 181
- Le nombre de valeurs distinctes de `categorie` est **supérieur à 6** alors que le service ne gère que six catégories. Notez-le sans le corriger : vous y reviendrez à l'étape 3
- `reservations_en_cours` doit renvoyer 72 réservations

### Indices

<details><summary>Indice 1</summary>

`csv.DictReader` renvoie un itérateur : enveloppez-le dans `list(...)` pour obtenir une liste. Ouvrez le fichier avec `open(chemin, encoding="utf-8", newline="")`.

</details>

<details><summary>Indice 2</summary>

Pour trier un dictionnaire de comptages du plus grand au plus petit : `Counter.most_common()`, ou `sorted(d.items(), key=lambda c: c[1], reverse=True)`.

</details>

<details><summary>Indice 3</summary>

Une chaîne vide est fausse en contexte booléen : `if not ligne["date_retour_reelle"].strip():` couvre la chaîne vide et la chaîne faite d'espaces. Attention à bien **appeler** `strip()` avec ses parenthèses.

</details>

---

## Étape 2 — Pandas : chargement, typage, agrégats et fusion

### Objectif

Mécanique de pandas : chargement, typage des dates et des nombres,exploration d'un DataFrame, tri, `groupby`, fusion avec `merge`, export CSV.

### Consignes

1. Créez le fichier `etape02/analyse_pandas.py`.
2. Chargez les quatre CSV dans `df_sites`, `df_materiel`, `df_associations`, `df_reservations`. Pour les réservations, convertissez `date_debut`, `date_fin_prevue` et `date_retour_reelle` en dates.
3. Affichez pour `df_materiel` et `df_reservations` : la forme (`shape`), le résultat de `info()`, et le nombre de valeurs manquantes par colonne.
4. Observez le type de la colonne `valeur_achat` dans `info()`. Si elle n'est pas numérique, trouvez pourquoi en regardant les valeurs, convertissez la colonne en nombre **dans le script** (sans modifier le CSV) et laissez un commentaire d'une ligne qui explique la cause.
5. Produisez par du code et affichez avec un libellé :
   - les 10 matériels les plus chers (`reference`, `designation`, `categorie`, `valeur_achat`), triés par valeur décroissante 
   - le nombre de matériels par `categorie`, trié du plus fréquent au moins fréquent 
   - le nombre de réservations et la quantité totale par `code_site`, en une seule opération `groupby`, triés par nombre de réservations décroissant.
6. Construisez `df_complet` en fusionnant `df_reservations` avec `df_materiel` sur `id_materiel`, puis avec `df_associations` sur `id_association`, en jointure `left` depuis les réservations. Affichez le nombre de lignes de `df_complet` et le nombre de lignes sans matériel correspondant.
7. À partir de `df_complet`, produisez le **top 10 des matériels les plus réservés** (`id_materiel`, `designation`, nombre de réservations) et exportez-le dans `sorties/top10_materiel.csv`, sans index, en UTF-8.
8. Le script ne doit produire aucun avertissement `SettingWithCopyWarning`.

### Livrable

`etape02/analyse_pandas.py` et `sorties/top10_materiel.csv`

### Points de vérification (à vérifiez vous-même)

- `df_reservations.shape` doit donner `(4618, 8)` et `df_materiel.shape` `(367, 8)`.
- Après conversion, les trois colonnes de dates apparaissent en `datetime64` dans `info()`, et `valeur_achat` en `float64`.
- Le nombre de valeurs manquantes de `date_retour_reelle` doit donner 72, comme à l'étape 1.
- Exactement 21 lignes de `df_complet` n'ont pas de matériel correspondant. Notez ce chiffre, vous le réutiliserez à l'étape 3.
- Comparez le nombre de lignes de `df_complet` au nombre de réservations. S'ils diffèrent, la fusion a créé des lignes : cherchez pourquoi dans `df_materiel` avant de faire le top 10.
- Le matériel en tête du top 10 totalise **48** réservations. Si vous obtenez un nombre nettement supérieur, le point précédent n'est pas réglé.

### Indices

<details><summary>Indice 1</summary>

`pd.to_numeric(serie.str.replace(",", "."), errors="coerce")` convertit une colonne de nombres écrits avec une virgule décimale ; les valeurs vides deviennent `NaN`.

</details>

<details><summary>Indice 2</summary>

Pour deux agrégats en une opération : `df.groupby("code_site").agg(nb=("id_reservation", "size"),
quantite=("quantite", "sum"))`.

</details>

<details><summary>Indice 3</summary>

Après un `merge(how="left")`, les lignes sans correspondance ont des valeurs manquantes dans les colonnes venues de la droite : `df_complet["designation"].isna().sum()`. Si la table de droite contient des lignes en double, chaque réservation concernée est dupliquée : `drop_duplicates()` sur la table de droite avant la fusion.

</details>

---

## Étape 3 — Qualité des données : détecter, quantifier, décider

### Objectif

Audit de qualité complet sur les trois tables métier, quantification de chaque anomalie, décision argumentée, fichiers nettoyés et rapport généré.

### Consignes

1. Créez le fichier `etape03/qualite.py`.
2. **Détectez et quantifiez** les catégories d'anomalies suivantes. Pour chacune, le code produit le nombre de lignes concernées et un échantillon de 3 lignes au maximum.

   Sur `materiel.csv` :
   - lignes en doublon strict
   - `annee_achat` vide
   - `annee_achat` postérieure à l'année courante
   - `valeur_achat` vide 
   - `categorie` écrite intégralement en majuscules
   - `categorie` avec des espaces parasites en début ou en fin
   - `valeur_achat` écrite avec une virgule décimale

   Sur `associations.csv` :
   - `code_postal` vide
   - `type_association` valant `inconnu`
   - `date_convention` au format `JJ/MM/AAAA`

   Sur `reservations.csv` :
   - lignes en doublon strict ;
   - `id_materiel` ne correspondant à aucun matériel
   - `date_retour_reelle` antérieure à `date_debut`
   - `quantite` égale à zéro

3. **Piège.** Les lignes dont `date_retour_reelle` est vide ne sont **pas** une anomalie : ce sont les prêts en cours. Le rapport les mentionne comme cas métier normal, avec leur nombre, sans les compter comme défaut.
4. **Décidez d'un traitement** pour chaque anomalie : suppression de la ligne, correction automatique, mise à valeur manquante, ou conservation avec signalement. Chaque décision est justifiée en une à deux phrases. Une valeur manquante se conserve, elle ne se remplace ni par zéro ni par une valeur inventée.
5. **Produisez les fichiers nettoyés** dans `sorties/` : `materiel_propre.csv`, `associations_propre.csv`, `reservations_propre.csv` avec les règles suivantes :
   - doublons stricts supprimés, une occurrence conservée
   - `categorie` ramenée à six libellés homogènes
   - `valeur_achat` numérique, les valeurs vides restant vides
   - années d'achat impossibles traitées selon votre décision documentée
   - `date_convention` toutes au format ISO
   - réservations pointant vers un matériel inexistant écartées (elles casseraient la clé étrangère à l'étape 4) 
   - réservations à la chronologie impossible et réservations de quantité nulle écartées
6. **Rédigez le rapport** `sorties/rapport_qualite.md`, généré par le script :
   - un tableau récapitulatif avec, par anomalie : fichier, colonne, description, nombre de lignes, part en pourcentage, traitement retenu
   - une section par fichier avec le nombre de lignes avant et après
   - le nombre de prêts en cours avant et après nettoyage, et l'explication de l'écart s'il y en a un
   - une section « points d'attention pour la direction » de 5 à 10 lignes en français courant, sans jargon

### Livrable

`etape03/qualite.py`, `sorties/materiel_propre.csv`,
`sorties/associations_propre.csv`, `sorties/reservations_propre.csv`,
`sorties/rapport_qualite.md`

### Points de vérification (à vérifiez vous-même)

- Le rapport recense **quatorze** catégories, de a à n. Si vous en avez
  plus, vous avez compté les prêts en cours comme défaut.
- Sur `materiel.csv`, chaque anomalie touche **moins de 4 %** du fichier.
- Sur `reservations.csv`, le nombre de lignes à matériel inexistant est
  **exactement** celui trouvé à l'étape 2 après la fusion.
- `sorties/materiel_propre.csv` contient 360 lignes et exactement 6
  catégories distinctes.
- `sorties/reservations_propre.csv` contient **moins de 4618 et plus de
  4500** lignes. Sous 4500, vous avez probablement supprimé les prêts en
  cours.
- Le nombre de prêts en cours après nettoyage est **inférieur d'une unité** à
  celui d'avant. Si vous retrouvez le même nombre, une catégorie
  d'anomalie n'a pas été appliquée ; trouvez laquelle et expliquez l'écart
  dans le rapport.

### Indices

<details><summary>Indice 1</summary>

`df.duplicated()` marque les lignes identiques sur toutes les colonnes en laissant la première à `False.
`df.drop_duplicates()` produit la version nettoyée.

</details>

<details><summary>Indice 2</summary>

Pour une catégorie en majuscules : `s.str.strip().str.isupper()`. Pour ramener à un libellé homogène : `s.str.strip().str.capitalize()`, puis vérifiez avec `nunique()` que vous retombez sur six valeurs.

</details>

<details><summary>Indice 3</summary>

Dates mélangées en deux passes : `pd.to_datetime(s, format="%Y-%m-%d", errors="coerce")` puis `pd.to_datetime(s, format="%d/%m/%Y", errors="coerce")` là où la première passe a échoué, combinées avec `fillna`.

</details>

<details><summary>Indice 4</summary>

Orphelins : `~df_reservations["id_materiel"].isin(df_materiel_propre["id_materiel"])`. Vérifiez que les deux colonnes ont le même type.

</details>
