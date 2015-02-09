# -*- coding: utf-8 -*-
"""
Created on Mon Jan 19 15:38:54 2015

@author: roms
"""

import math
import pandas as pd

def distance(lat1, lng1, lat2, lng2):
    r = 6378.137
    latitude1 = lat1 * math.pi / 180
    longitude1 = lng1 * math.pi / 180
    latitude2 = lat2 * math.pi / 180
    longitude2 = lng2 * math.pi / 180
    return r * math.acos(math.cos(latitude1) * math.cos(latitude2) * math.cos(longitude2 - longitude1) + math.sin(latitude1) * math.sin(latitude2))

ville1 = 'Tokyo',    35.732727,	139.722404
ville2 = 'Yokohama', 35.462635,	139.774854
ville3 = 'Osaka',    34.705359,	135.500729
ville4 = 'Nagoya',   35.193866,	136.907394
ville5 = 'Sapporo',  43.179025,	141.388028

villes = [ville1, ville2, ville3, ville4, ville5]
villes = pd.DataFrame([ville[1:] for ville in villes], index = [ville[0] for ville in villes], columns = ['lat', 'long'])

distances = pd.DataFrame(0.0, columns = villes.index, index = villes.index)
for villeX in range(5):
    for villeY in range(5):
        distances.iloc[villeX, villeY] = distance(villes['lat'][villeX], villes['long'][villeX], villes['lat'][villeY], villes['long'][villeY])

