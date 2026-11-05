import customtkinter as ctk #debut
import tkinter as tk
from Collection import CollectionMusicale
from PrevisionPopularite import PrevisionPopularite

class PagePrevision(ctk.CTkFrame): 
    def __init__(self, master, collection):
        super().__init__(master)
        self.master = master
        self.collection = collection        
        self.type_recherche = tk.StringVar(value="Artiste")        #Valeur depart quand la page souvre, ca va etre artiste
        self.create_widgets()
    def create_widgets(self):    
        #Initialise la grille
        self.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        #nom de l'artiste
        self.nom_entry = ctk.CTkEntry(self,placeholder_text = "Entrez le nom de l'ariste ou de la chanson")  #contient nom artiste
        self.nom_entry.grid(row=1, column =0, padx = 20, pady = (20,10))

        #choix artiste et chanson
        self.artiste_rb = ctk.CTkRadioButton(self,text= "Artiste", variable=self.type_recherche, value = "Artiste") #pourquoi bug affichage
        self.artiste_rb.grid(row=2, column = 0, padx = 20, pady = (20,10))
        self.chanson_rb = ctk.CTkRadioButton(self, text = "Chanson", variable = self.type_recherche, value= "Chanson")
        self.chanson_rb.grid(row = 3, column =0, padx = 20, pady = (20,10)) #choix artiste et chanson un en dessous de lautre meme colonne

        self.prevoir_boutton = ctk.CTkButton(self, text = "Prévoir", command= self.afficher_previsions) #bouton interactif qui affiche previsions, afficher_prevision a faire
        self.prevoir_boutton.grid(row=4,column=0,padx=20, pady =(10,10))
        #titre de la page
        self.titre_label = ctk.CTkLabel(self, text="Prévision de popularité")
        self.titre_label.grid(row=0, column=0, padx=20, pady=20)
        #Resultat de la recherche par utilisateur
        self.resultat_label = ctk.CTkLabel(self, text="")   #Initialise resultat avec chaine carateres vide, lorsque que Utilisateur pese sur boutton, la, le texte apparait 
        self.resultat_label.grid(row=5, column=0, padx=20, pady=(10, 20))
    def rechercher_element(self,nom):
        """Cela retourne l'artiste ou la chanson qui porte ce nom"""
        if self.type_recherche.get() == "Artiste":
            return self.collection.trouver_artiste(nom)        #si aucun artiste trouve, trouver_artiste retourne deja None
        if self.type_recherche.get() == "Chanson":
            for chanson in self.collection.chansons.values(): #juste les valeurs, cest les objets chanson
                if chanson.titre == nom:
                    return chanson  
        return None #si aucune correspondance
    def afficher_previsions(self):
        nom = self.nom_entry.get()
        element = self.rechercher_element(nom)
        if element == None:
            self.resultat_label.configure(text="Nous n'avons pas trouvé votre chanson/artiste")##
            return
        prevision = PrevisionPopularite()
        prevision.preparer_donnees(self.collection) #On prepare le tableau des ecoutes
        historique = prevision.part_ecoutes(element, 9) #On regarde les 9 dernieres semaines pour prevoir la prochaine semaine
        futur = prevision.regression(historique, 1) #On prevoit 1 semaine plus tard
        sem_actuel = historique[-1] 


        
