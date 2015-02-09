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
## Etape 1 : Commander une machine MongoDB 2.4 with 4000 IOPS 
http://docs.mongodb.org/ecosystem/platforms/amazon-ec2


Step by Step :

1) 

http://docs.mongodb.org/ecosystem/platforms/amazon-ec2/

temps (1mn)

2)se connecter à La machine aws 
chmod 400 ahmed.pem    
ssh -i ahmed.pem ec2-user@52.0.172.1  

temps (1mn)

3) importer les 1GB :
wget http://s3.amazonaws.com/bigdata-paristech/projet2014/data/data_1GB.csv

temps (2mn)

4) faire du remplacement avec les ligne de commnade pour adapter la "Date" à MongoDB
remplacer les virgules par des point
remplacer les espace par des T
ajouter à la position 23une lettre "Z"

input : 2015-01-18 09:19:16,888;Yok_98;35.462635;139.774854;526198

sed 's/,/./g;s/ /T/g;s/^\(.\{23\}\)/\1Z/'  data_10GB.csv > data_10GB_Date.csv 

output : 2015-01-18T09:19:16.888Z;Yok_98;35.462635;139.774854;526198

temps (30mn)

5) creer json

input : 2015-01-18T09:19:16.888Z;Yok_98;35.462635;139.774854;526198

awk -F ';' '{ print "{date:\"" $1 "\",code:\"" $2 "\",position:[" $4 "," $3 "],telephone:" $5 "}" }' data_10GB_Date.csv > data_10GB_Date.json

output : {"date":"2015-01-18T09:19:16.888Z","code":"Osa_61","position":[135.906451,34.232793],"telephone":829924}

temps (30mn)

6) lancer mongod 

mongod --repair
sudo mongod


7) lancer mongo dans un nouvel terminal


6) Importer le json dans mongo DB

mongoimport -d test -c Data_sedawk  --type json --file data_10GB_Date.json 

temps (100mn) --> 182000000 lignes


8) Querry dans mongodb :

db.Data_sedawk.find().count()

db.Data_sedawk.find().limit(10).pretty()

###Pour comparer la position:

Ensure Position:

db.Data_sedawk.ensureIndex({position:"2d"})

tester des requetes sur position

db.Data_sedawk.find({position: {$near:[51,-114],maxDistance: 500000}} )

Tester des requete sur la date:

db.Data_sedawk.find({
...     date: { 
...             '$gte': '2014-01-14 18:08:31,111',
...             '$lt': '2016-01-15 18:08:31,111' 
...     }
... }).limit(4)



{
  $near: {
     $geometry: {
        type: "Point" ,
        coordinates: [ <longitude> , <latitude> ]
     },
     $maxDistance: <distance in meters>,
     $minDistance: <distance in meters>
  }
}



GROUP BY :

db.Data_sedawk.aggregate( [ { $group : { _id : "$code" } } ] )
Comptage avec Group by:

db.Data_sedawk.aggregate( [ { $group : { _id : "$code" ,count: { $sum: 1 }} } ] )

GROUP BY DATE:

db.Data_sedawk.aggregate( [ { $group : { _id : "$telephone" , MaxDate: {$max: "$date"}} } ] ).limit(4) 


sh.allowSharding()
ceer un undex
ensureIndex
sharding(comme ensure)







#IMLEMENTATION VIA MONGO MMS AWS






## Liens utiles (calcul de distances sur une sphère et prise en charge en SQL)
http://janmatuschek.de/LatitudeLongitudeBoundingCoordinates
http://www.movable-type.co.uk/scripts/latlong-db.html
