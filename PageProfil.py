import customtkinter as ctk

class PageProfils(ctk.CTkFrame):

    def __init__(self, parent, collection):
        ctk.CTkFrame.__init__(self, parent)

        self.collection = collection
        self.utilisateur_selectionne = None

        self.creer_interface()

    def creer_interface(self):
        self.titre = ctk.CTkLabel(self, text="Profils des utilisateurs", font=("arial", 28 ,"bold"))
        self.titre.pack(pady=15)

        self.cadre_recherche = ctk.CTkFrame(self)
        self.cadre_recherche.pack(fill="x", padx=20, pady=10)

        self.champ_recherche = ctk.CTkEntry(self.cadre_recherche,placeholder_text="Nom de l'utilisateur")
        self.champ_recherche.pack(pady=10)

        self.bouton_recherche = ctk.CTkButton(self.cadre_recherche, text="Rechercher", command=self.rechercher_utilisateur)
        self.bouton_recherche.pack(pady=10)

        self.label_message = ctk.CTkLabel(self, text="")
        self.label_message.pack(pady=5)

        self.cadre_profil = ctk.CTkFrame(self)
        self.label_profil = ctk.CTkLabel(self.cadre_profil, text="Aucun utilisateur sélectionné")
        self.label_profil.pack(pady=10)
        self.cadre_profil.pack(fill="x", padx=20, pady=10)
        

        self.cadre_classements = ctk.CTkFrame(self)
        self.cadre_classements.pack(fill="x", padx=20, pady=10)

        self.label_artistes = ctk.CTkLabel(self.cadre_classements, text="", justify="left")
        self.label_artistes.pack(pady=10)

        self.label_chansons = ctk.CTkLabel(self.cadre_classements, text="", justify="left")
        self.label_chansons.pack(pady=10)

    def rechercher_utilisateur(self):
        nom = self.champ_recherche.get().strip()

        utilisateur_trouve = None

        for utilisateur in self.collection.utilisateurs:
            if utilisateur.nom.lower() == nom.lower():
                utilisateur_trouve = utilisateur
                break

        if utilisateur_trouve is not None:
            self.label_message.configure(text="")
            self.afficher_profil(utilisateur_trouve)
        else:
            self.utilisateur_selectionne = None
            self.label_message.configure(text="Utilisateur introuvable")
            self.label_profil.configure(text="Aucun utilisateur selectionné")
            self.label_artistes.configure(text="")
            self.label_chansons.configure(text="")

    def afficher_profil(self, utilisateur):
        self.utilisateur_selectionne = utilisateur

        total_ecoutes = utilisateur.nombre_ecoutes()

        texte = ("Utilisateur : " + utilisateur.nom + "\nNombre d'écoutes : " + str(total_ecoutes))

        self.label_profil.configure(text=texte)

        self.afficher_artistes_preferes(utilisateur)
        self.afficher_chansons_preferees(utilisateur)

    def afficher_artistes_preferes(self, utilisateur):
        compteur = {}

        for ecoute in utilisateur.ecoutes:
            nom = ecoute.chanson.artiste.nom

            if nom in compteur:
                compteur[nom] += 1
            else:
                compteur[nom] = 1

        texte = "Top 5 des artistes préférés :\n\n"

        position = 1

        while position <= 5 and len(compteur) > 0:
            artiste_populaire = None
            maximum_ecoutes = 0

            for artiste in compteur:
                if compteur[artiste] > maximum_ecoutes:
                    artiste_populaire = artiste
                    maximum_ecoutes = compteur[artiste]

            texte += (str(position) + ". " + artiste_populaire + " : " + str(maximum_ecoutes) + " ecoutes\n")

            del compteur[artiste_populaire]
            position += 1
        self.label_artistes.configure(text=texte)

    def afficher_chansons_preferees(self, utilisateur):
        compteur = {}

        for ecoute in utilisateur.ecoutes:
            chanson = ecoute.chanson

            cle = (chanson.titre,  chanson.artiste.nom)

            if cle in compteur:
                compteur[cle] += 1
            else:
                compteur[cle] = 1

        texte = "Top 5 des chansons preférées :\n\n"

        position = 1

        while position <= 5 and len(compteur) > 0:
            chanson_populaire = None
            maximum_ecoutes = 0
            
            for chanson in compteur:
                if compteur[chanson] > maximum_ecoutes:
                    maximum_ecoutes = compteur[chanson]
                    chanson_populaire = chanson

            titre = chanson_populaire[0]
            artiste = chanson_populaire[1]

            texte += (str(position) + ". " + titre + " - " + artiste + " : " + str(maximum_ecoutes) + " ecoutes\n")

            del compteur[chanson_populaire]
            position += 1

        self.label_chansons.configure(text=texte)

        

