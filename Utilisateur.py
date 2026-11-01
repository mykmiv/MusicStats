class Utilisateur:

#Initialise un utilisateur avec son nom et une liste d'ecoute vide.
    def __init__(self, nom):
        self.nom = nom
        self.ecoutes = []

#Ajoute une écoute à la liste des écoutes de l'utilisateur.
    def ajouter_ecoute(self, ecoute):
        self.ecoutes.append(ecoute)

#Retourne le nombre d'écoutes de l'utilisateur.
    def nombre_ecoutes(self):
        return len(self.ecoutes)
    
    #Crée un dictionnaire avec les artiste écoutés par un utilisateur
    #et retourne None  si l'utilisateur n'a pas d'écoute enregistrée
    #sinon retourne l'artiste le plus écouté par l'utilisateur
    def artiste_prefere(self):

        #Vérifie si l'utilisateur n'a aucune écoute.
        if len(self.ecoutes) == 0:
            return None

        #Crée un dictionnaire pour compter le nombre d'écoute
        #de chaque artiste.
        compteur_artistes = {}

        #Parcourt toutes les écoutes de l'utilisateur.
        for ecoute in self.ecoutes:
            artiste = ecoute.chanson.artiste

            #Ajoute une écoute à l'artiste si l'artiste est déja
            #dans le dictionnaire sinon crée le compteur de l'artiste
            #à 1.
            if artiste in compteur_artistes:
                compteur_artistes[artiste] += 1
            else:
                compteur_artistes[artiste] = 1

        #Prépare les variables pour trouver l'artiste qui a le plus
        #grand nombre d'écoutes.
        artiste_favoris = None
        maximum_ecoutes = 0

        #Compare le nombre d'écoutes de chaque artiste et conserve l'artiste
        #qui a le plus d'écoutes.
        for artiste in compteur_artistes:
            if compteur_artistes[artiste] > maximum_ecoutes:
                maximum_ecoutes = compteur_artistes[artiste]
                artiste_favoris = artiste

        #Retourne l'artiste le plus écouté par l'utilisateur.
        return artiste_favoris
