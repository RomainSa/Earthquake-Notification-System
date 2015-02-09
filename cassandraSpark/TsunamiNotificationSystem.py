# -*- coding: utf-8 -*-
"""
Created on Thu Jan 22 23:06:00 2015

@author: roms
"""

###############################################################################
# connection à la base et importations
import csv
from cassandra.cluster import Cluster

ip = ['54.84.252.58']
keyspace = 'tns'

cluster = Cluster()
session = cluster.connect(keyspace)

###############################################################################
# création des tables
session.execute('''CREATE TABLE tns.base (
	date text, 
	code_cellule text, 
	latitude decimal, 
	longitude decimal, 
	telephone int,
	PRIMARY KEY (telephone, date));''')

session.execute('''CREATE TABLE tns.filtre (
      date timestamp,
	latitude decimal, 
	longitude decimal, 
	telephone int PRIMARY KEY);''')

session.execute('''CREATE TABLE tns.lastPosition (
      date timestamp,    
	latitude decimal, 
	longitude decimal, 
	telephone int PRIMARY KEY);''')

session.execute('''CREATE TABLE tns.result (
      date timestamp,
	latitude decimal, 
	longitude decimal, 
	telephone int PRIMARY KEY);''')

###############################################################################
# remplissage des tables
inputFile = '/home/roms/Desktop/[10-02] Projet_noSQL/Earthquake-Notification-System/data_10.csv'

with open(inputFile, newline='') as csvfile:
    fileReader = csv.reader(csvfile, delimiter=';', quotechar = '|')
    for row in fileReader:
        session.execute("INSERT INTO tns.base (date, code_cellule, latitude, longitude, telephone) VALUES (%s, %s, %s, %s, %s)", [row[0][:19], row[1], float(row[2]), float(row[3]), int(row[4])])

# filtre sur la date du seisme et la met dans une nouvelle table
dateSeisme='2015-01-19 00:00:00'
rows = session.execute('SELECT * FROM tns.base WHERE date <= ' + '\'' + dateSeisme + '\'' + ' ALLOW FILTERING')        
for row in rows:
    session.execute("INSERT INTO tns.filtre (latitude, date, longitude, telephone) VALUES (%s, %s, %s, %s)", [row.latitude, row.date, row.longitude, row.telephone])

# filtre sur un carré
rows = session.execute('SELECT * FROM tns.filtre')        
for row in rows:
    session.execute("INSERT INTO tns.lastPosition (latitude, longitude, telephone) VALUES (%s, %s, %s)", [row.latitude, row.longitude, row.telephone])

# vérifie que cette base est bien triée (ie la dernière en dernière position)
# à copier dans CQLSH:


###############################################################################
# génération du séisme et de la table de résultats

lat = 20.0
long = 120.0
d = 16
d2 = d**2

rows = session.execute('SELECT * FROM tns.lastPosition')        
for row in rows:
    if((lat - d <= row.latitude <= lat + d) and (long - d <= row.longitude <= long + d)):
        session.execute("INSERT INTO tns.result (latitude, longitude, telephone) VALUES (%s, %s, %s)", [row.latitude, row.longitude, row.telephone])

# alternative
rows = session.execute('SELECT * FROM tns.lastPosition')        
for row in rows:
    if((row.latitude - lat) ** 2 + (row.longitude - long) ** 2 <= d2):
        session.execute("INSERT INTO tns.result (latitude, longitude, telephone) VALUES (%s, %s, %s)", [row.latitude, row.longitude, row.telephone])

