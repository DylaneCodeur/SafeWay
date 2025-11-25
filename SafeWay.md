🧠 1. Description générale du projet

Nom du projet : SafeWay
Type : Système d’assistance à la conduite basé sur l’IA et la caméra
But principal :
SafeWay est un système d’IA qui surveille en temps réel l’état du conducteur à l’aide de la caméra (PC, tablette, téléphone) et détecte les signes de fatigue, distraction et comportements dangereux, afin de prévenir les accidents.

SafeWay doit fonctionner en temps réel, localement sur l’appareil (sans envoyer les vidéos au cloud), et déclencher des alertes visuelles et sonores dès qu’un risque est détecté.

🎯 2. Problème à résoudre

De nombreux accidents sont causés par :

Somnolence au volant (yeux fermés, tête qui tombe)

Fatigue (bâillements, baisse d’attention)

Distraction (regard sur le téléphone, ailleurs que sur la route)

Utilisation du téléphone pendant la conduite

Les véhicules récents haut de gamme ont des systèmes de surveillance du conducteur, mais :

ils sont chers,

inaccessibles à la majorité des conducteurs (Afrique, Turquie, etc.),

inexistants pour les taxis, bus, motos et véhicules anciens.

SafeWay veut apporter une solution low-cost, accessible et portable, qui fonctionne simplement avec une caméra et une IA.

🚗 3. Utilisation prévue de SafeWay

Scénario de base :

Le conducteur pose son téléphone ou une tablette face à lui (sur le tableau de bord).

Il lance l’application SafeWay.

SafeWay active la caméra frontale.

L’IA analyse en temps réel :

son visage,

ses yeux,

sa bouche,

sa tête,

ses mains,

la présence d’un téléphone.

En cas de comportement dangereux, SafeWay déclenche immédiatement :

une alarme sonore,

une notification visuelle,

un message vocal (ex : « Attention, somnolence détectée »).

SafeWay enregistre aussi un historique des alertes pour analyse.

🧩 4. Fonctionnalités principales (Core Features)
4.1 Détection en temps réel via caméra

Ouvrir la caméra (webcam, caméra frontale appareil).

Lire les images image par image (frames).

Traitement en temps réel (objectif : minimum 15 FPS).

4.2 Détection du visage et du regard (avec IA)

L’IA doit détecter :

Position du visage (présent / absent).

Position de la tête :

tête droite

tête penchée (somnolence possible)

tête tournée longtemps à gauche/droite (distraction)

Direction du regard (regarde la route / regarde ailleurs).

4.3 Détection de l’état des yeux

Yeux ouverts

Yeux fermés

Clignements normaux versus prolongés

Fermeture des yeux > X millisecondes = suspicion de somnolence

4.4 Détection de la bouche

Bouche fermée

Bouche ouverte (bâillement)

Bâillements répétés = fatigue

4.5 Détection des mains / gestes

Main sur le volant / dans le champ

Main absente du volant longtemps

Détection de certains gestes (optionnel, version avancée) :

main tenant un téléphone

main devant le visage (distraction)

4.6 Détection du téléphone

Utilisation d’un modèle type YOLO pour détecter :

téléphone dans la main du conducteur

téléphone proche du visage

Si téléphone détecté pendant la conduite → alerte.

4.7 Détection de l’absence du conducteur

Si le visage disparaît complètement du champ de la caméra pendant un certain temps → alerte “conducteur absent”.

🚨 5. Système d’alertes

SafeWay doit déclencher différents types d’alertes selon la gravité.

5.1 Types d’alertes

Alerte visuelle : texte sur l’écran (rouge, clignotant)

Alerte sonore : bip/buzzer

Alerte vocale : message audio (ex : "Attention, somnolence détectée")

5.2 Règles d’alerte

Exemples de règles :

Yeux fermés > 1,5 seconde → alerte “Somnolence détectée”.

Bâillements 3 fois en 60 secondes → alerte “Fatigue détectée”.

Regard hors route > 2 secondes → alerte “Distraction détectée”.

Téléphone détecté → alerte “Téléphone détecté, danger”.

Absence de visage > 3 secondes → alerte “Conducteur absent”.

5.3 Historique des alertes

Chaque alerte doit être enregistrée avec :

type d’alerte

timestamp

éventuellement un score de gravité

Stockage possible : fichier JSON, CSV ou petite base (SQLite).

🏗 6. Architecture technique souhaitée

SafeWay doit être structuré proprement pour que Cursor puisse générer, organiser et améliorer le code.

6.1 Langage et bibliothèques

Langage principal IA : Python

Bibliothèques principales :

opencv-python → gestion de la caméra et des images

mediapipe → détection du visage, main, pose, yeux, bouche

ultralytics (YOLOv8 ou YOLO11) → détection d’objets (ex : téléphone)

numpy → opérations math

pygame ou autre pour jouer sons / alarmes (ou playsound)

Version future :

Export possible du modèle vers onnx ou tflite pour mobile (Flutter, etc.).