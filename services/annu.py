import csv

def afficher_annu():
    print("\nANNUNET - Recherche Annuaire")
    print("Champs disponibles : NOM, RUBRIQUE, LOCALITE, DEPARTEMENT, ADRESSE, PRENOM\n")
    champ = input("Champ : ").upper()
    valeur = input("Valeur : ").lower()

    try:
        with open("annu.csv", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            resultats = [row for row in reader if row.get(champ, '').lower() == valeur]

            if resultats:
                print("\nRésultats :")
                for r in resultats:
                    print(" - ", ", ".join(f"{k}: {v}" for k, v in r.items()))
            else:
                print("Aucun résultat.")
    except FileNotFoundError:
        print("annu.csv introuvable.")

    input("\nAppuyez sur ENTREE pour revenir.")
