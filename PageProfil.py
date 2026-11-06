import customtkinter as ctk

# Permet d'afficher les graphiques Matplotlib
# directement dans un cadre CustomTkinter.
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class PageProfils(ctk.CTkFrame):

    #Initialise la page Profils en enregistrant la collection,
    #en indiquant qu'aucun utilisateur n'est sélectionné et 
    #en créant les éléments visuels de la page.
    def __init__(self, parent, collection, analyseur, graphiques):

        #Initialise le cadre CustomTkinter de la page Profils.
        ctk.CTkFrame.__init__(self, parent)
        
        #Enregistre la collection musicale utilisé pour la recherche.
        self.collection = collection

        # Conserve l'analyseur pour calculer les statistiques.
        self.analyseur = analyseur

        # Conserve le gestionnaire pour créer les graphiques.
        self.graphiques = graphiques  

        #Aucun utilisateur n'est sélectionné au départ.
        self.utilisateur_selectionne = None

        #Crée l'interface graphique de la page.
        self.creer_interface()

    #Crée le champ de recherche, le bouton de recherche, les cadres et
    #les étiquettes qui permetteront d'afficher les infos du profil sélectionne.
    def creer_interface(self):

        # Crée une zone défilable pour permettre de consulter
        # les informations, les statistiques et les graphiques.
        self.zone = ctk.CTkScrollableFrame(self)
        self.zone.pack(fill="both", expand=True)

        #Crée et affiche le titre de la page.
        self.titre = ctk.CTkLabel(self.zone, text="Profils des utilisateurs", font=("arial", 28 ,"bold"))
        self.titre.pack(pady=15)

        #Crée un cadre pour la recherche d'un utilisateur.
        self.cadre_recherche = ctk.CTkFrame(self.zone)
        self.cadre_recherche.pack(fill="x", padx=20, pady=10)

        #Crée un champ pour écrire le nom de l'utilisateur recherché.
        self.champ_recherche = ctk.CTkEntry(self.cadre_recherche,placeholder_text="Nom de l'utilisateur")
        self.champ_recherche.pack(pady=10)

        #Crée un bouton qui lance la fonction recherche.
        self.bouton_recherche = ctk.CTkButton(self.cadre_recherche, text="Rechercher", command=self.rechercher_utilisateur)
        self.bouton_recherche.pack(pady=10)

        #Crée une étiquette pour afficher les messages de recherche.
        self.label_message = ctk.CTkLabel(self.zone, text="")
        self.label_message.pack(pady=5)

        #Crée un cadre pour afficher les infos du profil,
        self.cadre_profil = ctk.CTkFrame(self.zone)

        #Crée une étiquette qui indique qu'aucun profil n'est encore sélectionné.
        self.label_profil = ctk.CTkLabel(self.cadre_profil, text="Aucun utilisateur sélectionné")
        self.label_profil.pack(pady=10)
        self.cadre_profil.pack(fill="x", padx=20, pady=10)
        
        #Crée un cadre pour les classements des artistes et des chansons.
        self.cadre_classements = ctk.CTkFrame(self.zone)
        self.cadre_classements.pack(fill="x", padx=20, pady=10)

        #Crée une étiquette pour afficher les artistes préférés.
        self.label_artistes = ctk.CTkLabel(self.cadre_classements, text="", justify="left")
        self.label_artistes.pack(pady=10)

        #Crée une étiquette pour afficher les chansons préférés.
        self.label_chansons = ctk.CTkLabel(self.cadre_classements, text="", justify="left")
        self.label_chansons.pack(pady=10)

        # Crée un cadre pour afficher la fidélité musicale
        # et le coefficient de variation de l'utilisateur.
        self.cadre_statistiques = ctk.CTkFrame(self.zone)
        self.cadre_statistiques.pack(fill="x", padx=20, pady=10)

        # Crée une étiquette pour afficher la fidélité musicale.
        self.label_fidelite = ctk.CTkLabel(self.cadre_statistiques, text="Fidélité musicale : —")
        self.label_fidelite.pack(pady=10)

        # Crée une étiquette pour afficher la régularité d'écoute.
        self.label_regularite = ctk.CTkLabel(self.cadre_statistiques, text="Coefficient de variation : —")
        self.label_regularite.pack(pady=10)

        # Crée un cadre pour contenir les deux graphiques
        # déjà programmés dans GestionnaireGraphiques.
        self.cadre_graphiques = ctk.CTkFrame(self.zone)
        self.cadre_graphiques.pack(fill="x", padx=20, pady=10)

        # Récupère le diagramme circulaire qui montre
        # la répartition des écoutes selon le jour de la semaine.
        figure_jours = self.graphiques.graphique_jours()

        # Adapte les dimensions du graphique pour l'interface.
        figure_jours.set_size_inches(5.5, 3.5)

        # Intègre le graphique Matplotlib dans le cadre CustomTkinter.
        self.canvas_jours = FigureCanvasTkAgg(figure_jours, master=self.cadre_graphiques)

        # Dessine et affiche le diagramme circulaire.
        self.canvas_jours.draw()
        self.canvas_jours.get_tk_widget().pack(pady=10)

        # Récupère le graphique à barres qui montre
        # le nombre d'écoutes selon l'heure de la journée.
        figure_heures = self.graphiques.graphique_heures()

        # Adapte les dimensions du deuxième graphique.
        figure_heures.set_size_inches(5.5, 3.5)

        # Intègre le deuxième graphique dans le même cadre.
        self.canvas_heures = FigureCanvasTkAgg(figure_heures, master=self.cadre_graphiques )

        # Dessine et affiche le graphique à barres.
        self.canvas_heures.draw()
        self.canvas_heures.get_tk_widget().pack(pady=10)

        # Retire les figures de la gestion des fenêtres pyplot.
        # Elles restent affichées dans les widgets Tkinter.
        plt.close(figure_jours)
        plt.close(figure_heures)

    #Récupère le nom écrit dans le champ de recherche et cherche
    #un utilisateur avec ce nom dans la collection musicale.
    #Affiche son profil si il est trouvé sinon affiche un message d'erreur.
    def rechercher_utilisateur(self):

        #Récupère le nom écrit dans le champ de recherche.
        nom = self.champ_recherche.get().strip()

        #Prépare une variable pour enregistrer l'utilisateur trouvé.
        utilisateur_trouve = None

        #Parcourt les utilisateurs de la collection.
        for utilisateur in self.collection.utilisateurs.values():

            #Compare les noms sans tenir compte des majuscules.
            if utilisateur.nom.lower() == nom.lower():
                utilisateur_trouve = utilisateur

                #Arrête la boucle si troouvé.
                break

        #Si l'utilisateur existe, affiche son profil.
        if utilisateur_trouve is not None:
            self.label_message.configure(text="")
            self.afficher_profil(utilisateur_trouve)
        else:
            #Réinitialise le profil si aucun utilisateur n'est trouvé.
            self.utilisateur_selectionne = None
            self.label_message.configure(text="Utilisateur introuvable")
            self.label_profil.configure(text="Aucun utilisateur selectionné")

            #Efface les classements du profil précédent.
            self.label_artistes.configure(text="")
            self.label_chansons.configure(text="")

            # Efface les statistiques si aucun utilisateur n'est trouvé.
            self.label_fidelite.configure(text="Fidélité musicale : —")
            self.label_regularite.configure(text="Coefficient de variation : —")

    #Enregistre l'utilisateur sélectionné, récupère son nombre total
    #d'écoutes et affiche ses infos etses classements.
    def afficher_profil(self, utilisateur):

        #Enregistre l'utilisateur dont le profil doit être affiché.
        self.utilisateur_selectionne = utilisateur

        #Récupère le nombre total d'écoutes de cet utilisateur.
        total_ecoutes = utilisateur.nombre_ecoutes()

        #Prépare le texte contenant le nom et le nombre d'écoutes.
        texte = ("Utilisateur : " + utilisateur.nom + "\nNombre d'écoutes : " + str(total_ecoutes))

        #Affiche les informations du profil.
        self.label_profil.configure(text=texte)

        #Affiche les artistes et chansons préférés de l'utilisateur.
        self.afficher_artistes_preferes(utilisateur)
        self.afficher_chansons_preferees(utilisateur)

        # Calcule le pourcentage des écoutes consacrées
        # aux cinq artistes préférés de l'utilisateur.
        fidelite = self.analyseur.fidelite_musicale(utilisateur)

        # Calcule le coefficient de variation des écoutes
        # quotidiennes pour mesurer leur régularité.
        regularite = self.analyseur.coefficient_variation(utilisateur)

        # Affiche la fidélité musicale avec deux décimales.
        self.label_fidelite.configure(text="Fidélité musicale : " + str(round(fidelite, 2)) + " %")

        # Affiche le coefficient de variation avec deux décimales.
        self.label_regularite.configure(text="Coefficient de variation : " + str(round(regularite, 2)) + " %")

    #Compte les écoutes de chaque artiste pour un utilisateur,
    #trouve les 5 artistes ayant le plus d'écoutes et les affiche
    #avec leur position et leur nombre d'écoutes.
    def afficher_artistes_preferes(self, utilisateur):

        #Crée un dictionnaire pour compter les écoutes de chaque artiste.
        compteur = {}

        #Parcourt toutes les écoutes de l'utilisateur,
        for ecoute in utilisateur.ecoutes:
            nom = ecoute.chanson.artiste.nom

            #Augmente le compteur de l'artiste si il est déjà dans le dictionnaire
            #sinon crée le compteur de l'artiste à 1.
            if nom in compteur:
                compteur[nom] += 1
            else:
                compteur[nom] = 1

        #Prépare le texte et la position du premier artiste.
        texte = "Top 5 des artistes préférés :\n\n"
        position = 1

        #Continue jusqu'à temps de trouver 5 artistes ou que dictionnaire soit vide.
        while position <= 5 and len(compteur) > 0:
            artiste_populaire = None
            maximum_ecoutes = 0

            #Recherche l'artiste ayant le plus grand nombre d'écoutes.
            for artiste in compteur:
                if compteur[artiste] > maximum_ecoutes:
                    artiste_populaire = artiste
                    maximum_ecoutes = compteur[artiste]

            #Ajoute l'artiste trouvé, son rang et ses écoutes au texte.
            texte += (str(position) + ". " + artiste_populaire + " : " + str(maximum_ecoutes) + " ecoutes\n")

            #Retire l'artiste trouvé pour chercher le suivant.
            del compteur[artiste_populaire]
            position += 1

        #Affiche le classement complet des artistes.
        self.label_artistes.configure(text=texte)

    #Compte les écoutes de chaque chanson d'un utilisateur,
    #trouve les 5 chansons les plus écoutés et les affiche
    #avec leurs titres, leurs artistes et leurs nombre d'écoutes.
    def afficher_chansons_preferees(self, utilisateur):

        #Crée un dictionnaire pour compter les écoutes de chaque chanson.
        compteur = {}

        #Parcourt toutes les écoutes de l'utilisateur.
        for ecoute in utilisateur.ecoutes:
            chanson = ecoute.chanson

            #Identifie chaque chanson par son titre et son artiste, car plusieurs chansons peuvent avoir le même titre.
            cle = (chanson.titre,  chanson.artiste.nom)

            #Augmente le compteur de la chanson si elle est déjà dans le dictionnaire
            #sinon crée le compteur de la chanson à 1.
            if cle in compteur:
                compteur[cle] += 1
            else:
                compteur[cle] = 1

        #Prépare le texte et la position de la première chanson.
        texte = "Top 5 des chansons preférées :\n\n"
        position = 1

        #Continue jusqu'à temps de trouver 5 chansons ou que dictionnaire soit vide.
        while position <= 5 and len(compteur) > 0:
            chanson_populaire = None
            maximum_ecoutes = 0

            #Recherche la chanson ayant le plus grand nombre d'écoutes.
            for chanson in compteur:
                if compteur[chanson] > maximum_ecoutes:
                    maximum_ecoutes = compteur[chanson]
                    chanson_populaire = chanson

            #Récupère le titre et le nom de l'artiste de la chanson trouvé.
            titre = chanson_populaire[0]
            artiste = chanson_populaire[1]

            #Ajoute la chanson trouvée, son rang et ses écoutes au texte.
            texte += (str(position) + ". " + titre + " - " + artiste + " : " + str(maximum_ecoutes) + " ecoutes\n")

            #Retire la chanson trouvée pour chercher la suivante.
            del compteur[chanson_populaire]
            position += 1

        #Affiche le classement complet des chansons.
        self.label_chansons.configure(text=texte)

        

