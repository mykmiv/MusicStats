import os
import sys
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
#Dans l'exe, le CSV est dans le dossier temporaire créé par PyInstaller.
if getattr(sys, "frozen", False):
    DOSSIER_APPLICATION = sys._MEIPASS
else:
    DOSSIER_APPLICATION = os.path.dirname(os.path.abspath(__file__))
CHEMIN_CSV_DEFAUT = os.path.join(DOSSIER_APPLICATION, "donnees.csv")


class ApplicationMusicStats(ctk.CTk):

    #Initialise la fenetre principale, charge le CSV une seule fois
    #et crée les objets partagés par les 3 pages.
    def __init__(self, chemin_csv=CHEMIN_CSV_DEFAUT):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
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
        self.menu = ctk.CTkFrame(self, width=230, corner_radius=12)
        self.menu.pack(side="left", fill="y", padx=(10, 0), pady=10)
        self.menu.pack_propagate(False)

        #Affiche le titre de l'application.
        self.titre = ctk.CTkLabel(self.menu, text="🎵 MusicStats", font=("Arial", 24, "bold"))
        self.titre.pack(pady=(30, 0), padx=20, anchor="w")

        self.sous_titre = ctk.CTkLabel(self.menu, text="Statistiques d'écoute", font=("Arial", 13),
                                       text_color="gray60")
        self.sous_titre.pack(pady=(0, 30), padx=20, anchor="w")

        #Crée les 3 boutons de navigation.
        self.bouton_dashboard = self.creer_bouton_menu("📊   Tableau de bord", self.afficher_dashboard)
        self.bouton_profils = self.creer_bouton_menu("👤   Profils", self.afficher_profils)
        self.bouton_previsions = self.creer_bouton_menu("📈   Prévisions", self.afficher_previsions)

        self.label_infos = ctk.CTkLabel(self.menu, text="Aucune donnée chargée", font=("Arial", 12),
                                        text_color="gray55", justify="left")
        self.label_infos.pack(side="bottom", pady=20, padx=20, anchor="w")

        #Associe chaque nom de page à son bouton.
        self.boutons = {"dashboard": self.bouton_dashboard,
                        "profils": self.bouton_profils,
                        "previsions": self.bouton_previsions}

        #Conserve la couleur normale des boutons pour pouvoir la remettre.
        self.couleur_bouton = "transparent"
        self.couleur_bouton_actif = ctk.ThemeManager.theme["CTkButton"]["fg_color"]

        #Les boutons restent désactivés tant que les données ne sont pas chargées.
        self.activer_menu(False)

    def creer_bouton_menu(self, texte, commande):
        bouton = ctk.CTkButton(self.menu, text=texte, command=commande, height=42, corner_radius=8,
                               anchor="w", font=("Arial", 15), fg_color="transparent",
                               text_color="gray90", hover_color="gray25")
        bouton.pack(pady=4, padx=12, fill="x")
        return bouton

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
        cadre = ctk.CTkFrame(self.contenu, fg_color="transparent")
        cadre.grid(row=0, column=0)
        ctk.CTkLabel(cadre, text="Chargement des données...", font=("Arial", 22, "bold")).pack()
        ctk.CTkLabel(cadre, text=os.path.basename(chemin), font=("Arial", 13), text_color="gray60").pack(pady=5)
        self.label_infos.configure(text="Chargement...")
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

        #Écrit le nombre avec un espace entre les milliers (ex. 50456 devient 50 456).
        nombre_ecoutes = f"{len(self.collection.ecoutes):,}".replace(",", " ")
        self.label_infos.configure(text="📁 " + os.path.basename(chemin) + "\n"
                                   + nombre_ecoutes + " écoutes · "
                                   + str(len(self.collection.utilisateurs)) + " utilisateurs")

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
        self.label_infos.configure(text="Aucune donnée chargée")

        cadre = ctk.CTkFrame(self.contenu, fg_color="transparent")
        cadre.grid(row=0, column=0)

        icone = ctk.CTkLabel(cadre, text="⚠️", font=("Arial", 48))
        icone.pack()

        titre = ctk.CTkLabel(cadre, text="Impossible de charger les données", font=("Arial", 24, "bold"),
                             text_color="#e5675f")
        titre.pack(pady=(5, 15))

        texte = ctk.CTkLabel(cadre, text=message, wraplength=650, justify="center", text_color="gray75")
        texte.pack(pady=10)

        bouton = ctk.CTkButton(cadre, text="📂  Choisir un fichier CSV...", command=self.choisir_fichier,
                               height=40, font=("Arial", 15))
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
                bouton.configure(fg_color=self.couleur_bouton_actif, hover_color=self.couleur_bouton_actif,
                                 font=("Arial", 15, "bold"))
            else:
                bouton.configure(fg_color=self.couleur_bouton, hover_color="gray25", font=("Arial", 15))

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
