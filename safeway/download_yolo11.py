#!/usr/bin/env python3
"""
Script pour télécharger YOLOv11 (ultra performant)
"""
import sys
from pathlib import Path
from ultralytics import YOLO
import shutil

def main():
    print("Téléchargement du modèle YOLOv11 (ultra performant)...")
    
    model_path = Path("data/models/yolo11n.pt")
    model_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        # Télécharger YOLOv11
        print("Téléchargement de yolo11n.pt...")
        model = YOLO("yolo11n.pt")
        
        # Sauvegarder
        if Path("yolo11n.pt").exists():
            shutil.copy("yolo11n.pt", model_path)
            print(f"✅ Modèle YOLOv11 sauvegardé à {model_path}")
        else:
            print("⚠️  Tentative avec yolo11s.pt...")
            model = YOLO("yolo11s.pt")
            if Path("yolo11s.pt").exists():
                shutil.copy("yolo11s.pt", model_path)
                print(f"✅ Modèle YOLOv11s sauvegardé à {model_path}")
            else:
                print("⚠️  YOLOv11 non disponible, utilisation de YOLOv8s...")
                model = YOLO("yolov8s.pt")
                if Path("yolov8s.pt").exists():
                    shutil.copy("yolov8s.pt", model_path)
                    print(f"✅ Modèle YOLOv8s sauvegardé à {model_path}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

