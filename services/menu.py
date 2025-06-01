from services.ulla import afficher_ulla
from services.annu import afficher_annu
from services.police import afficher_police

def afficher_menu():
    while True:
        print("\n" * 2)
        print("         ┌───────────────────────────────┐")
        print("         │     BIENVENUE SUR 3615        │")
        print("         │           TELENET              │")
        print("         └───────────────────────────────┘")
        print("\nChoisissez un service :")
        print("1 - ULLA")
        print("2 - ANNU")
        print("3 - POLICE")
        print("0 - Quitter\n")

        choix = input("> ")
        if choix == "1":
            afficher_ulla()
        elif choix == "2":
            afficher_annu()
        elif choix == "3":
            afficher_police()
        elif choix == "0":
            print("\nDéconnexion...")
            break
        else:
            print("\nChoix invalide.")
