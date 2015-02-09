# MANUEL UTILISATEUR - CASSANDRA/SPARK
Implémentation de la partie base de données distribuée en Cassandra. Les calculs distribués sont effectués par Spark. Le tout est packagé dans DataStax Enterprise 4.6.
## Décomposition du code:
- lancement du cluster DataStax Enterprise 4.6 sous AWS
- téléchargement des données depuis S3 
- création puis remplissage des tables dans Cassandra
- lancement des calculs sous PySpark
- récupération des fichiers de résultat
- visualisation

NB: afin de ne pas trop alourdir ce manuel, chaque ligne de code n'est aps détaillée, nous présentons ici seulement les principales étapes.

## Comment lancer le code?
Une fois le cluster lancé dans AWS, récupérer les addresses publiques et privées des noeuds et renseigner les paramètres correspondants dans le code (node0, node1...). Lancer ensuite le code ligne à ligne dans Shell puis dans Pyspark Shell.

## En détails:
Chaque étape est rattachée au numéro correspondant dans le code source
### 1 - lancement du cluster DataStax Enterprise 4.6 sous AWS
Lien pour lancer le cluster dans la région 'us-east-1':<br>
https://console.aws.amazon.com/ec2/home?region=us-east-1#LaunchInstanceWizard:ami=ami-ada2b6c4

Il est nécessaire de configurer un 'security group' et de créer une 'key pair' au préalable (voir la doc de DataStax Enterprise pour les détails). Les paramètres du cluster doivent être renseignés au lancement (onglet '3. Configure instance' de AWS). Dans notre cas, les paramètres sont les suivants:<br>
```
--clustername clusterTest
--totalnodes 5
--version enterprise
--username *******
--password *******
--cfsreplicationfactor 2
--analyticsnodes 5
```

### 2 - téléchargement des données depuis S3 
Il est nécessaire de télécharger le dernier client aws afin de pouvoir télécharger les données:<br>
```shell
sudo pip install awscli
aws configure
sudo aws s3 cp s3://bigdata-paristech/projet2014/data/data_10GB.csv /raid0/data_raw`
```

### 3 - création puis remplissage des tables dans Cassandra
On se connecte à cqlsh afin de créer un keyspace, des tables de données (base1 et base10) et la tabel qui va recevoir les résultats (result):
```sql
CREATE KEYSPACE IF NOT EXISTS tns WITH REPLICATION = {'class': 'NetworkTopologyStrategy', 'Analytics' : 2};

CREATE TABLE tns.base1 (
	telephone int,
	date timestamp, 
	latitude decimal, 
	longitude decimal, 
	PRIMARY KEY ((telephone), date));

CREATE TABLE tns.base10 (
	telephone int,
	date timestamp, 
	latitude decimal, 
	longitude decimal, 
	PRIMARY KEY ((telephone), date));

CREATE TABLE tns.result (
	telephone int,
	date timestamp, 
	insertdate timestamp,
	latitude decimal, 
	longitude decimal, 
	PRIMARY KEY (telephone));
```
On remplit ensuite les tables de la manière suivante:
- on splitte, sur le master, le fichier téléchargé par le nombre de workers:
```shell
sudo -s
awk -F ';' '{ print $5 ";" substr($1,1,19) ";"$3 ";" $4  }' /raid0/data_raw > /raid0/data
n=4 # number of workers that will receive the splits
split -n l/$n -d -a 2 /raid0/data /raid0/datafirstsplit
```
- on envoie un split à chaque worker:
```shell
for ((i=1;i<$n+1;i++)); do
  numfile=$(printf "%02d" $(($i-1)))
  nodename=$(eval "echo \"\$nodeprivate$i\"")
  scp -o "StrictHostKeyChecking no" -i /home/ubuntu/DSE_EC2.pem /raid0/datafirstsplit$numfile ubuntu@$nodename:~
  scp -o "StrictHostKeyChecking no" -i /home/ubuntu/DSE_EC2.pem /home/ubuntu/spark-env.sh ubuntu@$nodename:~
done
```
- chaque worker redivise le fichier en 16, 32, 64...splits:
```shell
m=64
datafirstsplit="`find -name "datafirstsplit*" -print`"
split -n l/$m -d -a 2 $datafirstsplit datasecondsplit
```
- pour chaque split, le worker lance un process et fait un `INSERT INTO` dans Cassandra
```shell
for ((i=0;i<$m;i++)); do
  num=$(printf "%02d" $i)
  cqlsh -e "COPY tns.base10 (telephone, date, latitude, longitude) FROM '/home/ubuntu/datasecondsplit$num' WITH DELIMITER = ';';" &
done
```
Ceci permet de paralléliser les insertions des données et d'atteindre des débits de l'ordre de plusieurs dizaines de milliers d'insertions par seconde.

### 4 - lancement des calculs sous PySpark

### 5 - récupération des fichiers de résultat

### 6 visualisation des résultats
