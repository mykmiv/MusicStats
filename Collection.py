class CollectionMusicale:
    
    def __init__(self):
        self.artistes = {}
        self.chansons = {}
        self.utilisateurs = {}
        self.ecoutes = []

    
    def ajouter_artiste(self, artiste):
        self.artistes[artiste.nom] = artiste

    def trouver_artiste(self, nom):
        if nom in self.artistes:
            return self.artistes[nom]
        return None

    def ajouter_chanson(self, chanson):
        cle = chanson.titre + " - " + chanson.artiste.nom       #cle: titre - artiste
        self.chansons[cle] = chanson

    
    def trouver_chanson(self, titre, nom_artiste):
        cle = titre + " - " + nom_artiste
        if cle in self.chansons:
            return self.chansons[cle]
        return None

    
    def ajouter_utilisateur(self, utilisateur):
        self.utilisateurs[utilisateur.nom] = utilisateur

    
    def trouver_utilisateur(self, nom):
        if nom in self.utilisateurs:
            return self.utilisateurs[nom]
        return None

    def ajouter_ecoute(self, ecoute):
        self.ecoutes.append(ecoute)
        ecoute.utilisateur.ajouter_ecoute(ecoute)
