#coding:utf8

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

def listedesterritoires(territoiretest, exportationUSD, importationUSD):
    listedesterritoires = [[territoiretest[0], 0]]
    pos = 0
    for element in range(0,len(territoiretest)):
        if territoiretest[element] != listedesterritoires[pos][0]:
            listedesterritoires.append([territoiretest[element], element])
            pos += 1
    lignes = []
    for element in range(1,len(listedesterritoires)):
        lignes.append(listedesterritoires[element][1] - 1)
    lignes.append(len(territoiretest))
    liste = []
    for element in range(0,len(listedesterritoires)):
        liste.append([listedesterritoires[element][0], listedesterritoires[element][1], lignes[element]])
    totalparterritoire = []
    for element in range(0,len(liste)):
        totalparterritoire.append([liste[element][0], exportationUSD[liste[element][1]:liste[element][2]].sum(), importationUSD[liste[element][1]:liste[element][2]].sum()])
    return totalparterritoire

def nettoyage(colonne):
    colonne2 = []
    for element in colonne:
        if element == 'Sans objet' or element =='-':
            colonne2.append(float(0))
        else:
            colonne2.append(float(element))
    return colonne2

def getliste(territoiretest):
    listedesterritoires = [[territoiretest[0], 0]]
    pos = 0
    for element in range(0,len(territoiretest)):
        if territoiretest[element] != listedesterritoires[pos][0]:
            listedesterritoires.append([territoiretest[element], element])
            pos += 1
    lignes = []
    for element in range(1,len(listedesterritoires)):
        lignes.append(listedesterritoires[element][1] - 1)
    lignes.append(len(territoiretest))
    liste = []
    for element in range(0,len(listedesterritoires)):
        liste.append([listedesterritoires[element][0], listedesterritoires[element][1], lignes[element]])
    return liste

# Question 4
print("Question 4")
# Source des données : https://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=37
with open("./data/Afrique-2024.csv", "r", encoding="utf-8") as fichier:
    contenu = pd.read_csv(fichier)

print(contenu)

# Question 5
print("Question 5")
print(len(contenu))
print(len(contenu.columns))

# Question 6
print("Question 6")
print(contenu.head())

# Question 7
print("Question 7")
print(contenu.dtypes)

# Question 8
print("Question 8")
print(contenu["export_ton"])
print(contenu["import_ton"])

# Contenu des colonnes
# "year" : année
# "origin_id" : territoire de référence
# "dest_id" : territoire partenaire
# "Dist_VO (km)" : distance intercentroïde entre les deux territoires
# "hs92_Section_id" : code Section du produit
# "hs92_HS02_id" : code 2-digit du produit
# "hs92_HS04_id" : code 4-digit du produit
# "hs92_HS06_id" : code 6-digit du produit
# "export_val" : valeur des exportations du territoire de référence vers le territoire partenaire en dollars courants
# "import_val" : valeur des importations du territoire partenaire vers le territoire de référence en dollars courants
# "export_ton" : valeur des exportations du territoire de référence vers le territoire partenaire en tonnes
# "import_ton" : valeur des importations du territoire partenaire vers le territoire de référence en tonnes

# Question 9
print("Question 9")
export_ton = contenu["export_ton"]
import_ton = contenu["import_ton"]

# Question 10
print("Question 10")
effectif_export = 0
effectif_import = 0

for element in export_ton:
    if element != "-":
        effectif_export += 1

for element in import_ton:
    if element != "-":
        effectif_import += 1

print(effectif_export)
print(effectif_import)

# Question 11
print("Question 11")

origin_id = contenu["origin_id"]
export_val = contenu["export_val"]
import_val = contenu["import_val"]

totalparterritoire = listedesterritoires(origin_id, export_val, import_val)

territoires = []

for element in totalparterritoire:
    territoires.append(element[0])

for element in totalparterritoire:
    codeiso = element[0]
    exportation = element[1]
    importation = element[2]

    valeurs = [exportation, importation]
    noms = ["Exportations", "Importations"]

    plt.bar(noms, valeurs)
    plt.title(codeiso)
    plt.savefig("./img/" + codeiso + ".png")
    plt.close()

# Questions 12 et 14
print("Questions 12 et 14")

# Application de la fonction nettoyage(...) sur les colonnes
distance = nettoyage(contenu["Dist_VO (km)"])
export_val_2 = nettoyage(contenu["export_val"])
import_val_2 = nettoyage(contenu["import_val"])
export_ton_2 = nettoyage(contenu["export_ton"])
import_ton_2 = nettoyage(contenu["import_ton"])

