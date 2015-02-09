# MANUEL UTILISATEUR
## Décomposition du code:
- lancement du cluster DataStax Enterprise 4.6 sous AWS
- téléchargement des données depuis S3 
- création puis remplissage des tables dans Cassandra
- lancement des calculs sous PySpark

## En détails:
### lancement du cluster DataStax Enterprise 4.6 sous AWS
Il est nécessaire de configurer un 'security group' et de créer une 'key pair' avant de lancer le cluster. Les paramètres du cluster doivent être renseignés au lancement (onglet '3. Configure instance' de AWS). Dans notre cas, les paramètres sont les suivants:
`--clustername clusterTest
--totalnodes 5
--version enterprise
--username *******
--password *******
--cfsreplicationfactor 2
--analyticsnodes 5`



### téléchargement des données depuis S3 
### création puis remplissage des tables dans Cassandra
### lancement des calculs sous PySpark
