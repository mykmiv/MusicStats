# Étape 1 : examiner les données ListenBrainz avant de créer les classes

import pandas as pd

df = pd.read_csv("donnees/ecoutes.csv")

print("Nombre de lignes :", len(df))
print("\nColonnes :", list(df.columns))
print("\nPremières lignes :")
print(df.head())

# 2. Valeurs manquantes par colonne
print("\nValeurs manquantes :")
print(df.isna().sum())

#Gestion du temps
df["date_heure"] = pd.to_datetime(df["listened_at"], unit="s")
print("\nPremière écoute :", df["date_heure"].min())
print("Dernière écoute :", df["date_heure"].max())

secondes_par_semaines = 7 * 24 * 3600
df["semaine"] = (df["listened_at"] - df["listened_at"].min()) // secondes_par_semaines
print("\nÉcoutes par semaine (0 = la plus ancienne) :")
print(df["semaine"].value_counts().sort_index())

#Quantité de chaque
print("\nUtilisateurs :", len(df["user_name"].value_counts()))
print("Artistes :", len(df["artist_name"].value_counts()))
print("Chansons :", len(df["track_name"].value_counts()))
