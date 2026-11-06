# Rapport de qualité des données

Audit réalisé en 2026. Les pourcentages sont calculés sur le nombre de lignes du fichier source concerné.

## Anomalies détectées et traitements retenus

| Fichier | Colonne | Anomalie | Lignes | Part | Traitement retenu |
|---|---|---|---:|---:|---|
| materiel.csv | toutes | Lignes en doublon strict | 14 | 3.81 % | Suppression des copies exactes en double, en conservant une occurrence. Cela évite de compter plusieurs fois la même fiche. |
| materiel.csv | annee_achat | Année d'achat vide | 9 | 2.45 % | Conservation de la valeur vide. Aucune année ne peut être déduite sans inventer une information. |
| materiel.csv | annee_achat | Année d'achat postérieure à 2026 | 5 | 1.36 % | Remplacement par une valeur manquante, car l'année dépasse l'année courante et doit être vérifiée auprès de la source. |
| materiel.csv | valeur_achat | Valeur d'achat vide | 11 | 3.00 % | Conservation de la valeur vide. Elle ne peut pas être remplacée par zéro ou par une estimation. |
| materiel.csv | categorie | Catégorie écrite intégralement en majuscules | 6 | 1.63 % | Correction automatique vers le libellé homogène correspondant. La casse ne change pas la catégorie réelle. |
| materiel.csv | categorie | Espaces parasites autour de la catégorie | 5 | 1.36 % | Suppression des espaces placés au début ou à la fin, puis harmonisation du libellé. |
| materiel.csv | valeur_achat | Valeur d'achat avec une virgule décimale | 5 | 1.36 % | Remplacement de la virgule décimale par un point et conversion en nombre, sans modifier les valeurs vides. |
| associations.csv | code_postal | Code postal vide | 9 | 4.29 % | Conservation de la valeur vide. Le code postal manquant doit être confirmé plutôt que deviné. |
| associations.csv | type_association | Type d'association valant « inconnu » | 7 | 3.33 % | Remplacement de « inconnu » par une valeur manquante. Aucun type d'association ne peut être choisi sans confirmation. |
| associations.csv | date_convention | Date au format JJ/MM/AAAA | 6 | 2.86 % | Conversion du format JJ/MM/AAAA vers le format ISO AAAA-MM-JJ, sans changer la date. |
| reservations.csv | toutes | Lignes en doublon strict | 36 | 0.78 % | Suppression des copies exactes en double, en conservant une occurrence. Une réservation ne doit être comptée qu'une fois. |
| reservations.csv | id_materiel | Matériel absent de l'inventaire | 21 | 0.45 % | Suppression des réservations qui pointent vers un matériel absent de l'inventaire, car elles ne peuvent pas être reliées à une fiche valide. |
| reservations.csv | date_retour_reelle | Date de retour antérieure à la date de début | 15 | 0.32 % | Suppression des réservations dont le retour précède le début. Cette chronologie doit être corrigée dans la source. |
| reservations.csv | quantite | Quantité égale à zéro | 6 | 0.13 % | Suppression des réservations de quantité nulle, qui ne représentent aucun prêt. |

Pour les doublons stricts, le nombre indiqué comprend toutes les lignes appartenant à un groupe en doublon ; le nettoyage retire les copies excédentaires et en conserve une.

## Évolution des fichiers

| Fichier | Lignes avant | Lignes après |
|---|---:|---:|
| materiel.csv | 367 | 360 |
| associations.csv | 210 | 210 |
| reservations.csv | 4618 | 4560 |

## Prêts en cours

Avant nettoyage : **72** prêts sans date de retour réelle. Ce sont des prêts en cours normaux et ils ne sont pas comptés comme une anomalie.

Après nettoyage : **71** prêts en cours. L'écart de 1 s'explique par la suppression d'une réservation en cours liée à un matériel inexistant ; les autres prêts en cours sont conservés.

## Points d'attention pour la direction

- Plusieurs fiches de matériel ont des informations à vérifier, notamment leur année d'achat et leur prix.
- Les années d'achat situées dans le futur ont été laissées sans valeur plutôt que corrigées au hasard.
- Certains codes postaux manquent ; les associations concernées doivent être recontactées.
- Le type de quelques associations n'est pas renseigné clairement et nécessite une confirmation.
- Des réservations mentionnent du matériel absent de l'inventaire et ont été écartées des données nettoyées.
- Des dates de retour précèdent le début du prêt ; ces dossiers doivent être vérifiés à la source.
- Les catégories et les dates de convention ont été harmonisées sans changer leur sens.
- Les prêts sans date de retour restent dans le fichier : ils sont considérés comme toujours en cours.
