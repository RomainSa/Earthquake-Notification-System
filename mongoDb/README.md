# Earthquake-Notification-System
Earthquake Notification System designed using MongoDB

# PROBLEME
- créer un cluster avec au moins 5 noeuds dans les 5 villes les plus peuplées du Japon
- charger les données dans le Cluster
- les coordonnées d'un tremblement de terre sont fournies
- couper les noeuds présents dans la zone à risque (ie à 500 km de l'épicentre)
- faire un INSERT avec au minimum 'date/heure de réception', 'numéro de téléphone', 'position lors du temblement de terre'
- donner le temps pour avoir prévenu 80% de la population


# IMPLEMENTATION AVEC UNE SEULE INSTANCE AWS MongoDB 2.4 with 4000 IOPS 

#### Etape 1 : Commander une machine MongoDB 2.4 with 4000 IOPS 
http://docs.mongodb.org/ecosystem/platforms/amazon-ec2

#### Etape 2 : Se connecter à La machine AWS en SSH
Alley dans la repertoire de fichier keys téléchargé (Downloads)
$chmod 400 keys.pem    
$ssh -i keys.pem ec2-user@52.0.172.1  

#### Etape 3 : importer les 10GB depuis S3

$wget http://s3.amazonaws.com/bigdata-paristech/projet2014/data/data_1GB.csv

##### --> Temps (20mn)

#### Etape 4 : Prétraitement des données dans la machine AWS

Afin d'adapter le format de la Date pour MongoDB on procède par 3 changements:<br>

1-remplacer les virgules par des point<br>
2-remplacer les espace par des T<br>
3-ajouter à la position 23une lettre "Z"<br>

input : 2015-01-18 09:19:16,888;Yok_98;35.462635;139.774854;526198

En ligne de commande en tape :
$sed 's/,/./g;s/ /T/g;s/^\(.\{23\}\)/\1Z/'  data_10GB.csv > data_10GB_Date.csv 
output : 2015-01-18T09:19:16.888Z;Yok_98;35.462635;139.774854;526198
##### --> Temps (30mn)

Après avoir fait les remplacement en convertit le csv en json en ligne de commande:
Il faut permuter les deux colonnes latitude et longitude pour que Mongo les interprète correctement.

input : 2015-01-18T09:19:16.888Z;Yok_98;35.462635;139.774854;526198

$awk -F ';' '{ print "{date:\"" $1 "\",code:\"" $2 "\",position:[" $4 "," $3 "],telephone:" $5 "}" }' data_10GB_Date.csv > data_10GB_Date.json

output : {"date":"2015-01-18T09:19:16.888Z","code":"Osa_61","position":[135.906451,34.232793],"telephone":829924}

##### --> Temps (30mn)

#### Etape 5 : Lancer mongod 

$mongod --repair
$sudo mongod

#### Etape 6 : Lancer mongo dans un deuxième terminal 

#### Etape 7 : Importer le json dans la base MongoDB
Il faut changer la répertoire et aller à la partition data de cette machine car la répertoire de ec2-user n'a pas suffusement d'epace

$mongoimport -d test -c Data_sedawk  --type json --file data_10GB_Date.json 

##### --> Temps (100mn)

#### Etape 8 : Requeter la base Data_sedawk dans le Terminal Mongo
##### Le nombre de lignes importées
db.Data_sedawk.find().count()
##### Le format de base
db.Data_sedawk.find().limit(10).pretty()

##### Faire une requete GROUP BY qui renvoi une seule ligne par téléphone avec la dernière Date mise à jour
$Newbase=db.Data_sedawk.aggregate( [ { $group : { _id : "$telephone" , MaxDate: {$max: "$date"}} } ] ).limit(4) 

##### Filtrer par la Date de mise à jour
Pour se faire il faut indexer la Date avec la commande ENSUREINDEX :
$db.Data_sedawk.ensureIndex({date:-1})

db.Data_sedawk.find({
...     date: { 
...             '$gte': '2014-01-14 18:08:31,111',
...             '$lt': '2016-01-15 18:08:31,111' 
...     }
... })

##### Identifier la cible des personnes à contacter avec la commande NEAR:

Pour se faire il faut indexer la position avec la commande ENSUREINDEX :

$db.Data_sedawk.ensureIndex({position:"2d"})

$db.Data_sedawk.find({position: {$near:[longitude_de_tsunami,latitude_de_tsunami],maxDistance: 500000}} )

# IMPLEMENTATION AVEC UN CLUSTER MONGO MMS AWS 

#### Etape 1 : Creer un cluster MMS
Créer un compte MMS:
https://mms.mongodb.com/
suivre la tutoriel de deployement du cluster en précisant le nombre de noeuds:
http://blog.mms.mongodb.com/post/103214737505/mms-create-aws-role-for-cross-account-access

#### Etape 2 : Définir le master et les slaves

#### Etape 3 : se connecter sur le master et refaire toutes les commandes de IMLEMENTATION SUR UNE SEULE INSTANCE

#### Etape 4 : couper un noeud et refaire le calcul dans Mongo

!!! Le cluster MMS est trop cher : En une heure aws m'a facturer 150 dollas
