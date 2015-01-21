# Earthquake-Notification-System
Earthquake Notification System designed using Cassandra database

# PROBLEME
- créer un cluster avec au moins 5 noeuds dans les 5 villes les plus peuplées du Japon
- charger les données dans le Cluster
- les coordonnées d'un tremblement de terre sont fournies
- couper les noeuds présents dans la zone à risque (ie à 500 km de l'épicentre)
- faire un INSERT avec au minimum 'date/heure de réception', 'numéro de téléphone', 'position lors du temblement de terre'
- donner le temps pour avoir prévenu 80% de la population


# IMPLEMENTATION
En deux parties, en utilisant Python et Cassandra

## Partie Python
- créer le tunnel entre Python et Cassandra
- insérer manuellement les coordonnées du tremblement de terre
- calculer la zone à risque et en envoyer les coordonnées à Cassandra

## Partie Cassandra
- charger la BDD .csv dans une table 'base'
- la trier par numero de téléphone + date
- créer une deuxième table avec pour clé 'numéro de téléphone' et pour champ 'position' seulement (comme cela la position se met à jour puisque la dernière insérée dans la base écrase les précédente) ou éventuellement un simple 'distance par rapport à la longtiude de la côte la plus proche'...etc 
- éventuellement créer un attribut 'distance par rapport à la côte' et trier sur cet attribut
- faire un insert en filtrant les numéros de téléphone qui sont dans la zone à risque + l'heure d'insert

## A résoudre:
- est-ce que l'INSERT se fait par rapport à l'ordre de la table insérée? Si non, problème
- dans la base initiale: combien de positions par personne? Combien de personnes?

## Améliorations possibles:
- filtrer directement la latitude et la longitude avec:
WHERE Lmin < latitude AND Lmax < latitude AND lmin < longitude AND lmax < longitude 
- voir si des clauses de ce WHERE sont inutiles (dépend de la géographie du pays)
