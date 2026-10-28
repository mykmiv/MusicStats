class Artiste:
   
    def __init__(self, nom, mbid=None):
        self.nom = nom
        self.mbid = mbid
        self.chansons = []

    def ajouter_chanson(self, chanson):
        if chanson not in self.chansons:
            self.chansons.append(chanson)

    def nombre_chansons(self):
        return len(self.chansons)
