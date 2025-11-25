# 🚗 SafeWay - Système d'assistance à la conduite basé sur l'IA

> **Réalisé par [dylanecodeur](https://github.com/dylanecodeur)**

## 📋 Description du projet

**SafeWay** est un système d'intelligence artificielle avancé conçu pour améliorer la sécurité routière en surveillant en temps réel l'état du conducteur. Le système utilise la caméra de l'appareil (ordinateur, tablette ou téléphone) pour détecter automatiquement les signes de fatigue, de distraction et les comportements dangereux, déclenchant des alertes immédiates pour prévenir les accidents.

### 🎯 Problématique

Les accidents de la route causés par la fatigue, la distraction ou l'utilisation du téléphone au volant représentent un problème majeur de sécurité publique. Les systèmes de surveillance du conducteur existants dans les véhicules haut de gamme sont :

- 💰 **Chers** : Inaccessibles pour la majorité des conducteurs
- 🌍 **Géographiquement limités** : Principalement disponibles dans les pays développés
- 🚫 **Inexistants** : Absents pour les taxis, bus, motos et véhicules anciens

**SafeWay** apporte une solution **low-cost, accessible et portable** qui fonctionne simplement avec une caméra et une IA, rendant la sécurité routière accessible à tous.

## ✨ Fonctionnalités principales

### 🔍 Détection en temps réel

- **Détection du visage** : Identification précise du visage du conducteur
- **Analyse des yeux** : Détection de l'état des yeux (ouverts/fermés)
- **Analyse de la bouche** : Détection des bâillements (signe de fatigue)
- **Position de la tête** : Suivi de l'orientation de la tête
- **Détection des mains** : Identification des gestes et positions
- **Détection d'objets** : Utilisation de YOLOv11 pour détecter les téléphones

### 🚨 Système d'alertes intelligent

#### Types d'alertes détectées :

1. **Somnolence** ⚠️
   - Yeux fermés > 1.2 secondes
   - Message : "Veillez à ne pas dormir au volant, restez vigilant"

2. **Fatigue** 😴
   - 2+ bâillements en 60 secondes
   - Taux de clignement anormalement bas
   - Message : "Signes de fatigue détectés, faites une pause si nécessaire"

3. **Distraction** 👀
   - Regard détourné > 1.5 secondes
   - Mouvements excessifs de la tête
   - Message : "Vous ne regardez pas devant vous, concentrez-vous sur la route"

4. **Téléphone au volant** 📱
   - Détection d'un téléphone dans les mains
   - Message : "Veuillez ne pas utiliser le téléphone au volant"

5. **Conducteur absent** 🚫
   - Visage absent du champ de vision > 2.5 secondes
   - Message : "Conducteur absent, veuillez reprendre le contrôle du véhicule"

#### Modes d'alerte :

- **Visuel** : Messages clignotants à l'écran avec codes couleur
- **Sonore** : Bips d'alerte selon la sévérité
- **Vocal** : Synthèse vocale en français avec messages personnalisés

### 🔒 Confidentialité et sécurité

- ✅ **100% traitement local** : Aucune vidéo n'est envoyée au cloud
- ✅ **Données privées** : Toutes les analyses sont effectuées sur l'appareil
- ✅ **Open-source** : Code source entièrement accessible et auditable

## 🛠️ Technologies utilisées

### Bibliothèques principales

- **OpenCV** (4.8+) : Traitement vidéo et manipulation d'images
- **MediaPipe** (0.10+) : Détection du visage, des mains et analyse des landmarks
- **Ultralytics YOLOv11** : Détection d'objets ultra-performante
- **NumPy** : Calculs mathématiques et manipulation de tableaux
- **PyGame** : Génération et lecture de sons d'alerte
- **pyttsx3** : Synthèse vocale (Text-to-Speech)

### Architecture IA

- **MediaPipe Face Mesh** : 468 points de repère faciaux pour analyse précise
- **YOLOv11** : Modèle de détection d'objets state-of-the-art
- **Algorithmes personnalisés** : EAR (Eye Aspect Ratio), MAR (Mouth Aspect Ratio)

## 📦 Installation

### Prérequis

- Python 3.8 ou supérieur
- Caméra (webcam, caméra frontale)
- 2GB+ RAM recommandé
- macOS, Linux ou Windows

### Étapes d'installation

1. **Cloner le repository**

```bash
git clone https://github.com/dylanecodeur/SafeWay.git
cd SafeWay/safeway
```

2. **Installer les dépendances**

```bash
pip install -r requirements.txt
```

3. **Télécharger les modèles**

Les modèles MediaPipe sont téléchargés automatiquement au premier lancement.

Pour YOLOv11 :
```bash
python3 download_yolo11.py
```

4. **Lancer SafeWay**

```bash
python3 ui/cli_demo.py
```

## 🎮 Utilisation

### Lancement de base

```bash
cd safeway
python3 ui/cli_demo.py
```

### Contrôles

- **'q'** : Quitter l'application
- La caméra s'ouvre automatiquement
- Les alertes apparaissent en temps réel

### Configuration

Modifiez les paramètres dans `config/settings.py` :

```python
# Seuils de détection
EYE_CLOSED_TIME_MS = 1200  # Temps avant alerte somnolence
YAWN_COUNT_THRESHOLD = 2   # Nombre de bâillements
DISTRACTION_TIME_MS = 1500  # Temps avant alerte distraction

# Résolution caméra
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
```

## 📁 Structure du projet

```
SafeWay/
├── README.md                 # Ce fichier (bilingue)
├── README_FR.md             # Version française détaillée
├── README_EN.md             # Version anglaise détaillée
├── LICENSE                  # Licence MIT
├── CONTRIBUTING.md          # Guide de contribution
├── CHANGELOG.md             # Historique des versions
│
└── safeway/                 # Code source principal
    ├── README.md            # Documentation technique
    ├── GUIDE_ENTRAINEMENT.md # Guide d'entraînement
    ├── requirements.txt     # Dépendances Python
    │
    ├── config/              # Configuration
    │   └── settings.py     # Paramètres globaux
    │
    ├── ai/                  # Modules IA
    │   ├── video_stream.py      # Gestion flux vidéo
    │   ├── face_detector.py     # Détection visage (MediaPipe)
    │   ├── hand_detector.py     # Détection mains (MediaPipe)
    │   ├── yolo_detector.py     # Détection objets (YOLOv11)
    │   ├── state_analyzer.py    # Analyse état conducteur
    │   └── alert_manager.py     # Gestion alertes
    │
    ├── core/                # Utilitaires
    │   ├── logger.py        # Système de logging
    │   └── utils.py         # Fonctions utilitaires
    │
    ├── ui/                  # Interface utilisateur
    │   └── cli_demo.py      # Démonstration CLI
    │
    ├── data/                # Données et modèles
    │   ├── models/          # Modèles IA (YOLOv11)
    │   ├── logs/            # Fichiers de logs
    │   ├── samples/         # Vidéos d'exemple
    │   └── dataset/         # Dataset pour entraînement
    │
    ├── train_yolo.py        # Script d'entraînement
    ├── annotate_images.py   # Outil d'annotation
    └── download_yolo11.py   # Téléchargement modèles
```

## 🎓 Entraînement personnalisé

SafeWay permet d'entraîner YOLOv11 avec vos propres données pour améliorer la détection.

### Guide complet

Consultez [GUIDE_ENTRAINEMENT.md](safeway/GUIDE_ENTRAINEMENT.md) pour :
- Préparation du dataset
- Annotation des images
- Lancement de l'entraînement
- Optimisations avancées

### Démarrage rapide

```bash
# Créer le template
python3 train_yolo.py --create-template

# Annoter vos images
python3 annotate_images.py

# Lancer l'entraînement
python3 train_yolo.py --epochs 100 --batch 16
```

## 📊 Performances

### Métriques

- **FPS** : 15+ frames par seconde
- **Latence** : <100ms par frame
- **Précision fatigue** : >90%
- **Précision téléphone** : >85% (YOLOv11)
- **Utilisation CPU** : 30-50% (processeur moderne)

### Optimisations

- YOLO exécuté toutes les 3 frames (optimisation fluidité)
- Cache des résultats de détection
- Modèle YOLOv11 optimisé avec `fuse()` et `compile()`
- Vectorisation numpy pour calculs rapides

## 🔧 Développement

### Ajouter de nouvelles détections

1. Créez un nouveau module dans `ai/`
2. Intégrez-le dans `state_analyzer.py`
3. Ajoutez les alertes dans `alert_manager.py`

### Tests

```bash
# Test des imports
python3 test_imports.py

# Test complet
python3 ui/cli_demo.py
```

## 🐛 Dépannage

### La caméra ne s'ouvre pas

- Vérifiez les permissions de la caméra
- Changez `CAMERA_INDEX` dans `config/settings.py`
- Vérifiez qu'aucune autre app n'utilise la caméra

### Erreurs MediaPipe

- Réinstallez : `pip install --upgrade mediapipe`
- Vérifiez Python 3.8+

### Erreurs YOLO

- Vérifiez la connexion internet (téléchargement automatique)
- Réinstallez : `pip install --upgrade ultralytics`

## 📈 Roadmap

- [ ] Interface graphique (GUI) avec PyQt/Tkinter
- [ ] Support multi-caméras
- [ ] Export des statistiques (CSV, JSON)
- [ ] Mode nuit optimisé
- [ ] Détection de ceinture de sécurité
- [ ] Intégration avec systèmes de navigation
- [ ] Application mobile (Flutter/React Native)

## 🤝 Contribution

Les contributions sont les bienvenues ! Voir [CONTRIBUTING.md](CONTRIBUTING.md) pour les guidelines.

## 📄 Licence

Ce projet est sous licence MIT. Voir [LICENSE](LICENSE) pour plus de détails.

## 👨‍💻 Auteur

**Réalisé par [dylanecodeur](https://github.com/dylanecodeur)**

- GitHub : [@dylanecodeur](https://github.com/dylanecodeur)
- Projet : SafeWay - Système d'assistance à la conduite

## 🙏 Remerciements

- **Ultralytics** pour YOLOv11
- **Google MediaPipe** pour les outils de détection
- **OpenCV** pour le traitement vidéo
- La communauté open-source

## ⭐ Support

Si ce projet vous a aidé, n'hésitez pas à :
- ⭐ Mettre une étoile sur GitHub
- 🐛 Signaler des bugs
- 💡 Proposer des améliorations
- 📢 Partager le projet

---

**SafeWay** - Conduisez en toute sécurité ! 🛡️

*Réalisé avec ❤️ par dylanecodeur*

