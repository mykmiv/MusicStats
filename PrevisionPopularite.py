import pandas as pd
import numpy as np
from Artiste import Artiste


class PrevisionPopularite:

    def __init__(self):
        self.tableau = None

    # Transforme les ecoutes en DataFrame (une ligne par ecoute)
    def preparer_donnees(self, collection):
        artistes = []
        chansons = []
        dates = []

        for ecoute in collection.ecoutes:
            artistes.append(ecoute.chanson.artiste.nom)
            chansons.append(ecoute.chanson.titre + " - " + ecoute.chanson.artiste.nom)
            dates.append(ecoute.date_heure)

        self.tableau = pd.DataFrame({"artiste": artistes, "chanson": chansons, "date_heure": dates})

        # Numero de semaine : jours depuis la premiere ecoute divise par 7
        date_min = self.tableau["date_heure"].min()

        #(Heure d'ecoute - premiere heure d'ecoute) transforme en journée divisé par 7 pour avoir le chiffre de semaine
        self.tableau["semaine"] = (self.tableau["date_heure"] - date_min).dt.days // 7

    # Retourne la part d'ecoute(%)
    def part_ecoutes(self, entite, periode):

        #Check pour voir si le Dataframe est valide
        if not isinstance(self.tableau, pd.DataFrame) or len(self.tableau) == 0 or periode < 1:
            print("Pas de donnees pour calculer les parts d'ecoute.")
            return np.array([])

        # Choisir la bonne colonne a filtrer
        if isinstance(entite, Artiste):
            masque = self.tableau["artiste"] == entite.nom
        else:
            masque = self.tableau["chanson"] == entite.titre + " - " + entite.artiste.nom

        totaux = self.tableau.groupby("semaine").size()
        comptes = self.tableau[masque].groupby("semaine").size()

    
        derniere = self.tableau["semaine"].max()
        premiere = max(0, derniere - periode + 1)

        ecoutes_entite = []
        ecoutes_totales = []

        for semaine in range(premiere, derniere + 1):

            total = 0

            if semaine in totaux.index:
                total = totaux.loc[semaine]

            nombre = 0

            if semaine in comptes.index:
                nombre = comptes.loc[semaine]

            if total == 0:
                total = 1

            ecoutes_entite.append(nombre)
            ecoutes_totales.append(total)

        parts = np.array(ecoutes_entite) / np.array(ecoutes_totales) * 100
        return parts

    # Calcule la droite des moindres carres et la prolonge de horizon semaines
    # Horizon: Jusqua quand veut on prédire
    def regression(self, parts, horizon):
        n = len(parts)

        #Minimum des parametres
        if n < 4 or horizon < 1:
            print("Pas assez de semaines pour faire une prevision (minimum 4).")
            return np.array([])

        x = np.arange(n)
        y = np.array(parts)
        pente = np.sum((x - x.mean()) * (y - y.mean())) / np.sum((x - x.mean()) ** 2)
        ordonnee = y.mean() - pente * x.mean()

        # Semaines futures : n, n+1, ... (horizon valeurs)
        x_futur = np.arange(n, n + horizon)
        prevision = ordonnee + pente * x_futur

        
        prevision[prevision < 0] = 0
        return prevision

    # Retourne la croissance en % entre la part actuelle et la part prevue
    def croissance(self, actuel, prevu):
        if actuel == 0:
            return None
        return (prevu - actuel) / actuel * 100

    # Prevoit les top 10 artist
    def prevoir_artistes(self, collection, horizon):
        return self.classement(collection, horizon, "artiste")

    # Prevoit les top 10 chansons
    def prevoir_chansons(self, collection, horizon):
        return self.classement(collection, horizon, "chanson")

    # Calcule les previsions des 10 plus ecoutes de la colonne ("artiste" ou "chanson")
    def classement(self, collection, horizon, colonne):
        if collection == None or len(collection.ecoutes) == 0:
            print("Aucune ecoute pour faire une prevision.")
            return []

        self.preparer_donnees(collection)
        top = self.tableau[colonne].value_counts().head(10)

        noms = []
        historiques = []
        previsions = []
        actuels = []
        prevus = []
        
        #Itere sur les top 10
        for nom in top.index:
            entite = None
            if colonne == "artiste":
                entite = collection.trouver_artiste(nom)
            elif nom in collection.chansons:
                #nom est deja la cle "titre - artiste" du dictionnaire
                entite = collection.chansons[nom]

            if entite == None:
                print("Introuvable dans la collection :", nom)
            else:
                historique = self.part_ecoutes(entite, 12)
                prevision = self.regression(historique, horizon)

                # On garde seulement les entites avec assez de donnees
                if len(prevision) > 0:
                    noms.append(nom)
                    historiques.append(historique)
                    previsions.append(prevision)
                    actuels.append(historique[-1])
                    prevus.append(prevision[-1])

        # Trier du plus grand au plus petit selon la part prevue
        df = pd.DataFrame({"nom": noms, "historique": historiques, "prevision": previsions,
                           "actuel": actuels, "prevu": prevus})
        df = df.sort_values("prevu", ascending=False)

        resultats = []
        for i in range(len(df)):
            ligne = df.iloc[i]
            resultats.append({"nom": ligne["nom"],
                              "historique": ligne["historique"],
                              "prevision": ligne["prevision"],
                              "actuel": ligne["actuel"],
                              "prevu": ligne["prevu"],
                              "croissance": self.croissance(ligne["actuel"], ligne["prevu"])})
        return resultats
