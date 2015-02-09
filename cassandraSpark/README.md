# MANUEL UTILISATEUR
## Décomposition du code:
- lancement du cluster DataStax Enterprise 4.6 sous AWS
- téléchargement des données depuis S3 
- création puis remplissage des tables dans Cassandra
- lancement des calculs sous PySpark

## Comment lancer le code?
- une fois le cluster lancé dans AWS, récupérer les addresses publiques et privées des noeuds et renseigner les paramètres correspondants dans le code (node0, node1...). Lancer ensuite le code ligne à ligne dans Shell puis dans Pyspark Shell.

## En détails:
### 1 - lancement du cluster DataStax Enterprise 4.6 sous AWS
Il est nécessaire de configurer un 'security group' et de créer une 'key pair' avant de lancer le cluster. Les paramètres du cluster doivent être renseignés au lancement (onglet '3. Configure instance' de AWS). Dans notre cas, les paramètres sont les suivants:

--clustername clusterTest<br>
--totalnodes 5<br>
--version enterprise<br>
--username *******<br>
--password *******<br>
--cfsreplicationfactor 2<br>
--analyticsnodes 5<br><br>

Lien pour lancer le cluster dans la région 'us-east-1':<br>
https://console.aws.amazon.com/ec2/home?region=us-east-1#LaunchInstanceWizard:ami=ami-ada2b6c4

### 2 - téléchargement des données depuis S3 
Il est nécessaire de télécharger le dernier client aws afin de pouvoir télécharger les données:<br>
sudo pip install awscli<br>
aws configure <br>
sudo aws s3 cp s3://bigdata-paristech/projet2014/data/data_10GB.csv /raid0/data_raw`

### 3 - création puis remplissage des tables dans Cassandra
On se connecte à cqlsh afin de créer

### 4 - lancement des calculs sous PySpark

### 5 - récupération des fichiers de résultat

### 6 visualisation des résultats
