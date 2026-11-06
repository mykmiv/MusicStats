import customtkinter as ctk
from PageTableauDeBord import PageTableauDeBord
from PageProfil import PageProfils
from PagePrevision import PagePrevision


class ApplicationMusicStats(ctk.CTk):

    #Initialise la fenetre principale de l'application et conserve
    #les objets qui sont nécessaires aux 3 pages.
    def __init__(self, collection, analyseur, graphiques):
        ctk.CTk.__init__(self)

        #Enregistre les objets nécessaires au fonctionnement de l'application.
        self.collection = collection
        self.analyseur = analyseur
        self.graphiques = graphiques

        #Crée la fenetre principale.
        self.title("MusicStats")
        self.geometry("1100x750")
        self.minsize(850, 600)

        #Crée l'interface et affiche le tableau de bord.
        self.creer_interface()
        self.afficher_page("dashboard")


    #Crée le menu de naviguation et la zone contenat les pages.
    def creer_interface(self):

        #Crée un cadre pour le menu de navigation.
        self.menu = ctk.CTkFrame(self, width=200)
        self.menu.pack(side="left", fill="y", padx=10, pady=10)
        self.menu.pack_propagate(False)

        #Affiche le titre de l'application.
        self.titre = ctk.CTkLabel(self.menu, text="MusicStats", font=("Arial", 26, "bold"))
        self.titre.pack(pady=30)

        #Crée le bouton pour afficher le tableau de bord.
        self.bouton_dashboard = ctk.CTkButton(self.menu, text="Tableau de bord", command=self.afficher_dashboard)
        self.bouton_dashboard.pack(pady=10, padx=10, fill="x")

        #Crée le bouton pour afficher les profils.
        self.bouton_profils = ctk.CTkButton(self.menu, text="Profils", command=self.afficher_profils)
        self.bouton_profils.pack(pady=10, padx=15, fill="x")

        #Crée le bouton pour afficher les prévisions.
        self.bouton_previsions = ctk.CTkButton(self.menu, text="Prévisions", command=self.afficher_previsions)
        self.bouton_previsions.pack(pady=10, padx=15, fill="x")

        #Crée l cadre qui contient les pages.
        self.contenu = ctk.CTkFrame(self)
        self.contenu.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        #Permet aux pages de prendre la zone dispo.
        self.contenu.grid_rowconfigure(0, weight=1)
        self.contenu.grid_columnconfigure(0, weight=1)

        #Crée la page du tableau de bord.
        self.page_dashboard = PageTableauDeBord(self.contenu, self.collection, self.analyseur, self.graphiques)

        #Crée la page des profils.
        self.page_profils = PageProfils(self.contenu, self.collection)

        #Crée la page prevision.
        self.page_previsions = PagePrevision(self.contenu, self.collection)

        #Place les 3 pages au meme endroit.
        self.page_dashboard.grid(row=0, column=0, sticky="nsew")
        self.page_profils.grid(row=0, column=0, sticky="nsew")
        self.page_previsions.grid(row=0, column=0, sticky="nsew")

        #Cache les pages jusqua leur selection.
        self.page_dashboard.grid_remove()
        self.page_profils.grid_remove()
        self.page_previsions.grid_remove()

    #Cache les autres pages et affcihe celle qui est s'electionne.
    def afficher_page(self, page):

        self.page_dashboard.grid_remove()
        self.page_profils.grid_remove()
        self.page_previsions.grid_remove()

        if page == "dashboard":
            self.page_dashboard.grid()

        elif page == "profils":
            self.page_profils.grid()

        elif page == "previsions":
            self.page_previsions.grid()

    #Affiche la page du tableau de brd
    def afficher_dashboard(self):
        self.afficher_page("dashboard")

    #Affiche page des profils.
    def afficher_profils(self):
        self.afficher_page("profils")

    #Affiche page previsions.
    def afficher_previsions(self):
        self.afficher_page("previsions")


    