# Tsunami-Notification-System

![](http://renewaldynamics.com/wp-content/uploads/2011/03/wave1.jpg)

Projet noSQL: conception d'un système d'alerte tsunami par SMS pour le Japon suite à un tremblement de terre.

Notre approche a été la suivante: nous avons travaillé à la fois sur mongoDb et Cassandra/Spark afin de voir les avantages et inconvénients de chaque solution.
Vous trouverez dans chaque sous-dossier:
- le code source
- un manuel utilisateur (ReadMe.md)

La présentation qui a été donnée le 10 Janvier à 9h30 est à la racine du repository.

## Problématique
- créer un cluster avec au moins 5 noeuds dans les 5 villes les plus peuplées du Japon
- charger les données dans le Cluster
- les coordonnées d'un tremblement de terre sont fournies
- couper les noeuds présents dans la zone à risque (ie à 500 km de l'épicentre)
- faire un INSERT avec au minimum 'date/heure de réception', 'numéro de téléphone', 'position lors du temblement de terre'
- donner le temps pour avoir prévenu 80% de la population

## Implémentation
Nous avons utilisé deux technologies: mongoDb et Cassandra/Spark.
