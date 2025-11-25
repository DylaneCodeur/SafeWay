#!/usr/bin/env python3
"""
Script pour télécharger le modèle YOLOv8s (plus performant)
"""
import sys
from pathlib import Path
from ultralytics import YOLO
import shutil

def main():
    print("Téléchargement du modèle YOLOv8s (plus performant)...")
    
    model_path = Path("data/models/yolov8s.pt")
    model_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        # Télécharger yolov8s
        print("Téléchargement de yolov8s.pt...")
        model = YOLO("yolov8s.pt")
        
        # Sauvegarder
        if Path("yolov8s.pt").exists():
            shutil.copy("yolov8s.pt", model_path)
            print(f"✅ Modèle sauvegardé à {model_path}")
        else:
            print("⚠️  Fichier yolov8s.pt non trouvé après téléchargement")
            print("Tentative avec yolov8n.pt...")
            model = YOLO("yolov8n.pt")
            if Path("yolov8n.pt").exists():
                shutil.copy("yolov8n.pt", model_path)
                print(f"✅ Modèle yolov8n sauvegardé à {model_path}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

