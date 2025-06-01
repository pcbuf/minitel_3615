import csv

def run(minitel):
    minitel.clear()
    minitel.goto(1, 1)
    minitel.print("3615 ANNU - Recherche")
    minitel.goto(3, 1)
    minitel.print("Champ (NOM, LOCALITE, etc) : ")
    champ = minitel.saisie(15).upper()

    minitel.goto(5, 1)
    minitel.print("Valeur recherchée : ")
    valeur = minitel.saisie(20).lower()

    minitel.clear()
    try:
        with open("annu.csv", newline="") as f:
            reader = csv.DictReader(f)
            y = 1
            found = False
            for row in reader:
                if champ in row and valeur in row[champ].lower():
                    minitel.goto(y, 1)
                    minitel.print(f"{row['PRENOM']} {row['NOM']} - {row['RUBRIQUE']}")
                    y += 1
                    found = True
                    if y > 22:
                        break
            if not found:
                minitel.goto(1, 1)
                minitel.print("Aucun résultat.")
    except:
        minitel.goto(1, 1)
        minitel.print("Fichier annu.csv introuvable.")
    minitel.saisie(1)
