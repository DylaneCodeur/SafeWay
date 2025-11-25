"""
Démonstration CLI de SafeWay
"""
import sys
import cv2
import time
from pathlib import Path

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from ai.video_stream import VideoStream
from ai.face_detector import FaceDetector
from ai.hand_detector import HandDetector
from ai.yolo_detector import YOLODetector
from ai.state_analyzer import StateAnalyzer
from ai.alert_manager import AlertManager
from core.logger import setup_logger

logger = setup_logger("CLIDemo")

def main():
    """Fonction principale de la démo"""
    print("=" * 60)
    print("SafeWay - Système de détection de fatigue et distraction")
    print("=" * 60)
    print("\nInstructions:")
    print("- Appuyez sur 'q' pour quitter")
    print("- La caméra va s'ouvrir et analyser votre état")
    print("- Les alertes apparaîtront automatiquement\n")
    
    # Initialiser les composants
    logger.info("Initialisation des composants...")
    
    video_stream = VideoStream()
    face_detector = FaceDetector()
    hand_detector = HandDetector()
    yolo_detector = YOLODetector()
    state_analyzer = StateAnalyzer()
    alert_manager = AlertManager()
    
    # Cache pour résultats YOLO (optimisation performance)
    last_yolo_results = {'phone_detected': False}
    
    # Charger le modèle YOLO
    logger.info("Chargement du modèle YOLO...")
    if not yolo_detector.load_model():
        logger.error("Impossible de charger le modèle YOLO")
        return
    
    # Ouvrir la caméra
    logger.info("Ouverture de la caméra...")
    if not video_stream.start():
        logger.error("Impossible d'ouvrir la caméra")
        logger.error("Vérifiez que:")
        logger.error("  1. La caméra n'est pas utilisée par une autre application")
        logger.error("  2. Les permissions de caméra sont accordées")
        logger.error("  3. La caméra est bien connectée")
        return
    
    try:
        frame_count = 0
        consecutive_failures = 0
        max_failures = 10
        
        logger.info("Démarrage de la boucle principale...")
        logger.info("La fenêtre vidéo va s'ouvrir. Appuyez sur 'q' pour quitter.")
        
        while True:
            # Lire une frame
            ret, frame = video_stream.read_frame()
            
            if not ret:
                consecutive_failures += 1
                if consecutive_failures >= max_failures:
                    logger.error(f"Impossible de lire {max_failures} frames consécutives. Arrêt.")
                    break
                logger.warning(f"Impossible de lire la frame ({consecutive_failures}/{max_failures})")
                time.sleep(0.1)  # Attendre un peu avant de réessayer
                continue
            
            # Réinitialiser le compteur d'échecs si on a réussi
            consecutive_failures = 0
            
            frame_count += 1
            
            try:
                # Détections optimisées (YOLO seulement toutes les 3 frames pour performance)
                face_results = face_detector.detect(frame)
                hand_results = hand_detector.detect(frame)
                
                # YOLO moins fréquent pour meilleure fluidité (optimisation)
                if frame_count % 3 == 0:  # Toutes les 3 frames
                    yolo_results = yolo_detector.detect(frame)
                    last_yolo_results = yolo_results
                else:
                    # Réutiliser les résultats précédents
                    yolo_results = last_yolo_results
                
                # Analyse de l'état
                analysis = state_analyzer.analyze(face_results, hand_results, yolo_results)
            except Exception as e:
                logger.error(f"Erreur lors des détections: {e}", exc_info=True)
                # Continuer avec des résultats vides
                face_results = {'face_detected': False}
                hand_results = {'hands_detected': False}
                yolo_results = {'phone_detected': False}
                analysis = {'state': {}, 'alerts': []}
            
            # Dessiner les annotations
            annotated_frame = frame.copy()
            
            # Dessiner les landmarks du visage
            if face_results['face_detected']:
                annotated_frame = face_detector.draw_landmarks(annotated_frame, face_results)
                
                # Afficher les informations
                info_y = 30
                cv2.putText(annotated_frame, f"Visage: Detecte", (10, info_y),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                info_y += 25
                
                eye_status = "Ouverts" if face_results['eyes_open'] else "Fermes"
                eye_color = (0, 255, 0) if face_results['eyes_open'] else (0, 0, 255)
                cv2.putText(annotated_frame, f"Yeux: {eye_status}", (10, info_y),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, eye_color, 2)
                info_y += 25
                
                mouth_status = "Ouverte" if face_results['mouth_open'] else "Fermee"
                cv2.putText(annotated_frame, f"Bouche: {mouth_status}", (10, info_y),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
                info_y += 25
                
                cv2.putText(annotated_frame, f"Tete: {face_results['head_position']}", (10, info_y),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            else:
                cv2.putText(annotated_frame, "Visage: Non detecte", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            
            # Dessiner les détections YOLO
            if yolo_results['phone_detected']:
                annotated_frame = yolo_detector.draw_detections(annotated_frame, yolo_results)
            
            # Gérer les alertes
            if analysis['alerts']:
                for alert in analysis['alerts']:
                    annotated_frame = alert_manager.trigger_alert(alert, annotated_frame)
            
            # Afficher l'état
            state = analysis['state']
            state_y = annotated_frame.shape[0] - 100
            
            if state['fatigue_detected']:
                cv2.putText(annotated_frame, "ETAT: FATIGUE DETECTEE", (10, state_y),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            elif state['distraction_detected']:
                cv2.putText(annotated_frame, "ETAT: DISTRACTION DETECTEE", (10, state_y),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)
            elif state['phone_detected']:
                cv2.putText(annotated_frame, "ETAT: TELEPHONE DETECTE", (10, state_y),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            elif state['driver_absent']:
                cv2.putText(annotated_frame, "ETAT: CONDUCTEUR ABSENT", (10, state_y),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            else:
                cv2.putText(annotated_frame, "ETAT: NORMAL", (10, state_y),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Afficher le FPS (simplifié)
            cv2.putText(annotated_frame, f"Frame: {frame_count}", (10, annotated_frame.shape[0] - 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Afficher la frame
            cv2.imshow('SafeWay - Detection en temps reel', annotated_frame)
            
            # Vérifier la touche 'q' pour quitter
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                logger.info("Arrêt demandé par l'utilisateur")
                break
    
    except KeyboardInterrupt:
        logger.info("Interruption clavier")
    except Exception as e:
        logger.error(f"Erreur lors de l'exécution: {e}", exc_info=True)
    finally:
        # Nettoyage
        logger.info("Nettoyage des ressources...")
        video_stream.release()
        face_detector.release()
        hand_detector.release()
        alert_manager.release()
        cv2.destroyAllWindows()
        print("\nSafeWay ferme. Au revoir!")

if __name__ == "__main__":
    main()

