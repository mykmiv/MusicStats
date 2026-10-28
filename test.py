import pandas as pd
from Artiste import Artiste
from Chanson import Chanson
from Utilisateur import Utilisateur
from Ecoute import Ecoute
from Collectio import CollectionMusicale
from AnalyseurStatistique import AnalyseurStatistique

collection = CollectionMusicale()
analyseur = AnalyseurStatistique(collection)

#test 