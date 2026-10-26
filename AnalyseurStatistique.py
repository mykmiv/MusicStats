import pandas as pd
import numpy as np

class AnalysateurStatistique:
    def __init__(self, collection):
        self.collection = collection
    def top_artistes(self, collection, x):
        """
        Cela retourne les x artistes les plus populaires dans la collection. 
        """
        return
    ### il est temps de commencer les boys !!! ###
    def top_chansons(self, collection, x):
        """
        Cela retourne les x chansons les plus populaires dans la collection. 
        """
        return
    def top_genres(self, collection, x): ###si on peut je vais aussi faire cela.###
        """
        Cela retourne les x genres les plus populaires dans la collection. 
        """
        return
    def ecoutes_par_semaine(self, collection):
        """
        Cela retourne le nombre d'écoutes par semaine dans la collection. 
        """
        return
    def repartition_par_jour(self, collection):
        """
        Cela retourne le nombre d'écoutes par jour dans la collection.
        """
        return
    def repartition_par_heure(self, collection):
        """
        Cela retourne le nombre d'écoutes par heure dans la collection.
        """
        return
    
    def fidelite(self, utilisateur):
        """
        Cela retourne le pourcentage d'écoutes d'un utilisateur qui vont à ses 5 artistes préférés.  
        """
        ### (ecoutes des 5 artistes pref / ecoutes totales ) * 100
        if utilisateur.nombre_ecoutes() == 0: ###On sort si l'utlisateur n'a pas encore d'ecoutes
            return 0
        artistes ={}
        for ecoute in utilisateur.ecoutes:
            if ecoute.chanson.artiste in artistes:
                artistes[ecoute.chanson.artiste] += 1
            else:
                artistes[ecoute.chanson.artiste] = 1
        ecoutes_triees = sorted(artistes.values(), reverse = True) ### Liste ordre decroissante des ecoutes par artiste
        top5 = sum(ecoutes_triees[:5]) ### On prend juste les 5 premiers elements de la liste, car cest la somme des ecoutes de ces 5 artistes preferes
        
        return (top5/utilisateur.nombre_ecoutes()) * 100