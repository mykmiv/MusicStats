import pandas as pd
from Artiste import Artiste
from Chanson import Chanson
from Collection import CollectionMusicale
from Ecoute import Ecoute
from Utilisateur import Utilisateur


class GestionnaireCSV:
    # Lit le fichier CSV et retourne une CollectionMusicale
    def lire_fichier(self, chemin):
        try:
            df = pd.read_csv(chemin)
        except FileNotFoundError:
            print("Fichier introuvable :", chemin)
            return None

        # Enleve lignes avec info manquantes et transforme temps
        df = df.dropna(subset=["user_name", "listened_at", "artist_name", "track_name"])
        df["date_heure"] = pd.to_datetime(df["listened_at"], format="%m/%d/%Y %H:%M", errors="coerce")

        #Supprime les lignes dont la date est invalide
        df = df.dropna(subset=["date_heure"])

        #Transforme les durées en nombres.
        df["duree"] = pd.to_numeric(df["duree"], errors="coerce")

        #Les durées nulles ou négatives sont considérer comme inconnues.
        df.loc[df["duree"] <= 0, "duree"] = float("nan")
 
        collection = CollectionMusicale()
        for i in range(len(df)):
            ligne = df.iloc[i]

            #Creer un artiste sil existe pas 
            artiste = collection.trouver_artiste(ligne["artist_name"])
            if artiste == None:
                artiste = Artiste(ligne["artist_name"])
                collection.ajouter_artiste(artiste)

            #Chanson
            chanson = collection.trouver_chanson(ligne["track_name"], artiste.nom)
            if chanson == None:
                duree = None
                if not pd.isna(ligne["duree"]):
                    duree = ligne["duree"]
                recording_mbid = None
                if not pd.isna(ligne["recording_mbid"]):
                    recording_mbid = ligne["recording_mbid"]
                chanson = Chanson(ligne["track_name"], artiste, duree, recording_mbid)
                collection.ajouter_chanson(chanson)
                artiste.ajouter_chanson(chanson)

            else:
                #Ajoute la durée si elle est inconnue et que le CSV en contient une.
                if chanson.duree == None and not pd.isna(ligne["duree"]):
                    chanson.duree = ligne["duree"]

            # Utilisateur
            utilisateur = collection.trouver_utilisateur(ligne["user_name"])
            if utilisateur == None:
                utilisateur = Utilisateur(ligne["user_name"])
                collection.ajouter_utilisateur(utilisateur)

            
            ecoute = Ecoute(utilisateur, chanson, ligne["date_heure"])
            collection.ajouter_ecoute(ecoute)

        return collection

    
    def exporter_statistiques(self, chemin, donnees):
        if chemin[-4:] != ".csv":     #Enleve reste de caractere pour just garder le type de fichier
            print("Fichier non valide, le nom doit finir par .csv :", chemin)
            return False

        df = pd.DataFrame(donnees)
        try:
            df.to_csv(chemin, index=False)
        except OSError:
            print("Impossible d'écrire le fichier :", chemin)
            return False
        return True