# Liste des territoires
liste = getliste(contenu["origin_id"])

# Nouveau DataFrame avec les données nettoyées
donnees2titre = ["distance", "export_val_2", "import_val_2", "export_ton_2", "import_ton_2"]

donnees2 = pd.DataFrame({
    "distance": distance,
    "export_val_2": export_val_2,
    "import_val_2": import_val_2,
    "export_ton_2": export_ton_2,
    "import_ton_2": import_ton_2
})

# Calcul des paramètres statistiques
parametres = []
quartiles = []
deciles = []

for element in range(0,len(donnees2.columns)):
    parametres2 = []
    distanceinterquartile = []
    distanceinterdecile = []

    for element2 in range(0,len(liste)):
        codeiso = liste[element2][0]
        data2 = donnees2.iloc[liste[element2][1]:liste[element2][2],element]

        moyenne = data2.mean().round(decimals=2)
        mediane = data2.median().round(decimals=2)
        mode = data2.mode()[0].round(decimals=2)
        ecarttype = data2.std().round(decimals=2)
        ecartabsolumoyen = np.abs(data2 - moyenne).mean().round(decimals=2)
        etendue = (data2.max() - data2.min()).round(decimals=2)

        parametres2.append([codeiso, moyenne, mediane, mode, ecarttype, ecartabsolumoyen, etendue])

        quartile = data2.quantile([0.25, 0.75])
        distanceinterquartile.append([codeiso, (quartile[0.75] - quartile[0.25]).round(decimals=2)])

        decile = data2.quantile([0.1, 0.9])
        distanceinterdecile.append([codeiso, (decile[0.9] - decile[0.1]).round(decimals=2)])

    parametres.append(parametres2)
    quartiles.append(distanceinterquartile)
    deciles.append(distanceinterdecile)
#     for element2 in range(0,len(liste)):
#         codeiso = liste[element2][0]
#         data2 = donnees2.iloc[liste[element2][1]:liste[element2][2],element]

#         moyenne = 
#         mediane = 
#         mode = 
#         ecarttype = 
#         ecartabsolumoyen = 
#         etendue = 
#         parametres2.append([codeiso, moyenne, mediane, mode, ecarttype, ecartabsolumoyen, etendue])

#         quartile = 
#         distanceinterquartile.append([codeiso, (quartile[0.75] - quartile[0.25]).round(decimals=2)])
#         decile = 
#         distanceinterdecile.append([codeiso, (decile[0.9] - decile[0.1]).round(decimals=2)])
#     parametres.append(parametres2)
#     quartiles.append(distanceinterquartile)
#     deciles.append(distanceinterdecile)

# Question 13
print("Question 13")
print(parametres)

# Question 14
print("Question 14")
print(quartiles)
print(deciles)

# Question 15
print("Question 15")

for element in range(0,len(donnees2.columns)):
    plt.figure()
    plt.boxplot(donnees2.iloc[:,element])
    plt.title(donnees2titre[element])
    plt.savefig("./img/boxplot_" + donnees2titre[element] + ".png")
    plt.close()

# Question 16
print("Question 16")

distance2 = nettoyage(contenu["Dist_VO (km)"])

intervalles = [0, 0, 0, 0, 0, 0, 0, 0]

for element in distance2:
    if element > 0 and element <= 2500:
        intervalles[0] += 1
    elif element > 2500 and element <= 5000:
        intervalles[1] += 1
    elif element > 5000 and element <= 7500:
        intervalles[2] += 1
    elif element > 7500 and element <= 10000:
        intervalles[3] += 1
    elif element > 10000 and element <= 12500:
        intervalles[4] += 1
    elif element > 12500 and element <= 15000:
        intervalles[5] += 1
    elif element > 15000 and element <= 17500:
        intervalles[6] += 1
    elif element > 17500 and element <= 20000:
        intervalles[7] += 1

print(intervalles)

nomsintervalles = ["0-2500", "2500-5000", "5000-7500", "7500-10000",
                   "10000-12500", "12500-15000", "15000-17500", "17500-20000"]

plt.figure()
plt.bar(nomsintervalles, intervalles)
plt.xticks(rotation=45)
plt.title("Répartition des distances")
plt.xlabel("Distance (km)")
plt.ylabel("Effectif")
plt.tight_layout()
plt.savefig("./img/histogramme_distances.png")
plt.close()

# Question bonus
print("Question bonus")
