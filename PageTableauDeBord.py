from tkinter import filedialog, messagebox

import customtkinter as ctk
import matplotlib.pyplot as plt

from GestionnaireCSV import GestionnaireCSV

class PageTableauDeBord(ctk.CTkFrame):

    #Initialise la page Tableau de bord en enregistrant la collection,
    #l'analyseur et le gestionnaire de graphiques puis affiche les donnees.
    def __init__(self, parent, collection, analyseur, graphiques):
       ctk.CTkFrame.__init__(self, parent)

       #Enregistre les objets nécessaires au fonctionnement de la page.
       self.collection = collection
       self.analyseur = analyseur
       self.graphiques = graphiques

       #Définit la période initile à 4 semaines.
       self.semaines = 4

       #Crée l'interface et affiche les statistiques et classements.
       self.creer_interface()
       self.afficher_statistiques()
       self.afficher_top_artistes()
       self.afficher_top_chansons()

    #Crée les élements visuels du tableay de bord.
    def creer_interface(self):

        #Crée et afficher le titre du tableau de bord.
        self.titre = ctk.CTkLabel(self, text="Tableau de bord", font=("Arial", 28, "bold"))
        self.titre.pack(pady=15)

        #Crée un cadre pour les statistiques générales.
        self.cadre_statistiques = ctk.CTkFrame(self)
        self.cadre_statistiques.pack(fill="x", padx=20,pady=10)

        #Crée une étiquettes pour afficher le nombre d'écoutes.
        self.label_ecoutes =ctk.CTkLabel(self.cadre_statistiques, text="")
        self.label_ecoutes.pack(pady=5)

        #Crée une étiquette pour afficher l'artiste le plus populaire.
        self.label_utilisateurs = ctk.CTkLabel(self.cadre_statistiques, text="")
        self.label_utilisateurs.pack(pady=5)

        #Crée un cadre pour les classements des artistes et des chansons.
        self.label_artistes = ctk.CTkLabel(self.cadre_statistiques, text="")
        self.label_artistes.pack(pady=5)

        #Crée une étiquette pour présenter le top 5 des artistes.
        self.cadre_classements = ctk.CTkFrame(self)
        self.cadre_classements.pack(fill="x", padx=20, pady=10)

        #Crée un sélecteur permettant de choisir 4,6 ou 12 semaines.
        self.label_top_artistes = ctk.CTkLabel(self.cadre_classements, text="", justify="left")
        self.label_top_artistes.pack(pady=10)

        #Crée une étiquette pour présenter le top 5 des chansons.
        self.label_top_chansons = ctk.CTkLabel(self.cadre_classements, text="", justify="left")
        self.label_top_chansons.pack(pady=10)

        #Crée un bouton pour afficher le graphique des artistes les plus écoutés.
        self.bouton_artistes = ctk.CTkButton(self, text="Graphique des artistes", command=self.afficher_graphique_artistes)
        self.bouton_artistes.pack(pady=5)

        #Crée un bouton pour afficher le graphique des chansons les plus écoutés.
        self.bouton_chansons = ctk.CTkButton(self, text="Graphique des chansons", command=self.afficher_graphique_chansons)
        self.bouton_chansons.pack(pady=5)

        #Crée un sélevteur permettant de choisir 4,6 ou 12 semaines.
        self.choix_semaines = ctk.CTkSegmentedButton(self, values=["4", "6", "12"], command=self.changer_periode)
        self.choix_semaines.pack(pady=10)

        #Sélectionne 4 semaines par défault.
        self.choix_semaines.set("4")

        #Crée un bouton pour afficher le graphique des utilisateurs actifs.
        self.bouton_evolution = ctk.CTkButton(self, text="Evolution des utilisateurs actifs", command=self.afficher_evolution_utilisateurs)
        self.bouton_evolution.pack(pady=10)

        #Crée un bouton pour exporter les statistiques du tableau de bord en CSV.
        self.bouton_exporter = ctk.CTkButton(self, text="Exporter les statistiques (CSV)", command=self.exporter_csv)
        self.bouton_exporter.pack(pady=10)

    def afficher_statistiques(self):

        #Compte toutes les écoutes enregistrés dans la collection.
        total_ecoutes = len(self.collection.ecoutes)

        #Crée un ensemble pour enregistrer les utilisateurs différents.
        utilisateurs = set()

        #Ajoute chaque utilisateur dans l'ensemble pour éviter les doublons.
        for ecoute in self.collection.ecoutes:
            utilisateurs.add(ecoute.utilisateur)

        #Compte le nombre d'utilisateurs différents.
        total_utilisateurs = len(utilisateurs)

        #Affiche le nombre total d'écoutes.
        self.label_ecoutes.configure(text="Nombre d'écoutes : " + str(total_ecoutes))

        #Affiche le nombre total d'utilisateur.
        self.label_utilisateurs.configure(text="Nombre d'utilisateurs : " + str(total_utilisateurs))

        #Récupère l'artiste le plus écouté dans la collection.
        classement = self.analyseur.top_artistes(1)

        #Affiche son nom si le classement contient au moins 1 artiste.
        if len(classement) > 0:
            artiste = classement[0][0]

            self.label_artistes.configure(text="Artiste le plus populaire : " + artiste.nom)
        else:
            self.label_artistes.configure(text="Artiste le plus populaire : -")

    #Recupère les 5 artistes les plus écoutés dans la collection
    #et affiche leurs noms et leurs nombres d'écoutes dans le classement.
    def afficher_top_artistes(self):

        #Demande à l'analyseur le classement des 5 artistes.
        classement = self.analyseur.top_artistes(5)

        #Prépare le texte du classement et son premier numéro.
        texte = "Top 5 des artistes les plus écoutés :\n\n"
        position = 1

        #Ajoute chaque artiste, sa position et son nombre d'écoutes au texte.
        for artiste, nombre in classement:
            texte += (str(position) + ". " + artiste.nom + " : " + str(nombre) + " ecoutes\n")
            position += 1

        #Affiche le classement complet dans l'étiquette.
        self.label_top_artistes.configure(text=texte)

    #Récupère les 5 chansons les plus écoutées dans la collection
    #et affiche leurs titres et leurs nombre d'écoutes dans le classement.
    def afficher_top_chansons(self):

        #Demande à l'analyseur le classement des 5 chansons.
        classement = self.analyseur.top_chansons(5)

        #Prépare le texte du classement et son premier numéro.
        texte = "Top 5 des chansons les plus écoutées :\n\n"
        position = 1

        #Ajoute chaque chanson, sa position et son nombre d'écoutes au texte.
        for chanson, nombre in classement:
            texte += (str(position) + ". " + chanson.titre + " : " + str(nombre) + " ecoutes\n")
            position += 1

        #Afficher le classement complet dans l'étiquette.
        self.label_top_chansons.configure(text=texte)

    #Modifie le nombre de semaines sélectionnées par l'utilisateur
    #pour déterminer la période du graphique des utilisateurs actifs.
    def changer_periode(self, semaines):

        #Convertit la valeur choisie en entoer et l'enregistre.
        self.semaines = int(semaines)

    #Demande au gestionnaire de graphiques de créer la courbe
    #des utilisateur actifs pour la période choisie et l'affiche.
    def afficher_evolution_utilisateurs(self):

        #Crée le graphique à partir de la collection et de la période choisie.
        self.graphiques.graphique_utilisateur_actifs(self.semaines)

        #Ouvre la fenêtre Matplotlib contenant le graphique.
        plt.show()

    #Demande au gestionnaire de graphiques de créer le graphique
    #des 5 artistes les plus écoutés et l'affiche.
    def afficher_graphique_artistes(self):
        self.graphiques.graphique_top_artistes(5)
        plt.show()

    #Demande au gestionnaire de creer le graphique
    #des 5 chansons les plus ecoutes et l'affiche.
    def afficher_graphique_chansons(self):
        self.graphiques.graphique_top_chansons(5)
        plt.show()

    #Prépare les statistiques affichées dans le tableau de bord sous forme
    #de lignes (categorie, rang, nom, valeur) pour pouvoir les exporter en CSV.
    def preparer_donnees_export(self):

        #Crée une liste vide pour enregistrer chaque ligne du fichier.
        lignes = []

        #Compte le nombre d'utilisateurs différents (le set évite les doublons).
        utilisateurs = set()
        for ecoute in self.collection.ecoutes:
            utilisateurs.add(ecoute.utilisateur)

        #Ajoute les statistiques générales.
        lignes.append({"categorie": "Statistiques générales", "rang": "", "nom": "Nombre d'écoutes",
                       "valeur": len(self.collection.ecoutes)})
        lignes.append({"categorie": "Statistiques générales", "rang": "", "nom": "Nombre d'utilisateurs",
                       "valeur": len(utilisateurs)})

        #Ajoute le top 5 des artistes avec leur nombre d'écoutes.
        position = 1
        for artiste, nombre in self.analyseur.top_artistes(5):
            lignes.append({"categorie": "Top artistes", "rang": position, "nom": artiste.nom, "valeur": nombre})
            position += 1

        #Ajoute le top 5 des chansons avec leur nombre d'écoutes.
        position = 1
        for chanson, nombre in self.analyseur.top_chansons(5):
            lignes.append({"categorie": "Top chansons", "rang": position, "nom": chanson.titre, "valeur": nombre})
            position += 1

        #Ajoute les utilisateurs actifs par semaine pour la période choisie,
        #de la semaine la plus ancienne à la plus récente.
        actifs = self.analyseur.utilisateur_actifs_par_semaine(self.semaines)
        dates = list(actifs)
        dates.sort()
        for debut in dates:
            lignes.append({"categorie": "Utilisateurs actifs (" + str(self.semaines) + " semaines)",
                           "rang": "", "nom": "Semaine du " + str(debut), "valeur": actifs[debut]})

        #Retourne toutes les lignes à exporter.
        return lignes

    #Demande à l'utilisateur où enregistrer le fichier puis exporte
    #les statistiques du tableau de bord dans un fichier CSV.
    def exporter_csv(self):

        #Ouvre une boite de dialogue pour choisir le nom et l'emplacement du fichier.
        chemin = filedialog.asksaveasfilename(title="Exporter les statistiques",
                                              defaultextension=".csv",
                                              initialfile="statistiques_musicstats.csv",
                                              filetypes=[("Fichiers CSV", "*.csv")])

        #Arrête si l'utilisateur a annulé la boite de dialogue.
        if not chemin:
            return

        #Exporte les données et affiche un message selon le résultat.
        reussi = GestionnaireCSV().exporter_statistiques(chemin, self.preparer_donnees_export())
        if reussi:
            messagebox.showinfo("Exportation réussie", "Les statistiques ont été exportées dans :\n\n" + chemin)
        else:
            messagebox.showerror("Erreur d'exportation", "Impossible d'exporter les statistiques dans :\n\n" + chemin)

        




       


