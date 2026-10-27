from datetime import timedelta

class AnalysateurStatistique:

    def __init__(self, collection):
        self.collection = collection

    def top_artistes(self, collection, n):
        compteur_artistes = {}

        for ecoute in collection.ecoutes:
            artiste = ecoute.chanson.artiste

            if artiste in compteur_artistes:
                compteur_artistes[artiste] += 1
            else:
                compteur_artistes[artiste] = 1

        classement = []

        while len(classement) < n and compteur_artistes > 0:
            artiste_populaire = None
            maximum_ecoutes = 0

            for artiste in compteur_artistes:
                if compteur_artistes[artiste] > maximum_ecoutess:
                    maximum_ecoutes = compteur_artistes[artiste]
                    artiste_populaire = artiste

            classement.append((artiste_populaire, maximum_ecoutes))
            del compteur_artistes[artiste_populaire]

        return classement

    def top_chansons(self, collection, n):
        compteur_chanson = {}

        for ecoute in collection.ecoutes:
            chanson = ecoute.chanson

            if chanson in compteur_chanson:
                compteur_chanson[chanson] += 1
            else:
                compteur_chanson[chanson] = 1

        classement = []

        while len(classement) < n and compteur_chanson > 0:
            chanson_populaire = None
            maximum_ecoutes = 0

            for chanson in compteur_chanson:
                if compteur_chanson[chanson] > maximum_ecoutes:
                    maximum_ecoutes = compteur_chanson[chanson]
                    chanson_populaire = chanson

            classement.append((chanson_populaire, maximum_ecoutes))
            del compteur_chanson[chanson_populaire]

        return classement

    def ecoutes_par_semaine(self, collection):
        compteur_semaines = {}

        for ecoute in collection.ecoutes:
            date = ecoute.date_heure.date()
            debut_semaine = date - timedelta(days=date.weekday())

            if debut_semaine in compteur_semaines:
                compteur_semaines[debut_semaine] += 1
            else:
                compteur_semaines[debut_semaine] = 1

        return compteur_semaines

    def utilisateur_actifs_par_semaine(self, collection, semaines = 4):
        utilisateurs_semaines = {}

        if len(collection.ecoutes) == 0 or semaines <= 0:
            return {}

        derniere_date = collection.ecoutes[0].date_heure.date()

        for ecoute in collection.ecoutes:
            date = ecoute.date_heure.date()

            if date > derniere_date:
                derniere_date = date

        derniere_semaine = derniere_date -timedelta(days=derniere_date.weekday())

        for i in range(semaines):
            debut = derniere_semaine - timedelta(weeks=i)
            utilisateurs_semaines[debut] = set()

        for ecoute in collectio.ecoutes:
            date = ecoute,date_heure.date()
            debut = date - timedelta(days=date.weekday())

            if debut in utilisateurs_semaines:
                utilisateurs_semaines[debut].add(ecoute.utilisateur)

        resultat = {}

        for debut in utilisateurs_semaines:
            resultat[debut] = len(utilisateurs_semaines[debut])

        return resultat

def croissance_utilisateurs(self, collection, semaines = 4):
    donnees = self.utilisateur_actifs_par_semaine(collection, semaines)

    if len(donnees) < 2:
        return None

    dates = list(donnees)
    date.sort()

    semaine_actuelle = dates[-1]
    semaine_precedente = dates[-2]

    actuel = donnees[semaine_actuelle]
    precedent = donnees[semaine_precedente]

    if precedent == 0:
        return None

    croissance = (actuel - precedent) / precedent * 100

    return croissance

def utilisateurs_recurents(self, collection, semaines = 4):
    resultat = []

    if len(collection.ecoutes) == 0 or semaines <= 0:
        return resultat

    derniere_date = collection.ecoutes[0].date_heure.date()

    for ecoute in collection.ecoutes:
        date = ecoute.date_heure.date()

        if date > derniere_date:
            derniere_date = date

    derniere_semaine = derniere_date - timedelta(days=derniere_date.weekday())

    premiere_semaine = derniere_semaine - timedelta(weeks=semaines - 1)

    semaines_utilisateurs = {}

    for ecoute in collection.ecoutes:
        date = ecoute.date_heure.date()
        debut = date - timedelta(days=date.weekday())
        utilisateur = ecoute.utilisateur

        if premiere_semaine <= debut <= derniere_semaine:
            if debut not in semaines_utilisateurs:
                semaines_utilisateurs[utilisateur] = set()

            semaines_utilisateurs[utilisateur].add(debut)

    for utilisateur in semaines_utilisateurs:
        if len(semaines_utilisateurs[utilisateur]) > 2:
            resultat.append(utilisateur)

    return resultat






