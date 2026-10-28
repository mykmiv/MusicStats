import matplotlib.pyplot as plt

class GestionnaireGraphiques:

    def __init__(self, analyseur):
        self.analyseur = analyseur

    def graphique_utilisateur_actifs(self, collection, semaine=4):
        donnees = self.amalyseur.utilisateur_actifs_par_semaine(collection, semaines)

        dates = list(donnees)
        dates.sort()

        valeurs = []
        etiquettes = []


        for date in dates:
            
            etiquettes.append(str(date))
            valeurs.append(donnees[date])

        positions = list(range(len(etiquettes)))

        figure = plt.figure(figsize=(9, 5))

        plt.plot(positions, valeur, marker='o-')
        plt.xticks(positions, etiquettes)
        plt.title("Evolution des utilisateurs actifs")
        plt.xlabel("Semaine")
        plt.ylabel("Nombre d'utilisateurs actifs")

        return figure

    def graphique_top_artistes(self, collection, n = 5):
        classement = self.analyseur.top_artistes(collection, n)

        artistes = []
        ecoutes = []

        for artiste,nombre in classement:
            artistes.append(artiste)
            ecoutes.append(nombre)

        figure = plt.figure(figsize=(9, 5))

        plt.bar(artistes, ecoutes)
        plt.title("Artistes les plus écoutés")
        plt.xlabel("Artistes")
        plt.ylabel("Nombre d'écoutes")

        return figure

    def graphique_top_morceaux(self, collection, n = 5):
        classement = self.analyseur.top_moreaux(collection, n)

        chansons = []
        ecoutes = []

        for chanson, nombre in classement:
            chansons.append(chanson)
            ecoutes.append(nombre)

        figure = plt.figure(figsize=(9, 5))

        plt.bar(chansons, ecoutes)
        plt.title("Chansons les plus écoutées")
        plt.xlabel("Chansons")
        plt.ylabel("Nombre d'écoutes")

        return figure

