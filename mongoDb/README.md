# MANUEL UTILISATEUR - MONGODB

## Implémentation avec une seule instance AWS.

### Etape 1 : Commander une machine MongoDB 2.4 with 4000 IOPS 
http://docs.mongodb.org/ecosystem/platforms/amazon-ec2

### Etape 2 : Se connecter à La machine AWS en SSH
Allez dans le répertoire du fichier keys téléchargé (Downloads)
```shell
$chmod 400 keys.pem    
$ssh -i keys.pem ec2-user@52.0.172.1  
```

### Etape 3 : importer les 10GB depuis S3
```shell
$wget http://s3.amazonaws.com/bigdata-paristech/projet2014/data/data_1GB.csv
```
#### --> Temps (20mn)
### Etape 4 : Prétraitement des données dans la machine AWS
Afin d'adapter le format de la Date pour MongoDB on procède à 3 changements:<br>
1-remplacer les virgules par des points<br>
2-remplacer l'espace par un T<br>
3-ajouter à la position 23 la lettre "Z"<br>
input : 2015-01-18 09:19:16,888;Yok_98;35.462635;139.774854;526198<br>
En ligne de commande on tape :
```shell
$sed sed 's/,/./g;s/ /T/g;s/^\(.\{23\}\)/\1Z/' data_1MB.csv > data_1MB_Date.csv
output : 2015-01-18T09:19:16.888Z;Yok_98;35.462635;139.774854;526198
```
Afficher mes datas:
```shell
$head -10 data_10GB_Date.csv | grep 1
```
#### --> Temps (20mn)<br>
Après avoir fait les remplacements on convertit le csv en json en ligne de commandes:<br>
Il faut permuter les deux colonnes latitude et longitude pour que Mongo les interprète correctement.<br>
input : 2015-01-18T09:19:16.888Z;Yok_98;35.462635;139.774854;526198
```shell
$awk -F ';' '{ print "{date:\"" $1 "\",code:\"" $2 "\",position:[" $4 "," $3 "],telephone:" $5 "}" }' data_10GB_Date.csv > data_10GB_Date.json
output : {"date":"2015-01-18T09:19:16.888Z","code":"Osa_61","position":[135.906451,34.232793],"telephone":829924}
```
Afficher mes datas:
```shell
$head -10 data_10GB_Date.json | grep 1
```
#### --> Temps (30mn)
### Etape 5 : Lancer mongod
```shell
$mongod --repair
$sudo mongod
```
### Etape 6 : Lancer mongo dans un deuxième terminal <br>
```shell
$mongo
```
### Etape 7 : Importer le json dans la base MongoDB<br>
Il faut changer le répertoire et aller à la partition data de cette machine car le répertoire de ec2-user n'a pas suffisamment d'epace
```shell
$mongoimport -d test -c Data_sedawk  --type json --file data_10GB_Date.json <br>
```
#### --> Temps (100mn)<br>
### Etape 8 : Requêter la base Data_sedawk dans le Terminal Mongo<br>
#### Le nombre de lignes importées
```mongodb
db.Data_sedawk.find().count()
```
#### Le format de base
```mongodb
db.Data_sedawk.find().limit(10).pretty()
```
#### Faire une requete GROUP BY qui renvoie une seule ligne par téléphone avec la dernière Date mise à jour
```mongodb
$db.Data_sedawk.aggregate([{ $group : { position : "$position" , telephone : "$telephone" , MaxDate: {$max: "$date"}}}])
```
#### Filtrer par la Date de mise à jour<br>
Pour se faire il faut indexer la Date avec la commande ENSUREINDEX :
```mongodb
$db.Data_sedawk.ensureIndex({date:-1})
db.Data_sedawk.find({
     date: { 
             '$gte': '2014-01-14 18:08:31,111',
             '$lt': '2016-01-15 18:08:31,111' 
     }
})
```
#### Identifier la cible des personnes à contacter avec la commande NEAR:
Pour se faire il faut indexer la position avec la commande ENSUREINDEX :
```mongodb
$db.Data_sedawk.ensureIndex({position:"2d"})<br>
$db.Data_sedawk.find({position: {$near:[longitude_de_tsunami,latitude_de_tsunami],maxDistance: 500000}} )<br>
```
### Etape 8 : Exporter des collections depuis Mongo<br>
```mongodb
db.Data_sedawk.find().limit(4).forEach(function(doc){db.subset.insert(doc); });<br><br>
```
## Implémentation avec un cluster Mongo MMS AWS <br>
### Etape 1 : Créer un cluster MMS<br>
Créer un compte MMS:<br>
https://mms.mongodb.com/<br>
suivre le tutoriel de deploiement du cluster en précisant le nombre de noeuds:<br>
http://blog.mms.mongodb.com/post/103214737505/mms-create-aws-role-for-cross-account-access<br>
###Etape 2 : Définir le master et les slaves<br>
###Etape 3 : se connecter sur le master et refaire toutes les commandes de l'implémentation sur une seule instance.<br>
###Etape 4 : couper un noeud et refaire le calcul dans Mongo<br><br>
!!! Le cluster MMS est trop cher : En une heure aws m'a facturer 150 dollas<br>
 
##Liens utiles :<br>
http://www.tutorialspoint.com/mongodb/mongodb_overview.htm
