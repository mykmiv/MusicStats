import customtkinter as ctk #debut
class PagePrevision(ctk.CTkFrame):###version pas encore propre 
    def __init__(self, master, collection):
        super().__init__(master)
        self.master = master
        self.collection = collection        
        self.type_recherche = "Artiste"
        self.nb_semaines = 1
        self.create_widgets()
    def create_widgets(self):    
        titre = ctk.CTkLabel(self, text="Prévision de popularité")
        titre.grid(row=0, column=0, columnspan=2, padx=20, pady=20)