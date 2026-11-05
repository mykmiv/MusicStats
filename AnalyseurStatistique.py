import pandas as pd
import numpy as np
from datetime import timedelta


class AnalyseurStatistique:

    #Enregistre la collection musicale reçue dans l'attribut self.collection pour permettre à l'analyseur d'utiliser les données.
    def __init__(self, collection):
            self.collection = collection

    #Compte le nombre d'écoutes de chaque artiste dans la collection
    #puis retourne une liste contenant les n artistes les plus écoutés 
    #avec leur nombre d'écoutes du plus populaire au moins populaire.
    def top_artistes(self, n):

        #Crée un dictionnaire pour compter les écoutes par artiste.
        compteur_artistes = {}

        #Parcourt toutes les écoutes de la collection.
        for ecoute in self.collection.ecoutes:
            artiste = ecoute.chanson.artiste

            #Augmente le nombre d'écoute de l'artiste si il est déjà
            #dans le dictionnaire sinon crée le compteur de l'artiste à 1.
            if artiste in compteur_artistes:
                    compteur_artistes[artiste] += 1
            else:
                    compteur_artistes[artiste] = 1

        #Crée une liste vide pour enregistrer le classement.
        classement = []

        #Tant que le classement n'a pas atteint le nombre d'artistes demandé.
        while len(classement) < n and compteur_artistes > 0:
            artiste_populaire = None
            maximum_ecoutes = 0

            #Recherche l'artiste qui a le plus d'écoutes dans ceux qui restent 
            #dans le dictionnaire.
            for artiste in compteur_artistes:
                if compteur_artistes[artiste] > maximum_ecoutes:
                    maximum_ecoutes = compteur_artistes[artiste]
                    artiste_populaire = artiste

            #Ajoute l'artiste et son nombre d'écoute au classement puis le retire
            #pour chercher le prochain artiste.
            classement.append((artiste_populaire, maximum_ecoutes))
            del compteur_artistes[artiste_populaire]

        #Retourne le classement des artistes.
        return classement
    
    #Compte le nombre d'écoutes de chaque chanson dans la collection
    #puis retourne une liste contenant les n chansons les plus écoutés 
    #avec leur nombre d'écoutes du plus populaire au moins populaire.
    def top_chansons(self, n):

        #Crée un dictionnaire pour compter les écoutes par chanson.
        compteur_chanson = {}


        #Parcourt toutes les écoutes de la collection.
        for ecoute in self.collection.ecoutes:
            chanson = ecoute.chanson

            #Augmente le nombre d'écoute de la chanson si elle est déjà
            #dans le dictionnaire sinon crée le compteur de la chanson à 1.
            if chanson in compteur_chanson:
                compteur_chanson[chanson] += 1
            else:
                compteur_chanson[chanson] = 1

        #Crée une liste vide pour enregistrer le classement.
        classement = []

        #Tant que le classement n'a pas atteint le nombre de chansons demandé.
        while len(classement) < n and compteur_chanson > 0:
            chanson_populaire = None
            maximum_ecoutes = 0

            #Recherche la chanson qui a le plus d'écoutes dans celles qui restent
            #dans le dictionnaire.
            for chanson in compteur_chanson:
                if compteur_chanson[chanson] > maximum_ecoutes:
                     maximum_ecoutes = compteur_chanson[chanson]
                     chanson_populaire = chanson

            #Ajoute la chanson et son nombre d'écoute au classement puis la retire
            #pour chercher la prochaine chanson.
            classement.append((chanson_populaire, maximum_ecoutes))
            del compteur_chanson[chanson_populaire]

        #Retourne le classement des chansons.
        return classement

    #Regarde les écoutes de la collection et les regroupe par semaine.
    #Retourne un dictionnaire avec la date de chaque début
    #de semaine et le nombre d'écoutes de cette semaine.
    def ecoutes_par_semaine(self):

        #Crée un dictionnaire pour compter le nombre d'écoutes par semaine.
        compteur_semaines = {}

        #Parcourt toutes les écoutes de la collection.
        for ecoute in self.collection.ecoutes:

            #Récupère la date de l'écoute et l'heure.
            date = ecoute.date_heure.date()

            #Calcul le lundi correspondant à la semaine d'écoute.
            debut_semaine = date - timedelta(days=date.weekday())

            #Augmente le nombre d'écoute de la semaine si elle est déjà
            #dans le dictionnaire sinon crée le compteur de la semaine à 1.
            if debut_semaine in compteur_semaines:
                 compteur_semaines[debut_semaine] += 1
            else:
                compteur_semaines[debut_semaine] = 1

        #Retourne le dictionnaire avec les semaines et le nombre d'écoutes.
        return compteur_semaines

    #Compte le nombre d'utilisateurs différents ayant effectué au moins 
    #une écoute pendant chaque semaine de la période demandé.
    #La période se termine à la semaine de la dernière écoute enregistrée.
    #Retourne un dictionnaire avec les dates des débuts de semaine et le 
    #nombre d'utilisateurs actifs liés à chaque semaine.
    def utilisateur_actifs_par_semaine(self, semaines = 4):

        #Crée un dictionnaire pour enregistrer les uttilisateurs actifs
        #dans chaque semaine.
        utilisateurs_semaines = {}

        #Retourne un dictionnaire vide si aucune écoute n'existe
        #ou si le nombre de semaine demandé est invalide.
        if len(self.collection.ecoutes) == 0 or semaines <= 0:
            return {}

        #Prend la date de la première écoute comme point de départ
        #pour rechercher la date la plus récente.
        derniere_date = self.collection.ecoutes[0].date_heure.date()

        #Parcourt les écoutes pour trouver la date la plus récente.
        for ecoute in self.collection.ecoutes:
            date = ecoute.date_heure.date()
    
            if date > derniere_date:
                derniere_date = date
    
        #Calcule le lundi de la dernière semaine.
        derniere_semaine = derniere_date -timedelta(days=derniere_date.weekday())

        #Crée un ensemble vide pour chacune des semaines demandées
        #en partant de la drnière vers ceux d'avants.
        for i in range(semaines):
            debut = derniere_semaine - timedelta(weeks=i)
            utilisateurs_semaines[debut] = set()

        #Parcourt les écoutes pour enregistrer les utilisateurs  dans 
        #la semaine correspondant à leur écoute.
        for ecoute in self.collection.ecoutes:
            date = ecoute.date_heure.date()
            debut = date - timedelta(days=date.weekday())

            #Choisi un ensemble, car ça permet d'éviter les doublons
            #d'utilisateurs dans la même semaine.
            if debut in utilisateurs_semaines:
                utilisateurs_semaines[debut].add(ecoute.utilisateur)

        #Crée un dictionnaire pour enregistrer le nombre d'utilisateurs actifs par semaine.
        #différents pour chaque semaine.
        resultat = {}

        #Compte les utilisateurs présents dans chaque ensemble.
        for debut in utilisateurs_semaines:
            resultat[debut] = len(utilisateurs_semaines[debut])

        #Retourne le nombre d'utilisateurs actifs par semaine.
        return resultat

    #Calcul le pourcentage de la variation du nombre d'utilsateur
    #entre la première et la dernière semaine de la période demandée.
    #Retourne le pourcentage calculé ou None si le calcul est impossible 
    #genre quand la première semaine à zéro utilisateur.
    def croissance_utilisateurs(self, semaines = 4):

        #Récupère le nombre d'utilsateur actif par semaine.
        donnees = self.utilisateur_actifs_par_semaine(self.collection, semaines)

        #Retourne None si la période contient moins de 2 semaines.
        if len(donnees) < 2:
            return None

        #Place les dates des semaines dans une liste et les tris
        #de la plus ancienne à la plus récente.
        dates = list(donnees)
        dates.sort()

        #Récupère la date de la dernière semaine et celle de la 
        #première semaine de la période.
        semaine_actuelle = dates[-1]
        semaine_precedente = dates[0]

        #Récupère le nombre d'utilisateur actif pour ces deux semaines.
        actuel = donnees[semaine_actuelle]
        precedent = donnees[semaine_precedente]

        #Retourne None si la première semaine compte zéro utilisateur.
        if precedent == 0:
            return None

        #Calcul la variation en pourcentage entre les 2 semaines.
        croissance = (actuel - precedent) / precedent * 100

        #Retourne le pourcentage de variation.
        return croissance

    #Recherche les utilisateurs ayant effectué au moins une écoute
    #pendant trois semaines différentes ou plus dans la période demandée.
    #Retourne une liste avec les utilisateurs récurrents.
    #Si la collection est vide ou la période est invalide ça retourne une liste vide.
    def utilisateurs_recurents(self, semaines = 4):

        #Crée une liste vide pour enregistrer les utilisateurs récurrents..
        resultat = []

        #Retourne une liste vide si aucune écoute n'existe.
        if len(self.collection.ecoutes) == 0 or semaines <= 0:
            return resultat

        #Prend la date de la première écoute pour commencer la recherche
        #de la date la plus récente.
        derniere_date = self.collection.ecoutes[0].date_heure.date()

        #Recherche la date de la dernière écoute de la collection.
        for ecoute in self.collection.ecoutes:
            date = ecoute.date_heure.date()

            if date > derniere_date:
                derniere_date = date

        #Calcul le lundi de la dernière semaine.
        derniere_semaine = derniere_date - timedelta(days=derniere_date.weekday())

        #Calcul le lundi de la première semaine de la période demandée.
        premiere_semaine = derniere_semaine - timedelta(weeks=semaines - 1)

        #Crée un dictionnaire pour enregistrer les semaines durant 
        #lesquelles chaque utilisateur à été actif.
        semaines_utilisateurs = {}

        #Parcourt toutes les çoutes de la collection.
        for ecoute in self.collection.ecoutes:
            date = ecoute.date_heure.date()
            debut = date - timedelta(days=date.weekday())
            utilisateur = ecoute.utilisateur

            #Garde seulement les écoutes dans la période demandée.
            if premiere_semaine <= debut <= derniere_semaine:

                #Crée un ensemble vide si l'utilisateur n'est pas encore
                #dans le dictionnaire.
                if debut not in semaines_utilisateurs:
                    semaines_utilisateurs[utilisateur] = set()

                #Ajoute la semaine à l'ensemble de l'utilisateur.
                #Chaque semaine est comptée une seule fois.
                semaines_utilisateurs[utilisateur].add(debut)

        #Parcourt les utilisateurs pour vérifier le nombre de semaine
        #différentes durant lesquelles ils ont été actifs.
        for utilisateur in semaines_utilisateurs:

            #Ajoute à la liste les utilisateurs actifs durant 3
            #semaines différentes ou plus.
            if len(semaines_utilisateurs[utilisateur]) > 2:
                resultat.append(utilisateur)

        #Retourne la liste des utilisateurs récurrents.
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
        return compte.reindex(index = range(24), fill_value=0) #meme structure que ecoute_par_jour, les index sont de 0-23
        
    
    def fidelite_musicale(self, utilisateur):
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
        if utilisateur.nombre_ecoutes() == 0:
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

