#!/usr/bin/env python3
import serial, pynitel, os, time, random

m = pynitel.Pynitel(serial.Serial('/dev/serial0', 1200,
    parity=serial.PARITY_EVEN,
    bytesize=7,
    stopbits=serial.STOPBITS_ONE,
    timeout=2))

WIDTH = 40
HEIGHT = 24
NODE_COUNT = 5
IA_INTERVAL = 3  # seconds
TIME_LIMIT = 30  # seconds

# Initialisation
m.home()
m.cursor(False)
m._print(">> PIRATAGE EN COURS <<\r\n")

# Génération de 5 nœuds aléatoires
nodes = []
while len(nodes) < NODE_COUNT:
    x, y = random.randint(5, WIDTH - 5), random.randint(4, HEIGHT - 4)
    if (x, y) not in nodes:
        nodes.append((x, y))

# Statuts : 0 = neutre, 1 = joueur, 2 = IA
statuses = {pos: 0 for pos in nodes}
start_time = time.time()
last_ia_time = start_time
ia_interval = random.randint(3, 6)

# Dessin initial
for (x, y) in nodes:
    m.pos(y, x)
    m.forecolor(m.blanc)
    m._print("O")

# Curseur de l'utilisateur
cursor_x, cursor_y = nodes[0]

def draw_cursor():
    m.pos(cursor_y, cursor_x)
    m.inverse()
    m._print("O")
    m.inverse(False)

def update_display():
    for (x, y), status in statuses.items():
        m.pos(y, x)
        if status == 0:
            m.forecolor(m.blanc)
        elif status == 1:
            m.forecolor(m.vert)
        elif status == 2:
            m.forecolor(m.rouge)
        m._print("O")

draw_cursor()

# Boucle de jeu
while True:
    if time.time() - start_time > TIME_LIMIT:
        m.pos(HEIGHT, 1)
        m._print("Temps écoulé. Échec du piratage.")
        break

    if list(statuses.values()).count(2) >= NODE_COUNT:
        m.pos(HEIGHT, 1)
        m._print("IA a pris le contrôle. Échec du piratage.")
        break
        m.pos(HEIGHT, 1)
        m._print("IA a pris le contrôle. Échec du piratage.")
        break

    if list(statuses.values()).count(1) >= NODE_COUNT:
        m.pos(HEIGHT, 1)
        m._print("Succès ! Accès au serveur accordé.")
        break

    m.pos(HEIGHT, 1)
    m._print("Noeuds Joueur: %d / IA: %d       " % (
        list(statuses.values()).count(1),
        list(statuses.values()).count(2)
    ))

    m.cursor(True)
    m.pos(cursor_y, cursor_x)
    (cmd, touche) = m.input(cursor_y, cursor_x, 0, '', redraw=True)
    m.cursor(False)

    if touche == m.retour:
        os.execv("/usr/bin/python3", ["python3", "police_menu.py"])

    if (cursor_x, cursor_y) in statuses and statuses[(cursor_x, cursor_y)] == 0:
        statuses[(cursor_x, cursor_y)] = 1
        update_display()

    if touche == m.haut and cursor_y > 1:
        cursor_y -= 1
    elif touche == m.bas and cursor_y < HEIGHT:
        cursor_y += 1
    elif touche == m.gauche and cursor_x > 1:
        cursor_x -= 1
    elif touche == m.droite and cursor_x < WIDTH:
        cursor_x += 1

    # Tour de l'IA
    if time.time() - last_ia_time >= ia_interval:
        for pos in statuses:
            if statuses[pos] == 0:
                statuses[pos] = 2
                break
        update_display()
        last_ia_time = time.time()
        ia_interval = random.randint(3, 6)

