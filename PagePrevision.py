import customtkinter as ctk #debut
import tkinter as tk
from Collection import CollectionMusicale
from PrevisionPopularite import PrevisionPopularite
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
class PagePrevision(ctk.CTkFrame): 
    def __init__(self, master, collection):
        super().__init__(master)
        self.master = master
        self.collection = collection        
        self.type_recherche = tk.StringVar(value="Artiste")   #Valeur depart quand la page souvre, ca va etre artiste
        self.zone_du_graph = None  # pas encore de graphique au départ
        self.create_widgets()
    def create_widgets(self):    
    
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
        prevision.preparer_donnees(self.collection) #On prepare le tableau des ecoutes, cela fait la colonne semaine dans prevision et sans cela, on pourrait pas regarder les 9 dernieres semaines
        historique = prevision.part_ecoutes(element, 9) #On regarde les 9 dernieres semaines pour prevoir la prochaine semaine
        futur = prevision.regression(historique, 1) #On prevoit 1 semaine plus tard

        if len(futur) == 0: #La methode regression() retourne tableau vide si il y a moins de 4 semaines
            self.resultat_label.configure(text="Il n'y a pas assez de semaines pour faire la prévision") #Si le nombre de semaines est plus petit que 4
            return ##On sort, aucune prévision à afficher
        sem_actuel = round(historique[-1], 1) #Sinon le nombre de decimale est trop grand, exemple= 3,14232312134532, donc arrondit 1 chiffre après la virgule
        sem_prevue = round(futur[-1], 1)    #La même raison pour les décimales
        self.resultat_label.configure(text=f"Actuel : {sem_actuel} %   Prévu : {sem_prevue} %")

        #Creer le graphique des previsions
        plt.figure(figsize=(6, 4))
        plt.plot(range(len(historique)), historique, label="Semaines passées", color="blue")   #Les semaines déjà passées
        plt.plot(len(historique), futur[0],marker = "o", label="Prévision", color="red")  #La prediction
        plt.title("Part d'écoute par semaine")
        plt.xlabel("Semaine")
        plt.ylabel("Part d'écoute (%)")
        plt.legend(loc = "lower right")
        #Mettre le graphique dans la page
        self.zone_du_graph = FigureCanvasTkAgg(plt.gcf(), master=self)  #gcf == get current figure, comme dans tp CTk, section matplotlib
        self.zone_du_graph.draw()   #dessine le graph
        self.zone_du_graph.get_tk_widget().grid(row=6, column=0, pady=(10, 10)) #place le graph dans la page




        
