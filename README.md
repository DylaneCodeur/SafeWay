# 🚗 SafeWay - Système d'assistance à la conduite basé sur l'IA

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Version](https://img.shields.io/badge/version-1.0.0-orange.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

[🇫🇷 Français](#français) | [🇬🇧 English](#english)

> **Réalisé par [dylanecodeur](https://github.com/dylanecodeur)**

---

## 🇫🇷 Français

### 📋 Description

**SafeWay** est un système d'intelligence artificielle avancé qui surveille en temps réel l'état du conducteur à l'aide de la caméra de l'appareil (PC, tablette, téléphone). Le système détecte automatiquement les signes de fatigue, de distraction et les comportements dangereux pour prévenir les accidents de la route.

### ✨ Fonctionnalités principales

- ✅ **Détection de somnolence** : Détecte les yeux fermés prolongés (>1.2s)
- ✅ **Détection de fatigue** : Analyse les bâillements répétés et le taux de clignement anormal
- ✅ **Détection de distraction** : Identifie les regards détournés et mouvements excessifs de tête
- ✅ **Détection de téléphone** : Utilise YOLOv11 pour détecter l'utilisation du téléphone au volant
- ✅ **Alertes multi-modales** : Alertes visuelles, sonores et vocales en français
- ✅ **Traitement local** : Aucune donnée vidéo n'est envoyée au cloud (100% privé)
- ✅ **Temps réel** : Analyse fluide à 15+ FPS
- ✅ **Modèle personnalisable** : Possibilité d'entraîner YOLOv11 avec vos propres données

### 🛠️ Technologies utilisées

- **Python 3.8+**
- **MediaPipe** : Détection du visage, des yeux, de la bouche et des mains
- **YOLOv11** : Détection d'objets (téléphones) ultra-performante
- **OpenCV** : Traitement vidéo en temps réel
- **PyGame** : Alertes sonores
- **TTS (Text-to-Speech)** : Synthèse vocale en français

### 🚀 Installation rapide

```bash
# Cloner le repository
git clone https://github.com/dylanecodeur/SafeWay.git
cd SafeWay/safeway

# Installer les dépendances
pip install -r requirements.txt

# Télécharger les modèles (automatique au premier lancement)
python3 download_yolo11.py

# Lancer SafeWay
python3 ui/cli_demo.py
```

### 📖 Documentation

- [Guide d'installation complet](safeway/README.md)
- [Guide d'entraînement personnalisé](safeway/GUIDE_ENTRAINEMENT.md)
- [Documentation technique](safeway/README.md#architecture)

### 🎯 Cas d'usage

- **Conducteurs professionnels** : Taxis, bus, camions
- **Conducteurs particuliers** : Surveillance personnelle
- **Fleets** : Gestion de flottes de véhicules
- **Recherche** : Études sur la fatigue au volant

### 📊 Statistiques

- ⚡ **Performance** : 15+ FPS en temps réel
- 🎯 **Précision** : Détection >90% pour la fatigue
- 🔒 **Sécurité** : 100% traitement local
- 💰 **Coût** : Gratuit et open-source

### 👨‍💻 Auteur

**Réalisé par [dylanecodeur](https://github.com/dylanecodeur)**

### 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 🇬🇧 English

### 📋 Description

**SafeWay** is an advanced artificial intelligence system that monitors in real-time the driver's state using the device's camera (PC, tablet, phone). The system automatically detects signs of fatigue, distraction, and dangerous behaviors to prevent road accidents.

### ✨ Key Features

- ✅ **Drowsiness Detection** : Detects prolonged eye closure (>1.2s)
- ✅ **Fatigue Detection** : Analyzes repeated yawns and abnormal blink rate
- ✅ **Distraction Detection** : Identifies diverted gazes and excessive head movements
- ✅ **Phone Detection** : Uses YOLOv11 to detect phone use while driving
- ✅ **Multi-modal Alerts** : Visual, audio, and voice alerts in French
- ✅ **Local Processing** : No video data sent to cloud (100% private)
- ✅ **Real-time** : Smooth analysis at 15+ FPS
- ✅ **Customizable Model** : Ability to train YOLOv11 with your own data

### 🛠️ Technologies Used

- **Python 3.8+**
- **MediaPipe** : Face, eyes, mouth, and hands detection
- **YOLOv11** : Ultra-performing object detection (phones)
- **OpenCV** : Real-time video processing
- **PyGame** : Audio alerts
- **TTS (Text-to-Speech)** : French voice synthesis

### 🚀 Quick Installation

```bash
# Clone the repository
git clone https://github.com/dylanecodeur/SafeWay.git
cd SafeWay/safeway

# Install dependencies
pip install -r requirements.txt

# Download models (automatic on first launch)
python3 download_yolo11.py

# Launch SafeWay
python3 ui/cli_demo.py
```

### 📖 Documentation

- [Complete installation guide](safeway/README.md)
- [Custom training guide](safeway/GUIDE_ENTRAINEMENT.md)
- [Technical documentation](safeway/README.md#architecture)

### 🎯 Use Cases

- **Professional drivers** : Taxis, buses, trucks
- **Private drivers** : Personal monitoring
- **Fleets** : Vehicle fleet management
- **Research** : Studies on driver fatigue

### 📊 Statistics

- ⚡ **Performance** : 15+ FPS real-time
- 🎯 **Accuracy** : >90% detection for fatigue
- 🔒 **Security** : 100% local processing
- 💰 **Cost** : Free and open-source

### 👨‍💻 Author

**Created by [dylanecodeur](https://github.com/dylanecodeur)**

### 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🌟 Contribuer

Les contributions sont les bienvenues ! Veuillez lire [CONTRIBUTING.md](CONTRIBUTING.md) pour plus de détails.

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## ⭐ Support

Si ce projet vous a aidé, n'hésitez pas à lui donner une ⭐ sur GitHub !

If this project helped you, feel free to give it a ⭐ on GitHub!

---

**SafeWay** - Drive safely! 🛡️
