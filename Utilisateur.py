class Utilisateur:

    def __init__(self, nom):
        self.nom = nom
        self.ecoutes = []

    def ajouter_ecoute(self, ecoute):
        self.ecoutes.append(ecoute)

    def nombre_ecoutes(self):
        return len(self.ecoutes)
    
    #Crée un dictionnaire avec les artiste écoutés par un utilisateur
    #et retourne None  si l'utilisateur n'a pas d'écoute enregistrée
    #sinon retourne l'artiste le plus écouté par l'utilisateur
    def artiste_prefere(self):
        if len(self.ecoutes) == 0:
            return None
        
        compteur_artistes = {}

        for ecoute in self.ecoutes:
            artiste = ecoute.chanson.artiste

            if artiste in compteur_artistes:
                compteur_artistes[artiste] += 1
            else:
                compteur_artistes[artiste] = 1

        artiste_favoris = None
        maximum_ecoutes = 0

        for artiste in compteur_artistes:
            if compteur_artistes[artiste] > maximum_ecoutes:
                maximum_ecoutes = compteur_artistes[artiste]
                artiste_favoris = artiste

        return artiste_favoris
