class Chanson:
    
    def __init__(self, titre, artiste, duree=None, recording_mbid=None):
        self.titre = titre
        self.artiste = artiste
        self.duree = duree
        self.recording_mbid = recording_mbid

    # Transforme la duree
    def duree_formatee(self):
        if self.duree is None:
            return "Durée inconnue"
        total = int(self.duree)
        minutes = total // 60
        secondes = total % 60
        if secondes < 10:
            return str(minutes) + ":0" + str(secondes)
        return str(minutes) + ":" + str(secondes)

    # Retourne une phrase qui résume la chanson
    def description(self):
        return self.titre + " - " + self.artiste.nom + " (" + self.duree_formatee() + ")"
