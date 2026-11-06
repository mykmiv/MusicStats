import os
from tkinter import filedialog

import customtkinter as ctk
import matplotlib.pyplot as plt

from GestionnaireCSV import GestionnaireCSV
from AnalyseurStatistique import AnalyseurStatistique
from GestionnaireGraphique import GestionnaireGraphiques
from PrevisionPopularite import PrevisionPopularite
from PageTableauDeBord import PageTableauDeBord
from PageProfil import PageProfils
from PagePrevision import PagePrevision


#Chemin du CSV par défaut, calculé à partir du dossier de ce fichier
#pour que l'application fonctionne peu importe d'où elle est lancée.
CHEMIN_CSV_DEFAUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "donnees.csv")


class ApplicationMusicStats(ctk.CTk):

    #Initialise la fenetre principale, charge le CSV une seule fois
    #et crée les objets partagés par les 3 pages.
    def __init__(self, chemin_csv=CHEMIN_CSV_DEFAUT):
        ctk.CTk.__init__(self)

        #Objets créés seulement si le chargement du CSV réussit.
        self.collection = None
        self.analyseur = None
        self.graphiques = None
        self.prevision = None
        self.pages = {}

        #Crée la fenetre principale.
        self.title("MusicStats")
        self.geometry("1100x750")
        self.minsize(850, 600)

        #Ferme aussi les fenetres Matplotlib quand on quitte l'application.
        self.protocol("WM_DELETE_WINDOW", self.quitter)

        #Crée le menu et la zone de contenu, puis charge les données.
        self.creer_menu()
        self.creer_zone_contenu()
        self.charger_donnees(chemin_csv)

    #Crée le menu de navigation à gauche de la fenetre.
    def creer_menu(self):

        #Crée un cadre pour le menu de navigation.
        self.menu = ctk.CTkFrame(self, width=200)
        self.menu.pack(side="left", fill="y", padx=10, pady=10)
        self.menu.pack_propagate(False)

        #Affiche le titre de l'application.
        self.titre = ctk.CTkLabel(self.menu, text="MusicStats", font=("Arial", 26, "bold"))
        self.titre.pack(pady=30)

        #Crée les 3 boutons de navigation.
        self.bouton_dashboard = ctk.CTkButton(self.menu, text="Tableau de bord", command=self.afficher_dashboard)
        self.bouton_dashboard.pack(pady=10, padx=15, fill="x")

        self.bouton_profils = ctk.CTkButton(self.menu, text="Profils", command=self.afficher_profils)
        self.bouton_profils.pack(pady=10, padx=15, fill="x")

        self.bouton_previsions = ctk.CTkButton(self.menu, text="Prévisions", command=self.afficher_previsions)
        self.bouton_previsions.pack(pady=10, padx=15, fill="x")

        #Associe chaque nom de page à son bouton.
        self.boutons = {"dashboard": self.bouton_dashboard,
                        "profils": self.bouton_profils,
                        "previsions": self.bouton_previsions}

        #Conserve la couleur normale des boutons pour pouvoir la remettre.
        self.couleur_bouton = self.bouton_dashboard.cget("fg_color")
        self.couleur_bouton_actif = self.bouton_dashboard.cget("hover_color")

        #Les boutons restent désactivés tant que les données ne sont pas chargées.
        self.activer_menu(False)

    #Crée le cadre qui contient les pages.
    def creer_zone_contenu(self):
        self.contenu = ctk.CTkFrame(self)
        self.contenu.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        #Permet aux pages de prendre toute la zone disponible.
        self.contenu.grid_rowconfigure(0, weight=1)
        self.contenu.grid_columnconfigure(0, weight=1)

    #Active ou désactive les boutons du menu.
    def activer_menu(self, actif):
        etat = "normal" if actif else "disabled"
        for bouton in self.boutons.values():
            bouton.configure(state=etat)

    #Supprime tout ce qui est affiché dans la zone de contenu.
    def vider_contenu(self):
        for widget in self.contenu.winfo_children():
            widget.destroy()
        self.pages = {}

    #Lit le CSV et crée les objets partagés.
    #Affiche un message d'erreur si le fichier
    #est introuvable ou invalide.
    def charger_donnees(self, chemin):
        self.vider_contenu()
        self.activer_menu(False)

        #Affiche un message pendant le chargement.
        message = ctk.CTkLabel(self.contenu, text="Chargement des données...", font=("Arial", 18))
        message.grid(row=0, column=0)
        self.update()

        try:
            collection = GestionnaireCSV().lire_fichier(chemin)
        except KeyError as erreur:
            self.afficher_erreur("Le fichier CSV est invalide : la colonne « " + str(erreur.args[0])
                                 + " » est manquante.\n\n" + chemin)
            return
        except ValueError as erreur:
            self.afficher_erreur("Le fichier CSV est invalide ou illisible.\n\n" + chemin
                                 + "\n\nDétail : " + str(erreur))
            return
        except OSError as erreur:
            self.afficher_erreur("Impossible d'ouvrir le fichier CSV.\n\n" + chemin
                                 + "\n\nDétail : " + str(erreur))
            return

        if collection is None:
            self.afficher_erreur("Fichier CSV introuvable :\n\n" + chemin)
            return

        if len(collection.ecoutes) == 0:
            self.afficher_erreur("Le fichier CSV ne contient aucune écoute valide.\n\n" + chemin)
            return

        #Crée les objets de service partagés par les pages.
        self.collection = collection
        self.analyseur = AnalyseurStatistique(self.collection)
        self.graphiques = GestionnaireGraphiques(self.analyseur)
        #PagePrevision crée encore sa propre prévision : cet objet est
        #gardé ici pour quand la page pourra le recevoir.
        self.prevision = PrevisionPopularite()

        self.vider_contenu()
        self.creer_pages()
        self.activer_menu(True)
        self.afficher_page("dashboard")

    #Crée les 3 pages et les place au meme endroit.
    def creer_pages(self):
        self.pages["dashboard"] = PageTableauDeBord(self.contenu, self.collection, self.analyseur, self.graphiques)
        self.pages["profils"] = PageProfils(self.contenu, self.collection)
        self.pages["previsions"] = PagePrevision(self.contenu, self.collection)

        #Place les pages dans la meme case puis les cache.
        for page in self.pages.values():
            page.grid(row=0, column=0, sticky="nsew")
            page.grid_remove()

    #Affiche un message d'erreur clair et un bouton pour choisir un autre fichier.
    def afficher_erreur(self, message):
        self.vider_contenu()

        cadre = ctk.CTkFrame(self.contenu, fg_color="transparent")
        cadre.grid(row=0, column=0)

        titre = ctk.CTkLabel(cadre, text="Impossible de charger les données", font=("Arial", 24, "bold"),
                             text_color="#d9534f")
        titre.pack(pady=(0, 15))

        texte = ctk.CTkLabel(cadre, text=message, wraplength=650, justify="center")
        texte.pack(pady=10)

        bouton = ctk.CTkButton(cadre, text="Choisir un fichier CSV...", command=self.choisir_fichier)
        bouton.pack(pady=15)

    #Ouvre une boite de dialogue pour choisir un CSV.
    def choisir_fichier(self):
        chemin = filedialog.askopenfilename(title="Choisir le fichier CSV",
                                            filetypes=[("Fichiers CSV", "*.csv"), ("Tous les fichiers", "*.*")])
        #Chaine vide si l'utilisateur annule.
        if chemin:
            self.charger_donnees(chemin)

    #Cache les autres pages, affiche celle qui est sélectionnée
    #et met en évidence son bouton.
    def afficher_page(self, nom):
        if nom not in self.pages:
            return

        for page in self.pages.values():
            page.grid_remove()
        self.pages[nom].grid()

        for nom_bouton, bouton in self.boutons.items():
            if nom_bouton == nom:
                bouton.configure(fg_color=self.couleur_bouton_actif)
            else:
                bouton.configure(fg_color=self.couleur_bouton)

    #Affiche la page du tableau de bord.
    def afficher_dashboard(self):
        self.afficher_page("dashboard")

    #Affiche la page des profils.
    def afficher_profils(self):
        self.afficher_page("profils")

    #Affiche la page des prévisions.
    def afficher_previsions(self):
        self.afficher_page("previsions")

    #Ferme les graphiques Matplotlib encore ouverts puis la fenetre.
    def quitter(self):
        plt.close("all")
        self.destroy()
