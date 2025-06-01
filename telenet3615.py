import serial
import pynitel
import time
from services import ulla, annu, police

def display_home(minitel):
    minitel.home()
    minitel.clear()
    minitel.curseur(False)

    minitel.couleur(minitel.blanc, minitel.noir)
    minitel.goto(1, 1)
    minitel.print(" *p")  # Mode graphique
    minitel.goto(2, 1)
    minitel.print("Télétel 3615")

    minitel.goto(4, 1)
    minitel.couleur(minitel.bleu, minitel.noir)
    minitel.print(" 0,12F à la connexion, puis :")
    minitel.goto(5, 1)
    minitel.couleur(minitel.rouge, minitel.noir)
    minitel.print(" prix total en F/min TTC ")

    minitel.couleur(minitel.blanc, minitel.noir)
    lignes = [
        "t2   0.37   t32  0.85   t36  1.29",
        "t23  0.45   t34  1.01   t44  2.23",
        "t22: 0.45 (avantages horaires)",
        "dont F.TELECOM 0.12 à 0.50F/min",
        "vers les DOM, ajouter 0.33F/min",
        "facturation par Unités Télécom",
        "indivisibles de 0.74F TTC"
    ]
    for i, l in enumerate(lignes):
        minitel.goto(6 + i, 1)
        minitel.print(l)

    minitel.goto(14, 1)
    minitel.print("code du service : ....................")
    minitel.goto(15, 32)
    minitel.print("[Envoi]")

    minitel.goto(18, 1)
    minitel.print("ANNUAIRE DES SERVICES")
    minitel.goto(19, 1)
    minitel.print("et tarifs Télétel")
    minitel.goto(20, 1)
    minitel.print("affichage du prix")
    minitel.goto(21, 1)
    minitel.print("fin")

    minitel.goto(21, 30)
    minitel.print("Sommaire")
    minitel.goto(22, 30)
    minitel.print("Cx/Fin")

def main():
    minitel = pynitel.Pynitel(serial.Serial('/dev/serial0', 1200, timeout=1))
    while True:
        display_home(minitel)
        minitel.goto(14, 22)
        code = minitel.saisie(8)
        if not code:
            continue
        code = code.upper()
        if code == "ULLA":
            ulla.run(minitel)
        elif code == "ANNU":
            annu.run(minitel)
        elif code == "POLICE":
            police.run(minitel)
        else:
            minitel.goto(16, 1)
            minitel.print("Service inconnu...")
            time.sleep(2)

if __name__ == "__main__":
    main()
