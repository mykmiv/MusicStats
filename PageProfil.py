import customtkinter as ctk

class PageProfils(ctk.CTkFrame):

    #Initialise la page Profils en enregistrant la collection,
    #en indiquant qu'aucun utilisateur n'est sélectionné et 
    #en créant les éléments visuels de la page.
    def __init__(self, parent, collection):
        ctk.CTkFrame.__init__(self, parent)

        #Enregistre la collection musicale utilisé pour la recherche.
        self.collection = collection

        #Aucun utilisateur n'est sélectionné au départ.
        self.utilisateur_selectionne = None

        #Crée l'interface graphique de la page.
        self.creer_interface()

    #Crée le champ de recherche, le bouton de recherche, les cadres et
    #les étiquettes qui permetteront d'afficher les infos du profil sélectionne.
    def creer_interface(self):

        #Crée et affiche le titre de la page.
        self.titre = ctk.CTkLabel(self, text="Profils des utilisateurs", font=("arial", 28 ,"bold"))
        self.titre.pack(pady=15)

        #Crée un cadre pour la recherche d'un utilisateur.
        self.cadre_recherche = ctk.CTkFrame(self)
        self.cadre_recherche.pack(fill="x", padx=20, pady=10)

        #Crée un champ pour écrire le nom de l'utilisateur recherché.
        self.champ_recherche = ctk.CTkEntry(self.cadre_recherche,placeholder_text="Nom de l'utilisateur")
        self.champ_recherche.pack(pady=10)

        #Crée un bouton qui lance la fonction recherche.
        self.bouton_recherche = ctk.CTkButton(self.cadre_recherche, text="Rechercher", command=self.rechercher_utilisateur)
        self.bouton_recherche.pack(pady=10)

        #Crée une étiquette pour afficher les messages de recherche.
        self.label_message = ctk.CTkLabel(self, text="")
        self.label_message.pack(pady=5)

        #Crée un cadre pour afficher les infos du profil,
        self.cadre_profil = ctk.CTkFrame(self)

        #Crée une étiquette qui indique qu'aucun profil n'est encore sélectionné.
        self.label_profil = ctk.CTkLabel(self.cadre_profil, text="Aucun utilisateur sélectionné")
        self.label_profil.pack(pady=10)
        self.cadre_profil.pack(fill="x", padx=20, pady=10)
        
        #Crée un cadre pour les classements des artistes et des chansons.
        self.cadre_classements = ctk.CTkFrame(self)
        self.cadre_classements.pack(fill="x", padx=20, pady=10)

        #Crée une étiquette pour afficher les artistes préférés.
        self.label_artistes = ctk.CTkLabel(self.cadre_classements, text="", justify="left")
        self.label_artistes.pack(pady=10)

        #Crée une étiquette pour afficher les chansons préférés.
        self.label_chansons = ctk.CTkLabel(self.cadre_classements, text="", justify="left")
        self.label_chansons.pack(pady=10)

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

        

