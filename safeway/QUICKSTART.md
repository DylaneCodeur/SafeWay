# 🚀 Guide de démarrage rapide SafeWay

## Installation (déjà fait ✅)

Les dépendances ont été installées et le modèle YOLO téléchargé.

## Lancer SafeWay

```bash
cd safeway
python3 ui/cli_demo.py
```

## Contrôles

- **'q'** : Quitter l'application
- La caméra s'ouvre automatiquement

## Ce que SafeWay détecte

- ✅ **Somnolence** : Yeux fermés > 1.5 secondes
- ✅ **Fatigue** : 3 bâillements en 60 secondes  
- ✅ **Distraction** : Regard détourné > 2 secondes
- ✅ **Téléphone** : Détection d'un téléphone dans les mains
- ✅ **Absence** : Conducteur absent > 3 secondes

## Test des imports

Pour vérifier que tout fonctionne :

```bash
python3 test_imports.py
```

## Configuration

Modifiez les paramètres dans `config/settings.py` :
- Seuils de détection
- Résolution caméra
- Alertes

## Dépannage

### Caméra ne s'ouvre pas
- Vérifiez qu'elle n'est pas utilisée ailleurs
- Changez `CAMERA_INDEX` dans `config/settings.py`

### Erreurs
- Consultez les logs dans `data/logs/safeway.log`

---

**Bon test ! 🚗**

