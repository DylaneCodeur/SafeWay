# 🎓 Guide complet d'entraînement SafeWay

## 📋 Vue d'ensemble

Ce guide vous explique comment entraîner YOLOv11 avec vos propres données pour améliorer la détection dans SafeWay.

## 🚀 Démarrage rapide

### 1. Préparer le dataset

```bash
# Créer la structure
mkdir -p data/dataset/images/{train,val}
mkdir -p data/dataset/labels/{train,val}

# Créer le template de configuration
python3 train_yolo.py --create-template
```

### 2. Annoter vos images

```bash
# Installer et lancer LabelImg
python3 annotate_images.py
```

Ou manuellement:
```bash
pip install labelImg
labelImg
```

### 3. Lancer l'entraînement

```bash
# Entraînement de base (100 epochs)
python3 train_yolo.py --epochs 100 --batch 16

# Entraînement avec modèle plus grand (meilleure précision)
python3 train_yolo.py --epochs 150 --batch 8 --model s

# Entraînement rapide (test)
python3 train_yolo.py --epochs 20 --batch 32
```

## 📊 Structure des données

### Format YOLO

Chaque image doit avoir un fichier `.txt` correspondant avec les annotations:

**Exemple: `img001.txt`**
```
0 0.5 0.5 0.3 0.4
1 0.2 0.3 0.1 0.15
```

Format: `class_id center_x center_y width height` (toutes les valeurs entre 0 et 1)

### Classes recommandées

- **0: telephone** - Téléphone portable seul
- **1: main_telephone** - Main tenant un téléphone
- **2: distraction** - Autres objets de distraction
- **3: conducteur** - Visage du conducteur (optionnel)

## 🎯 Bonnes pratiques

### Collecte de données

1. **Diversité**: 
   - Différentes conditions d'éclairage
   - Différents angles de vue
   - Différents types de téléphones
   - Différentes positions des mains

2. **Quantité minimale**:
   - 100+ images par classe pour un bon résultat
   - 500+ images pour un excellent résultat

3. **Qualité**:
   - Images nettes et bien éclairées
   - Annotations précises
   - Pas de doublons

### Paramètres d'entraînement

| Paramètre | Valeur recommandée | Description |
|-----------|-------------------|-------------|
| epochs | 100-200 | Nombre d'itérations |
| batch | 8-32 | Taille du batch (selon RAM/GPU) |
| imgsz | 640 | Taille des images |
| model | n ou s | Taille du modèle (n=rapide, s=précis) |

## 📈 Suivi de l'entraînement

Les résultats sont sauvegardés dans `runs/detect/safeway_custom/`:

- `weights/best.pt` - Meilleur modèle (meilleure précision)
- `weights/last.pt` - Dernier modèle
- `results.png` - Graphiques de performance
- `confusion_matrix.png` - Matrice de confusion

### Métriques importantes

- **mAP50**: Précision moyenne (objectif: >0.7)
- **mAP50-95**: Précision moyenne multi-seuils (objectif: >0.5)
- **Precision**: Précision des détections
- **Recall**: Taux de détection

## 🔧 Utiliser le modèle entraîné

Après l'entraînement, le modèle est automatiquement copié vers `data/models/yolo11_custom.pt`.

Pour l'utiliser dans SafeWay, modifiez `config/settings.py`:

```python
YOLO_MODEL_PATH = MODELS_DIR / "yolo11_custom.pt"
```

## 💡 Optimisations avancées

### Utiliser un GPU

Si vous avez un GPU NVIDIA:

```python
# Dans train_yolo.py, changer:
device='cuda'  # au lieu de 'cpu'
```

### Fine-tuning

Pour améliorer un modèle existant:

```python
# Charger votre modèle personnalisé
model = YOLO("data/models/yolo11_custom.pt")
model.train(data="data/dataset/dataset.yaml", epochs=50)
```

### Export pour production

```python
# Exporter en ONNX (plus rapide)
model.export(format='onnx')

# Exporter en TensorRT (GPU NVIDIA)
model.export(format='engine')
```

## 🐛 Dépannage

### Erreur: "No labels found"
- Vérifiez que les fichiers `.txt` existent dans `labels/train/`
- Vérifiez le format des annotations (5 valeurs par ligne)

### Erreur: "CUDA out of memory"
- Réduisez `batch` (ex: 8 ou 4)
- Utilisez un modèle plus petit (`--model n`)

### Précision faible
- Augmentez le nombre d'images
- Vérifiez la qualité des annotations
- Augmentez le nombre d'epochs
- Utilisez un modèle plus grand (`--model s` ou `m`)

## 📚 Ressources

- Documentation Ultralytics: https://docs.ultralytics.com
- Guide YOLO: https://docs.ultralytics.com/modes/train/
- LabelImg: https://github.com/HumanSignal/labelImg

---

**Bon entraînement ! 🚀**

