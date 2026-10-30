import customtkinter as ctk
import matplotlib.pyplot as plt

class PageTableauDeBord(ctk.CTkFrame):

    def __init__(self, parent, collection, analyseur, graphiques):
       ctk.CTkFrame.__init__(self, parent)

       self.collection = collection
       self.analyseur = analyseur
       self.graphiques = graphiques
       self.semaines = 4

       self.creer_interface()
       self.afficher_statistiques()
       self.afficher_top_artistes()
       self.afficher_top_chansons()

    def creer_interface(self):
        self.titre = ctk.CTkLabel(self, text="Tableau de bord", font=("Arial", 28, "bold"))
        self.titre.pack(pady=15)


        self.cadre_statistiques = ctk.CTkFrame(self)
        self.cadre_statistiques.pack(fill="x", padx=20,pady=10)

        self.label_ecoutes =ctk.CTkLabel(self.cadre_statistiques, text="")
        self.label_ecoutes.pack(pady=5)

        self.label_utilisateurs = ctk.CTkLabel(self.cadre_statistiques, text="")
        self.label_utilisateurs.pack(pady=5)

        self.label_artistes = ctk.CTkLabel(self.cadre_statistiques, text="")
        self.label_artistes.pack(pady=5)

        self.cadre_classements = ctk.CTkFrame(self)
        self.cadre_classements.pack(fill="x", padx=20, pady=10)

        self.label_top_artistes = ctk.CTkLabel(self.cadre_classements, text="", justify="left")
        self.label_top_artistes.pack(pady=10)

        self.label_top_chansons = ctk.CTkLabel(self.cadre_classements, text="", justify="left")
        self.label_top_chansons.pack(pady=10)

        self.bouton_artistes = ctk.CTkButton(self, text="Graphique des artistes", command=self.afficher_graphique_artistes)
        self.bouton_artistes.pack(pady=5)

        self.bouton_chansons = ctk.CTkButton(self, text="Graphique des chansons", command=self.afficher_graphique_chansons)
        self.bouton_chansons.pack(pady=5)

        self.choix_semaines = ctk.CTkSegmentedButton(self, values=["4", "6", "12"], command=self.changer_periode)
        self.choix_semaines.pack(pady=10)
        self.choix_semaines.set("4")

        self.bouton_evolution = ctk.CTkButton(self, text="Evolution des utilisateurs actifs", command=self.afficher_evolution_utilisateurs)
        self.bouton_evolution.pack(pady=10)

    def afficher_statistiques(self):
        total_ecoutes = len(self.collection.ecoutes)

        utilisateurs = set()

        for ecoute in self.collection.ecoutes:
            utilisateurs.add(ecoute.utilisateur)

        total_utilisateurs = len(utilisateurs)

        self.label_ecoutes.configure(text="Nombre d'écoutes : " + str(total_ecoutes))

        self.label_utilisateurs.configure(text="Nombre d'utilisateurs : " + str(total_utilisateurs))

        classement = self.analyseur.top_artistes(self.collection, 1)

        if len(classement) > 0:
            artiste = classement[0][0]

            self.label_artistes.configure(text="Artiste le plus populaire : " + artiste.nom)
        else:
            self.label_artistes.configure(text="Artiste le plus populaire : -")

    def afficher_top_artistes(self):
        classement = self.analyseur.top_artistes(self.collection, 5)

        texte = "Top 5 des artistes les plus écoutés :\n\n"
        position = 1
        
        for artiste, nombre in classement:
            texte += (str(position) + ". " + artiste.nom + " : " + str(nombre) + " ecoutes\n")
            position += 1

        self.label_top_artistes.configure(text=texte)

    def afficher_top_chansons(self):
        classement = self.analyseur.top_chansons(self.collection, 5)

        texte = "Top 5 des chansons les plus écoutées :\n\n"
        position = 1

        for chanson, nombre in classement:
            texte += (str(position) + ". " + chanson.titre + " : " + str(nombre) + " ecoutes\n")
            position += 1

        self.label_top_chansons.configure(text=texte)

    def changer_periode(self, semaines):
        self.semaines = int(semaines)

    def afficher_evolution_utilisateurs(self):
        self.graphiques.graphique_utilisateurs_actifs(self.collection, self.semaines)
        plt.show()

        




       


