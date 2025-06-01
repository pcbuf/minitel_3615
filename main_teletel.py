#!/usr/bin/env python3

import serial
import pynitel

m = None

def init():
    """Initialisation du Minitel avec les bons paramètres"""
    global m
    m = pynitel.Pynitel(serial.Serial(
        '/dev/serial0',
        baudrate=1200,
        bytesize=7,
        parity=serial.PARITY_EVEN,
        stopbits=serial.STOPBITS_ONE,
        timeout=2
    ))
    return m

def page_accueil():
    """Affichage de la page d'accueil TELENET 3615 (fixe, pixel près)"""
    global m
    m.home()
    m.cursor(False)

    # Haut de page - logo et Télé tel 3615
    m.pos(1, 1)
    m.color(m.blanc)
    m._print(" ")
    m.pos(1, 5)
    m.backcolor(m.bleu)
    m.color(m.blanc)
    m._print("Télétel")
    m.pos(1, 33)
    m._print("3615")

    # Tarifs
    m.backcolor(m.noir)
    m.color(m.blanc)
    m.pos(3, 5)
    m._print("0,12F à la connexion, puis:")
    m.pos(4, 5)
    m.backcolor(m.rouge)
    m._print("prix total en F/min TTC")

    lignes_tarif = [
        ("t2", "0.37"),
        ("t23", "0.45"),
        ("t22", "0.45 (avantages horaires)"),
        ("t32", "0.85"),
        ("t34", "1.01"),
        ("t36", "2.29"),
        ("t44", "2.23")
    ]
    row = 5
    for (code, prix) in lignes_tarif:
        m.pos(row, 6)
        m._print(f"{code} : {prix}")
        row += 1

    m.pos(row, 5)
    m._print("dont F. TELECOM 0,12 à la connexion")
    row += 1
    m.pos(row, 5)
    m._print("vers les DOM, ajouter 0,33F/min")
    row += 1
    m.pos(row, 5)
    m._print("facturation par Unités Télécom")
    row += 1
    m.pos(row, 5)
    m._print("indivisibles de 0,74F TTC")

    # Zone de saisie : code service
    m.resetzones()
    m.pos(18, 5)
    m._print("code du service:")
    m.zone(18, 25, 8, '', m.jaune)

    # Bas de page
    m.pos(22, 1)
    m._print("ANNUAIRE DES SERVICES")
    m.pos(23, 1)
    m._print("et tarifs Télétel")
    m.pos(24, 1)
    m._print("affichage du prix      fin")

    m.pos(21, 32)
    m._print("Envoi")
    m.pos(22, 32)
    m.inverse()
    m._print("Guide")
    m.inverse(False)
    m.pos(23, 32)
    m.color(m.vert)
    m._print("Sommaire")
    m.pos(24, 32)
    m.color(m.blanc)
    m._print("Cx/Fin")

    m.cursor(True)
    (zone, touche) = m.waitzones(1)

    # Code saisi (sans effet pour le moment)
    code = m.zones[0]['texte'].strip().upper()
    if touche == m.envoi and code in ['ULLA', 'ANNU', 'POLICE']:
        m.message(0, 1, 2, f"Code {code} reconnu (pas encore actif)", bip=True)
    elif touche == m.envoi:
        m.message(0, 1, 2, "Code inconnu", bip=True)
    elif touche == m.sommaire:
        m.message(0, 1, 2, "Retour sommaire", bip=True)
    elif touche == m.guide:
        m.message(0, 1, 2, "Guide non disponible", bip=True)

if __name__ == '__main__':
    init()
    while True:
        page_accueil()
