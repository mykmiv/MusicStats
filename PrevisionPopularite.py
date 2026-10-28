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

        #(Heure d'ecoute - premiere heure d'ecoute) transforme en journée divisé par 7 pour avoir le chiffre de semain
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

            # Semaine sans ecoute, on divise par 1 pour eviter la division par zero
            if total == 0:
                total = 1
            
            ecoutes_entite.append(nombre)
            ecoutes_totales.append(total)

        parts = np.array(ecoutes_entite) / np.array(ecoutes_totales) * 100
        return parts
