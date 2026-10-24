import pandas as pd

class Ecoute:
    def __init__(self, utilisateur, chanson, date_heure):
        """Initialisation du constructeur"""
        self.utilisateur = utilisateur
        self.chanson = chanson
        self.date_heure = date_heure
    def jour_semaine(self):
        return self.date_heure.weekday() ### weekday = Methode
    def heure(self):
        return self.date_heure.hour ### hour = Attribut
        
##essai de la classe Ecoute
###ecoute1 = Ecoute("Xavier", "Chanson Try", pd.to_datetime("2026-10-24 18:40:19")) 
###print(ecoute1.jour_semaine()) ###Lundi commence a 0 donc 5 = Samedi
###print(ecoute1.heure()) ###18