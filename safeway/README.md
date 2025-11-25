# SafeWay 🚗

> **Réalisé par [dylanecodeur](https://github.com/dylanecodeur)**

Système d'assistance à la conduite basé sur l'IA pour détecter la fatigue, la distraction et les comportements dangereux du conducteur.

## 📋 Description

SafeWay est un système d'IA qui surveille en temps réel l'état du conducteur à l'aide de la caméra (PC, tablette, téléphone) et détecte les signes de fatigue, distraction et comportements dangereux, afin de prévenir les accidents.

### Caractéristiques principales

- ✅ Détection en temps réel via caméra
- ✅ Détection du visage et analyse du regard
- ✅ Détection de l'état des yeux (ouvert/fermé)
- ✅ Détection de la bouche (bâillements)
- ✅ Détection des mains
- ✅ Détection du téléphone avec YOLO
- ✅ Système d'alertes visuelles, sonores et vocales
- ✅ Traitement local (pas d'envoi au cloud)

## 🚀 Installation

### Prérequis

- Python 3.8 ou supérieur
- Caméra (webcam, caméra frontale)

### Étapes d'installation

1. **Cloner ou télécharger le projet**

```bash
cd SafeWay
```

2. **Installer les dépendances**

```bash
cd safeway
pip install -r requirements.txt
```

3. **Télécharger les modèles**

Les modèles MediaPipe sont téléchargés automatiquement au premier lancement.

Pour le modèle YOLO, il sera téléchargé automatiquement au premier lancement, ou vous pouvez le télécharger manuellement :

```bash
cd data/models
# Le modèle sera téléchargé automatiquement au premier lancement
# Ou utilisez ultralytics pour le télécharger :
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
```

## 🎮 Utilisation

### Lancer la démonstration

```bash
cd safeway
python ui/cli_demo.py
```

### Contrôles

- **'q'** : Quitter l'application
- La caméra s'ouvre automatiquement et commence l'analyse

### Fonctionnalités de détection

SafeWay détecte automatiquement :

- **Somnolence** : Yeux fermés plus de 1.5 secondes
- **Fatigue** : 3 bâillements en 60 secondes
- **Distraction** : Regard détourné plus de 2 secondes
- **Téléphone** : Détection d'un téléphone dans les mains
- **Absence** : Conducteur absent du champ de vision plus de 3 secondes

## 📁 Structure du projet

```
safeway/
├── README.md                 # Ce fichier
├── requirements.txt          # Dépendances Python
├── config/
│   ├── __init__.py
│   └── settings.py          # Configuration globale
├── ai/
│   ├── __init__.py
│   ├── video_stream.py      # Gestion du flux vidéo
│   ├── face_detector.py     # Détection du visage (MediaPipe)
│   ├── hand_detector.py     # Détection des mains (MediaPipe)
│   ├── yolo_detector.py     # Détection d'objets (YOLO)
│   ├── state_analyzer.py    # Analyse de l'état du conducteur
│   └── alert_manager.py     # Gestion des alertes
├── core/
│   ├── __init__.py
│   ├── logger.py            # Système de logging
│   └── utils.py             # Utilitaires
├── ui/
│   ├── __init__.py
│   └── cli_demo.py          # Démonstration CLI
└── data/
    ├── models/              # Modèles IA (YOLO, etc.)
    ├── logs/                # Fichiers de logs
    └── samples/             # Vidéos d'exemple
```

## ⚙️ Configuration

Les paramètres peuvent être modifiés dans `config/settings.py` :

- **Seuils de détection** : Temps avant déclenchement des alertes
- **Résolution caméra** : Largeur et hauteur des frames
- **Chemins des modèles** : Emplacement des modèles IA
- **Alertes** : Activation/désactivation des alertes sonores/visuelles

### Exemple de configuration

```python
# Seuils de détection
EYE_CLOSED_TIME_MS = 1500  # Temps en ms avant alerte somnolence
YAWN_COUNT_THRESHOLD = 3   # Nombre de bâillements en 60s
DISTRACTION_TIME_MS = 2000  # Temps en ms avant alerte distraction
```

## 🔧 Développement

### Ajouter un modèle YOLO personnalisé

1. Placez votre modèle dans `data/models/`
2. Modifiez `YOLO_MODEL_PATH` dans `config/settings.py`
3. Le modèle sera chargé automatiquement

### Ajouter de nouvelles détections

1. Créez un nouveau module dans `ai/`
2. Intégrez-le dans `state_analyzer.py`
3. Ajoutez les alertes correspondantes dans `alert_manager.py`

## 📝 Logs

Les logs sont enregistrés dans :
- **Fichier** : `data/logs/safeway.log`
- **Console** : Affichage en temps réel

## 🐛 Dépannage

### La caméra ne s'ouvre pas

- Vérifiez que la caméra n'est pas utilisée par une autre application
- Modifiez `CAMERA_INDEX` dans `config/settings.py` (essayez 0, 1, 2...)

### Le modèle YOLO ne se charge pas

- Vérifiez votre connexion internet (téléchargement automatique)
- Vérifiez que le fichier `data/models/yolov8n.pt` existe
- Réinstallez ultralytics : `pip install --upgrade ultralytics`

### Erreurs MediaPipe

- Réinstallez mediapipe : `pip install --upgrade mediapipe`
- Vérifiez que votre version de Python est compatible (3.8+)

## 📄 Licence

Ce projet est fourni à des fins éducatives et de démonstration.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.

## 📧 Contact

Pour toute question ou suggestion, veuillez ouvrir une issue sur le dépôt du projet.

---

**SafeWay** - Conduisez en toute sécurité ! 🛡️

