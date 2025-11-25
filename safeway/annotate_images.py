#!/usr/bin/env python3
"""
Script d'aide pour annoter les images avec LabelImg
"""
import subprocess
import sys
from pathlib import Path

def install_labelimg():
    """Installe LabelImg si nécessaire"""
    try:
        import labelImg
        print("✅ LabelImg est déjà installé")
        return True
    except ImportError:
        print("Installation de LabelImg...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "labelImg"])
            print("✅ LabelImg installé avec succès")
            return True
        except Exception as e:
            print(f"❌ Erreur lors de l'installation: {e}")
            return False

def launch_labelimg(dataset_path: str = "data/dataset"):
    """Lance LabelImg avec la configuration SafeWay"""
    dataset_dir = Path(dataset_path)
    images_dir = dataset_dir / "images" / "train"
    labels_dir = dataset_dir / "labels" / "train"
    
    # Créer les dossiers s'ils n'existent pas
    images_dir.mkdir(parents=True, exist_ok=True)
    labels_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📁 Dossier images: {images_dir}")
    print(f"📁 Dossier labels: {labels_dir}")
    
    # Fichier de classes
    classes_file = dataset_dir / "classes.txt"
    if not classes_file.exists():
        classes_content = """telephone
main_telephone
distraction
conducteur"""
        classes_file.write_text(classes_content)
        print(f"✅ Fichier classes.txt créé: {classes_file}")
    
    try:
        # Lancer LabelImg
        print("\n🚀 Lancement de LabelImg...")
        print("Instructions:")
        print("1. Ouvrez le dossier images/train/")
        print("2. Changez le format d'export vers YOLO")
        print("3. Sauvegardez les labels dans labels/train/")
        print("4. Utilisez le fichier classes.txt pour les noms de classes\n")
        
        subprocess.run(["labelImg", str(images_dir), str(classes_file), str(labels_dir)])
        
    except FileNotFoundError:
        print("❌ LabelImg non trouvé. Installation...")
        if install_labelimg():
            subprocess.run(["labelImg", str(images_dir), str(classes_file), str(labels_dir)])
        else:
            print("\n💡 Installation manuelle:")
            print("  pip install labelImg")
            print("  labelImg")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Lancer LabelImg pour annoter les images")
    parser.add_argument("--dataset", type=str, default="data/dataset",
                       help="Chemin vers le dossier dataset")
    
    args = parser.parse_args()
    launch_labelimg(args.dataset)

