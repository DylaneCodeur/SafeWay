#!/usr/bin/env python3
"""
Script de test pour vérifier que tous les imports fonctionnent
"""
import sys
from pathlib import Path

# Ajouter le répertoire au path
sys.path.insert(0, str(Path(__file__).parent))

print("Test des imports SafeWay...")
print("=" * 60)

try:
    print("1. Test import config...")
    from config import settings
    print("   ✓ config.settings importé")
    
    print("2. Test import core...")
    from core import logger, utils
    print("   ✓ core.logger et core.utils importés")
    
    print("3. Test import ai modules...")
    from ai import video_stream, face_detector, hand_detector, yolo_detector, state_analyzer, alert_manager
    print("   ✓ Tous les modules AI importés")
    
    print("4. Test initialisation des composants...")
    logger_instance = logger.setup_logger("Test")
    print("   ✓ Logger initialisé")
    
    video = video_stream.VideoStream()
    print("   ✓ VideoStream créé")
    
    face = face_detector.FaceDetector()
    print("   ✓ FaceDetector créé")
    
    hand = hand_detector.HandDetector()
    print("   ✓ HandDetector créé")
    
    yolo = yolo_detector.YOLODetector()
    print("   ✓ YOLODetector créé")
    
    state = state_analyzer.StateAnalyzer()
    print("   ✓ StateAnalyzer créé")
    
    alert = alert_manager.AlertManager()
    print("   ✓ AlertManager créé")
    
    print("5. Test chargement modèle YOLO...")
    if yolo.load_model():
        print("   ✓ Modèle YOLO chargé")
    else:
        print("   ⚠ Modèle YOLO non chargé (peut être normal si pas de connexion)")
    
    print("\n" + "=" * 60)
    print("✅ TOUS LES TESTS SONT PASSÉS!")
    print("=" * 60)
    print("\nVous pouvez maintenant lancer la démo avec:")
    print("  python3 ui/cli_demo.py")
    
except ImportError as e:
    print(f"\n❌ ERREUR D'IMPORT: {e}")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ ERREUR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

