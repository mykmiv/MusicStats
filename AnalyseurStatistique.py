import pandas as pd
import numpy as np
from datetime import timedelta


class AnalyseurStatistique:

    def __init__(self, collection):
            self.collection = collection
    
    def top_artistes(self, collection, n):
        compteur_artistes = {}
    
        for ecoute in collection.ecoutes:
            artiste = ecoute.chanson.artiste
    
            if artiste in compteur_artistes:
                    compteur_artistes[artiste] += 1
            else:
                    compteur_artistes[artiste] = 1
    
        classement = []
    
        while len(classement) < n and compteur_artistes > 0:
            artiste_populaire = None
            maximum_ecoutes = 0
    
            for artiste in compteur_artistes:
                if compteur_artistes[artiste] > maximum_ecoutes:
                    maximum_ecoutes = compteur_artistes[artiste]
                    artiste_populaire = artiste
    
            classement.append((artiste_populaire, maximum_ecoutes))
            del compteur_artistes[artiste_populaire]
    
        return classement
    
    def top_chansons(self, collection, n):
        compteur_chanson = {}
    
        for ecoute in collection.ecoutes:
            chanson = ecoute.chanson
    
            if chanson in compteur_chanson:
                compteur_chanson[chanson] += 1
            else:
                compteur_chanson[chanson] = 1
    
        classement = []
    
        while len(classement) < n and compteur_chanson > 0:
            chanson_populaire = None
            maximum_ecoutes = 0
    
            for chanson in compteur_chanson:
                if compteur_chanson[chanson] > maximum_ecoutes:
                     maximum_ecoutes = compteur_chanson[chanson]
                     chanson_populaire = chanson
    
            classement.append((chanson_populaire, maximum_ecoutes))
            del compteur_chanson[chanson_populaire]
    
        return classement
    
    def ecoutes_par_semaine(self, collection):
        compteur_semaines = {}
    
        for ecoute in collection.ecoutes:
            date = ecoute.date_heure.date()
            debut_semaine = date - timedelta(days=date.weekday())
    
            if debut_semaine in compteur_semaines:
                 compteur_semaines[debut_semaine] += 1
            else:
                compteur_semaines[debut_semaine] = 1
    
        return compteur_semaines
    
    def utilisateur_actifs_par_semaine(self, collection, semaines = 4):
        utilisateurs_semaines = {}
    
        if len(collection.ecoutes) == 0 or semaines <= 0:
            return {}
    
        derniere_date = collection.ecoutes[0].date_heure.date()
    
        for ecoute in collection.ecoutes:
            date = ecoute.date_heure.date()
    
            if date > derniere_date:
                derniere_date = date
    
        derniere_semaine = derniere_date -timedelta(days=derniere_date.weekday())
    
        for i in range(semaines):
            debut = derniere_semaine - timedelta(weeks=i)
            utilisateurs_semaines[debut] = set()
    
        for ecoute in collection.ecoutes:
            date = ecoute.date_heure.date()
            debut = date - timedelta(days=date.weekday())
    
            if debut in utilisateurs_semaines:
                utilisateurs_semaines[debut].add(ecoute.utilisateur)
    
        resultat = {}
    
        for debut in utilisateurs_semaines:
            resultat[debut] = len(utilisateurs_semaines[debut])
    
        return resultat
    
    def croissance_utilisateurs(self, collection, semaines = 4):
        donnees = self.utilisateur_actifs_par_semaine(collection, semaines)
    
        if len(donnees) < 2:
            return None
    
        dates = list(donnees)
        dates.sort()
    
        semaine_actuelle = dates[-1]
        semaine_precedente = dates[0]
    
        actuel = donnees[semaine_actuelle]
        precedent = donnees[semaine_precedente]
    
        if precedent == 0:
            return None
    
        croissance = (actuel - precedent) / precedent * 100
    
        return croissance
    
    def utilisateurs_recurents(self, collection, semaines = 4):
        resultat = []
    
        if len(collection.ecoutes) == 0 or semaines <= 0:
            return resultat
    
        derniere_date = collection.ecoutes[0].date_heure.date()
    
        for ecoute in collection.ecoutes:
            date = ecoute.date_heure.date()
    
            if date > derniere_date:
                derniere_date = date
    
        derniere_semaine = derniere_date - timedelta(days=derniere_date.weekday())
    
        premiere_semaine = derniere_semaine - timedelta(weeks=semaines - 1)
    
        semaines_utilisateurs = {}
    
        for ecoute in collection.ecoutes:
            date = ecoute.date_heure.date()
            debut = date - timedelta(days=date.weekday())
            utilisateur = ecoute.utilisateur
    
            if premiere_semaine <= debut <= derniere_semaine:
                if debut not in semaines_utilisateurs:
                    semaines_utilisateurs[utilisateur] = set()
    
                semaines_utilisateurs[utilisateur].add(debut)
    
        for utilisateur in semaines_utilisateurs:
            if len(semaines_utilisateurs[utilisateur]) > 2:
                resultat.append(utilisateur)
    
        return resultat
    
    def top_genres(self, collection, x): #si on a le temps je vais aussi faire cela.
        """
        Cela retourne les x genres les plus populaires dans la collection. 
        """
        return
   
    def ecoutes_par_jour(self, collection):
        """
        Cela retourne le nombre d'écoutes par jour dans la collection.
        """
        if len(collection.ecoutes) == 0:
            return pd.Series(np.zeros(7), dtype = int)   # 0 ecoute chaque jour, dtype int pour pas de decimale
        liste_jours = [ecoute.jour_semaine() for ecoute in collection.ecoutes]  # Mettre le jour de chaque ecoute dans une liste
        compte = pd.Series(liste_jours).value_counts() #probleme, value_counts() modifie lindex des jours
        return compte.reindex(index=[0,1,2,3,4,5,6], fill_value=0)  #Reindex remet les jours dans le bon ordre et fill_value remplace les Nan par 0 si aucune ecoute ce jour la
    
    def ecoutes_par_heure(self, collection):
        """
        Cela retourne le nombre d'écoutes par heure dans la collection.
        """
        if len(collection.ecoutes) == 0:
            return pd.Series(np.zeros(24), dtype = int)
        liste_heures = [ecoute.heure() for ecoute in collection.ecoutes]
        compte = pd.Series(liste_heures).value_counts()
        return compte.reindex(index = range(24), fill_value=0) 
        
    
    def fidelite(self, utilisateur):
        """
        Cela retourne le pourcentage d'écoutes d'un utilisateur qui vont à ses 5 artistes préférés.  
        """
        ### (ecoutes des 5 artistes pref / ecoutes totales ) * 100
        if utilisateur.nombre_ecoutes() == 0: #On sort si l'utlisateur n'a pas encore d'ecoutes
            return 0
        artistes ={}
        for ecoute in utilisateur.ecoutes:
            if ecoute.chanson.artiste in artistes:
                artistes[ecoute.chanson.artiste] += 1
            else:
                artistes[ecoute.chanson.artiste] = 1
        ecoutes_triees = sorted(artistes.values(), reverse = True) ### Liste ordre decroissante des ecoutes par artiste
        top5 = sum(ecoutes_triees[:5]) # On prend juste les 5 premiers elements de la liste, car cest la somme des ecoutes de ces 5 artistes preferes
        
        return (top5/utilisateur.nombre_ecoutes()) * 100
    
    def coefficient_variation(self, utilisateur):
        """
        Cela retourne le coefficient de variation des écoutes quotidiennes de l'utilisateur
        (écart-type / moyenne) * 100, en incluant les jours sans écoute.
        """
        if len(utilisateur.ecoutes) == 0:
            return 0
        liste_jours= [ecoute.date_heure.normalize() for ecoute in utilisateur.ecoutes]  #normalize permet de garder la date comme elle etait, mais modifie l'heure a 0, ce qui permet dempiler les dates qui ont le meme jour
        jours_en_ordre = []
        premier_jour = min(liste_jours)
        dernier_jour = max(liste_jours)
        while (premier_jour <= dernier_jour):
            jours_en_ordre.append(premier_jour)
            premier_jour += pd.Timedelta(days=1)    #pd.Timedelta permet d'aditionner un certain temps a un autre, dans ce cas jajoute 1 jour donc days=1. Sans cela, impossible d'additionner un jour a une date.
        compte = pd.Series(liste_jours).value_counts().reindex(index=jours_en_ordre, fill_value=0)
        compte_en_liste = list(compte)
        return (np.std(compte_en_liste)/np.mean(compte_en_liste)) * 100

