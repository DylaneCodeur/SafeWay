#!/usr/bin/env python3
"""
Script d'entraînement pour YOLOv11 sur données personnalisées SafeWay
"""
import sys
from pathlib import Path
from ultralytics import YOLO
from config.settings import MODELS_DIR
from core.logger import setup_logger

logger = setup_logger("TrainYOLO")

def train_model(
    data_yaml: str = "data/dataset/dataset.yaml",
    epochs: int = 100,
    imgsz: int = 640,
    batch: int = 16,
    model_size: str = "n"  # n, s, m, l, x
):
    """
    Entraîne un modèle YOLOv11 personnalisé
    
    Args:
        data_yaml: Chemin vers le fichier YAML de configuration du dataset
        epochs: Nombre d'époques d'entraînement
        imgsz: Taille des images (640 recommandé)
        batch: Taille du batch
        model_size: Taille du modèle (n=nano, s=small, m=medium, l=large, x=xlarge)
    """
    logger.info("=" * 60)
    logger.info("ENTRAÎNEMENT YOLOv11 POUR SAFEWAY")
    logger.info("=" * 60)
    
    # Vérifier que le fichier dataset existe
    data_path = Path(data_yaml)
    if not data_path.exists():
        logger.error(f"Fichier dataset non trouvé: {data_yaml}")
        logger.info("\nPour créer le dataset:")
        logger.info("1. Créez un dossier data/dataset/")
        logger.info("2. Organisez vos images: data/dataset/images/train/ et data/dataset/images/val/")
        logger.info("3. Organisez vos annotations: data/dataset/labels/train/ et data/dataset/labels/val/")
        logger.info("4. Créez data/dataset/dataset.yaml (voir exemple ci-dessous)")
        return False
    
    # Charger le modèle de base YOLOv11
    model_name = f"yolo11{model_size}.pt"
    logger.info(f"Chargement du modèle de base: {model_name}")
    
    try:
        model = YOLO(model_name)
    except Exception as e:
        logger.error(f"Impossible de charger {model_name}: {e}")
        logger.info("Tentative avec yolo11n.pt...")
        model = YOLO("yolo11n.pt")
    
    # Paramètres d'entraînement optimisés
    logger.info(f"\nParamètres d'entraînement:")
    logger.info(f"  - Époques: {epochs}")
    logger.info(f"  - Taille images: {imgsz}")
    logger.info(f"  - Batch size: {batch}")
    logger.info(f"  - Dataset: {data_yaml}")
    
    try:
        # Lancer l'entraînement
        results = model.train(
            data=data_yaml,
            epochs=epochs,
            imgsz=imgsz,
            batch=batch,
            name="safeway_custom",  # Nom du run
            project="runs/detect",  # Dossier des résultats
            patience=50,  # Arrêt anticipé si pas d'amélioration
            save=True,
            save_period=10,  # Sauvegarder tous les 10 epochs
            val=True,  # Validation
            plots=True,  # Générer les graphiques
            verbose=True,
            # Optimisations pour performance
            device='cpu',  # ou 'cuda' si GPU disponible
            workers=4,  # Nombre de workers pour le chargement des données
            # Augmentation de données
            hsv_h=0.015,  # Augmentation teinte HSV
            hsv_s=0.7,
            hsv_v=0.4,
            degrees=10,  # Rotation
            translate=0.1,  # Translation
            scale=0.5,  # Mise à l'échelle
            flipud=0.0,  # Flip vertical
            fliplr=0.5,  # Flip horizontal
            mosaic=1.0,  # Mosaic augmentation
            mixup=0.1,  # Mixup augmentation
        )
        
        logger.info("\n" + "=" * 60)
        logger.info("ENTRAÎNEMENT TERMINÉ AVEC SUCCÈS!")
        logger.info("=" * 60)
        logger.info(f"Meilleur modèle sauvegardé dans: runs/detect/safeway_custom/weights/best.pt")
        logger.info(f"Modèle final sauvegardé dans: runs/detect/safeway_custom/weights/last.pt")
        
        # Copier le meilleur modèle vers data/models/
        best_model = Path("runs/detect/safeway_custom/weights/best.pt")
        if best_model.exists():
            import shutil
            custom_model_path = MODELS_DIR / "yolo11_custom.pt"
            shutil.copy(best_model, custom_model_path)
            logger.info(f"Modèle personnalisé copié vers: {custom_model_path}")
        
        return True
        
    except Exception as e:
        logger.error(f"Erreur lors de l'entraînement: {e}", exc_info=True)
        return False

def create_dataset_template():
    """Crée un template pour le fichier dataset.yaml"""
    template = """# Configuration du dataset SafeWay
# Chemin vers les images et labels

path: data/dataset  # Chemin racine du dataset
train: images/train  # Dossier des images d'entraînement (relatif à path)
val: images/val      # Dossier des images de validation (relatif à path)
test: images/test     # Dossier des images de test (optionnel, relatif à path)

# Classes à détecter
names:
  0: telephone        # Téléphone portable
  1: main_telephone   # Main tenant un téléphone
  2: distraction      # Objet de distraction
  3: conducteur       # Visage du conducteur (optionnel)

# Nombre de classes
nc: 3
"""
    
    dataset_dir = Path("data/dataset")
    dataset_dir.mkdir(parents=True, exist_ok=True)
    
    yaml_path = dataset_dir / "dataset.yaml"
    if not yaml_path.exists():
        yaml_path.write_text(template)
        logger.info(f"Template créé: {yaml_path}")
    else:
        logger.info(f"Fichier existe déjà: {yaml_path}")
    
    return yaml_path

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Entraîner YOLOv11 pour SafeWay")
    parser.add_argument("--data", type=str, default="data/dataset/dataset.yaml",
                       help="Chemin vers le fichier dataset.yaml")
    parser.add_argument("--epochs", type=int, default=100,
                       help="Nombre d'époques")
    parser.add_argument("--imgsz", type=int, default=640,
                       help="Taille des images")
    parser.add_argument("--batch", type=int, default=16,
                       help="Taille du batch")
    parser.add_argument("--model", type=str, default="n",
                       choices=["n", "s", "m", "l", "x"],
                       help="Taille du modèle (n=nano, s=small, m=medium, l=large, x=xlarge)")
    parser.add_argument("--create-template", action="store_true",
                       help="Créer un template pour dataset.yaml")
    
    args = parser.parse_args()
    
    if args.create_template:
        create_dataset_template()
        logger.info("\nTemplate créé! Configurez votre dataset et relancez l'entraînement.")
    else:
        success = train_model(
            data_yaml=args.data,
            epochs=args.epochs,
            imgsz=args.imgsz,
            batch=args.batch,
            model_size=args.model
        )
        sys.exit(0 if success else 1)

