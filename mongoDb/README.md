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
- dans la base initiale: combien de positions par personne? Combien de personnes?
- combien y a t il de personnes? Pas 120 millions puisque les numéros de téléphone n'ont que 6 chiffres
- réplication entre les différents noeuds: quels facteurs choisir?
- pour l'insert, il faut passer par un csv (externe). Utilisation d'une base graph plutôt?
- utilisation d'un geoHash?

## Résolu:
- est-ce que l'INSERT se fait par rapport à l'ordre de la table insérée? Oui

## Améliorations possibles:
- filtrer directement la latitude et la longitude avec:
WHERE Lmin < latitude AND Lmax < latitude AND lmin < longitude AND lmax < longitude 
- voir si des clauses de ce WHERE sont inutiles (dépend de la géographie du pays)

## Liens utiles (calcul de distances sur une sphère et prise en charge en SQL)
http://janmatuschek.de/LatitudeLongitudeBoundingCoordinates
http://www.movable-type.co.uk/scripts/latlong-db.html
