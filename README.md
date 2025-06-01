# Projet TELENET 3615

Simulation d’un portail Minitel classique avec 3 services :
- **3615 ULLA** : site factice sans interaction
- **3615 ANNU** : recherche dans un annuaire local depuis un fichier CSV
- **3615 POLICE** : portail réservé, sans fonction (pour l’instant)

## Démarrage

```bash
python3 telenet.py
```

## Démarrage automatique (optionnel)

Créer un service systemd ou ajouter dans `.bashrc`.

## annu.csv

Fichier CSV avec les colonnes :
```
NOM,RUBRIQUE,LOCALITE,DEPARTEMENT,ADRESSE,PRENOM
```

## Roadmap

- Ajouter des mini-jeux dans POLICE
- Améliorer l'affichage avec gestion du clignotement Minitel
