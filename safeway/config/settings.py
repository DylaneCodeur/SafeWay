"""
Configuration globale pour SafeWay
"""
import os
from pathlib import Path

# Chemins de base
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = DATA_DIR / "models"
LOGS_DIR = DATA_DIR / "logs"
SAMPLES_DIR = DATA_DIR / "samples"

# Créer les dossiers s'ils n'existent pas
MODELS_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)
SAMPLES_DIR.mkdir(parents=True, exist_ok=True)

# Configuration de la caméra
CAMERA_INDEX = 0  # Index de la caméra (0 = caméra par défaut)
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
FPS_TARGET = 15  # FPS minimum visé

# Seuils de détection (optimisés pour meilleure cohérence)
EYE_CLOSED_THRESHOLD = 0.22  # Ratio pour considérer l'œil fermé (ajusté)
EYE_CLOSED_TIME_MS = 1200  # Temps en ms avant alerte somnolence (plus rapide)
YAWN_THRESHOLD = 0.45  # Ratio pour considérer la bouche ouverte (ajusté)
YAWN_COUNT_THRESHOLD = 2  # Nombre de bâillements en 60s (plus sensible)
YAWN_TIME_WINDOW = 60  # Fenêtre de temps en secondes
DISTRACTION_TIME_MS = 1500  # Temps en ms avant alerte distraction (plus rapide)
ABSENCE_TIME_MS = 2500  # Temps en ms avant alerte absence (plus rapide)

# Nouveaux signaux de détection
BLINK_RATE_THRESHOLD = 0.15  # Taux de clignement anormal (yeux/sec)
HEAD_MOVEMENT_THRESHOLD = 30  # Seuil de mouvement de tête (degrés)
GAZE_DEVIATION_THRESHOLD = 25  # Seuil de déviation du regard (degrés)

# Modèles - Utiliser YOLOv11 pour meilleure performance
YOLO_MODEL_PATH = MODELS_DIR / "yolo11n.pt"
YOLO_MODEL_NAME = "yolo11n.pt"  # YOLOv11 est plus récent et performant
USE_YOLO11 = True  # Utiliser YOLOv11 au lieu de YOLOv8

# Classes YOLO à détecter (téléphone)
PHONE_CLASS_ID = 67  # ID de la classe "cell phone" dans COCO

# Alertes
ALERT_SOUND_ENABLED = True
ALERT_VOICE_ENABLED = True
ALERT_VISUAL_ENABLED = True

# Logging
LOG_FILE = LOGS_DIR / "safeway.log"
LOG_LEVEL = "INFO"

