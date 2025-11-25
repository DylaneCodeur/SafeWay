# Guide de préparation du dataset pour l'entraînement SafeWay

## 📁 Structure du dataset

Votre dataset doit être organisé comme suit:

```
data/dataset/
├── dataset.yaml          # Fichier de configuration
├── images/
│   ├── train/           # Images d'entraînement
│   │   ├── img001.jpg
│   │   ├── img002.jpg
│   │   └── ...
│   ├── val/             # Images de validation
│   │   ├── img101.jpg
│   │   └── ...
│   └── test/            # Images de test (optionnel)
│       └── ...
└── labels/
    ├── train/           # Annotations d'entraînement (format YOLO)
    │   ├── img001.txt
    │   ├── img002.txt
    │   └── ...
    └── val/             # Annotations de validation
        ├── img101.txt
        └── ...
```

## 🏷️ Format des annotations YOLO

Chaque fichier `.txt` doit contenir une ligne par objet détecté:

```
class_id center_x center_y width height
```

**Exemple:**
```
0 0.5 0.5 0.3 0.4
```

Où:
- `class_id`: ID de la classe (0=téléphone, 1=main_telephone, etc.)
- `center_x`, `center_y`: Coordonnées du centre (normalisées 0-1)
- `width`, `height`: Largeur et hauteur (normalisées 0-1)

## 📝 Format du fichier dataset.yaml

```yaml
path: data/dataset
train: images/train
val: images/val

names:
  0: telephone
  1: main_telephone
  2: distraction

nc: 3
```

## 🛠️ Outils pour annoter vos images

### Option 1: LabelImg (Recommandé)
```bash
pip install labelImg
labelImg
```

### Option 2: Roboflow
- Site web: https://roboflow.com
- Interface web gratuite
- Export au format YOLO

### Option 3: CVAT
- Outil professionnel open-source
- Site: https://cvat.org

## 📊 Recommandations

- **Minimum 100 images par classe** pour un bon entraînement
- **Ratio train/val**: 80% train, 20% validation
- **Diversité**: Images dans différentes conditions (lumière, angle, etc.)
- **Qualité**: Images claires et bien annotées

## 🚀 Lancer l'entraînement

```bash
# Créer le template
python3 train_yolo.py --create-template

# Configurer dataset.yaml avec vos chemins

# Lancer l'entraînement
python3 train_yolo.py --epochs 100 --batch 16
```

## 💡 Astuces

1. **Augmentation de données**: Le script applique automatiquement des augmentations
2. **Transfer Learning**: Le modèle part de YOLOv11 pré-entraîné
3. **Validation**: Surveillez les métriques de validation pour éviter le surapprentissage
4. **GPU**: Utilisez `device='cuda'` dans le script si vous avez un GPU

