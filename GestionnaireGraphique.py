import matplotlib.pyplot as plt
import AnalyseurStatistique
class GestionnaireGraphiques:

     #Enregistre l'objet analyseur dans self.analyseur pour pouvoir
     #utiliser ses fonctions de calcul de statistiques musicales.
    def __init__(self, analyseur):
        self.analyseur = analyseur
    
    #Crée une courbe du nombre d'utilisateurs actifs pour chaque semaine
    #de la période demandée et retourne la figure Matplotlib.
    def graphique_utilisateur_actifs(self, collection, semaine=4):

        #Récupère le nombre d'utilisateurs actifs pour chaque semaine.
        donnees = self.amalyseur.utilisateur_actifs_par_semaine(collection, semaines)

        #Trie les dates des semaines dans l'ordre chronologique.
        dates = list(donnees)
        dates.sort()

        #Crée deux listes pour les valeurs et les dates du graphique.
        valeurs = []
        etiquettes = []

        #Ajoute chaque date et son nombre d'utilisateurs actifs aux listes.
        for date in dates:
            
            etiquettes.append(str(date))
            valeurs.append(donnees[date])

        #Crée les positions des semaines sur l'axe horizontal.
        positions = list(range(len(etiquettes)))

        #Crée la figure qui va contenir le graphique.
        figure = plt.figure(figsize=(9, 5))

        #Trace la courbe et affiche les dates sur l'axe horizontal.
        plt.plot(positions, valeur, marker='o-')
        plt.xticks(positions, etiquettes)
        plt.title("Evolution des utilisateurs actifs")
        plt.xlabel("Semaine")
        plt.ylabel("Nombre d'utilisateurs actifs")

        return figure
    
    #Prend les n artistes les plus écoutés et crée un diagramme
    #à barres qui présente le nombre d'écoutes de chaque artiste.
    #Retourne la figure Matplotlib.
    def graphique_top_artistes(self, collection, n = 5):

        #Récupère le classement des artistes.
        classement = self.analyseur.top_artistes(collection, n)

        #Crée les listes pour les artistes et leur nombre d'écoutes.
        artistes = []
        ecoutes = []

        #Sépare les artistes et leur nombre d'écoutes.
        for artiste,nombre in classement:
            artistes.append(artiste)
            ecoutes.append(nombre)

        #Crée la figure et trace le diagramme à barres.
        figure = plt.figure(figsize=(9, 5))

        plt.bar(artistes, ecoutes)
        plt.title("Artistes les plus écoutés")
        plt.xlabel("Artistes")
        plt.ylabel("Nombre d'écoutes")

        return figure

    #Prend les n chansons les plus écoutés et crée un diagramme
    #à barres présantant le nobre d'écoutes de chaque morceau.
    #Retourne la figure Matplotlib.
    def graphique_top_morceaux(self, collection, n = 5):

        #Récupère le classement des chansons.
        classement = self.analyseur.top_moreaux(collection, n)

        #Crée les listes pour les chansons et leur nombre d'écoutes.
        chansons = []
        ecoutes = []

        #Sépare les chansons et leur nombre d'éçoute.
        for chanson, nombre in classement:
            chansons.append(chanson)
            ecoutes.append(nombre)

        #Crée la figure et trace le diagramme à barres.
        figure = plt.figure(figsize=(9, 5))

        plt.bar(chansons, ecoutes)
        plt.title("Chansons les plus écoutées")
        plt.xlabel("Chansons")
        plt.ylabel("Nombre d'écoutes")

        return figure

    def graphique_jours(self, collection):
        """Cela retourne un diagramme circulaire des ecoutes par jour"""
        jours = ["Lundi", "Mardi","Mercredi","Jeudi","Vendredi","Samedi","Dimanche"]
        ecoutes = self.analyseur.ecoutes_par_jour(collection)   #Myke a mis attribut analyseur
        jours_graph = []
        ecoutes_graph = []
        for jour in range(7):
            if ecoutes[jour] > 0:
                ecoutes_graph.append(ecoutes[jour])
                jours_graph.append(jours[jour])

        fig = plt.figure() #Cest sur elle que le graphique sera cree
        plt.pie(ecoutes_graph, labels= jours_graph, autopct="%1.0f%%")
        plt.title("La répartition des écoutes par jour de la semaine ")
        plt.legend(jours_graph)
        return fig
    
    def graphique_heures(self, collection):
         """Cela retourne un diagramme a barres des ecoutes par heure"""
         heures = [i for i in range(24)]
         ecoutes = self.analyseur.ecoutes_par_heure(collection) #Myke a mis attribut analyseur
        
         fig = plt.figure()
         plt.bar(heures, ecoutes,
                 width=0.8,
                 color= "green")
         plt.title("Le nombre d'écoutes par heure de la journée")
         plt.xlabel("Heures")
         plt.ylabel("Nombre d'écoutes")
         plt.grid(False)
         return fig