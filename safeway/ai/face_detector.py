"""
Module de détection du visage et analyse des yeux/bouche pour SafeWay
"""
import cv2
import numpy as np
import mediapipe as mp
from typing import Optional, Dict, List, Tuple
from config.settings import EYE_CLOSED_THRESHOLD
from core.logger import setup_logger
from core.utils import calculate_eye_aspect_ratio, calculate_mouth_aspect_ratio

logger = setup_logger("FaceDetector")

class FaceDetector:
    """
    Détecte le visage et analyse les yeux et la bouche avec MediaPipe
    """
    
    def __init__(self):
        """Initialise le détecteur de visage MediaPipe"""
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.6,  # Augmenté pour meilleure précision
            min_tracking_confidence=0.6    # Augmenté pour meilleure précision
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        # Indices des landmarks pour les yeux et la bouche (MediaPipe Face Mesh)
        # Œil gauche
        self.LEFT_EYE_INDICES = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
        # Œil droit
        self.RIGHT_EYE_INDICES = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
        # Bouche
        self.MOUTH_INDICES = [61, 146, 91, 181, 84, 17, 314, 405, 320, 307, 375, 321, 308, 324, 318]
        
        # Indices simplifiés pour EAR et MAR
        # Œil gauche (6 points pour EAR)
        self.LEFT_EYE_EAR_INDICES = [33, 160, 158, 133, 153, 144]
        # Œil droit (6 points pour EAR)
        self.RIGHT_EYE_EAR_INDICES = [362, 385, 387, 263, 373, 380]
        # Bouche (8 points pour MAR)
        self.MOUTH_MAR_INDICES = [61, 84, 17, 314, 405, 320, 307, 375]
        
    def detect(self, frame: np.ndarray) -> Dict:
        """
        Détecte le visage et analyse les yeux et la bouche
        
        Args:
            frame: Image BGR (OpenCV)
            
        Returns:
            Dictionnaire avec les résultats de détection
        """
        results = {
            'face_detected': False,
            'eyes_open': True,
            'left_eye_open': True,
            'right_eye_open': True,
            'mouth_open': False,
            'head_position': 'center',  # center, left, right, down
            'landmarks': None,
            'left_ear': 0.0,
            'right_ear': 0.0,
            'mar': 0.0
        }
        
        if frame is None:
            return results
        
        # Convertir BGR en RGB pour MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Détection
        face_results = self.face_mesh.process(rgb_frame)
        
        if not face_results.multi_face_landmarks:
            return results
        
        results['face_detected'] = True
        
        # Prendre le premier visage détecté
        face_landmarks = face_results.multi_face_landmarks[0]
        results['landmarks'] = face_landmarks
        
        h, w = frame.shape[:2]
        
        # Extraire les coordonnées des landmarks
        landmarks_2d = []
        for landmark in face_landmarks.landmark:
            x = int(landmark.x * w)
            y = int(landmark.y * h)
            landmarks_2d.append((x, y))
        
        # Calculer EAR pour l'œil gauche
        left_eye_points = [landmarks_2d[i] for i in self.LEFT_EYE_EAR_INDICES]
        left_ear = calculate_eye_aspect_ratio(left_eye_points)
        results['left_ear'] = left_ear
        results['left_eye_open'] = left_ear > EYE_CLOSED_THRESHOLD
        
        # Calculer EAR pour l'œil droit
        right_eye_points = [landmarks_2d[i] for i in self.RIGHT_EYE_EAR_INDICES]
        right_ear = calculate_eye_aspect_ratio(right_eye_points)
        results['right_ear'] = right_ear
        results['right_eye_open'] = right_ear > EYE_CLOSED_THRESHOLD
        
        # Les deux yeux doivent être ouverts
        results['eyes_open'] = results['left_eye_open'] and results['right_eye_open']
        
        # Calculer MAR pour la bouche
        mouth_points = [landmarks_2d[i] for i in self.MOUTH_MAR_INDICES]
        mar = calculate_mouth_aspect_ratio(mouth_points)
        results['mar'] = mar
        results['mouth_open'] = mar > 0.5  # Seuil pour bâillement
        
        # Estimer la position de la tête (simplifié)
        # Utiliser le nez comme référence
        nose_tip = landmarks_2d[1]  # Point du nez
        face_center_x = w / 2
        
        if nose_tip[0] < face_center_x - 50:
            results['head_position'] = 'left'
        elif nose_tip[0] > face_center_x + 50:
            results['head_position'] = 'right'
        elif nose_tip[1] > h / 2 + 30:
            results['head_position'] = 'down'
        else:
            results['head_position'] = 'center'
        
        return results
    
    def draw_landmarks(self, frame: np.ndarray, results: Dict) -> np.ndarray:
        """
        Dessine les landmarks du visage sur l'image
        
        Args:
            frame: Image BGR
            results: Résultats de détection
            
        Returns:
            Image avec landmarks dessinés
        """
        if not results['face_detected'] or results['landmarks'] is None:
            return frame
        
        annotated_frame = frame.copy()
        h, w = frame.shape[:2]
        
        try:
            # Dessiner les contours du visage (plus sûr)
            self.mp_drawing.draw_landmarks(
                annotated_frame,
                results['landmarks'],
                self.mp_face_mesh.FACEMESH_CONTOURS,
                None,
                self.mp_drawing_styles.get_default_face_mesh_contours_style()
            )
        except Exception as e:
            logger.warning(f"Erreur lors du dessin des contours: {e}")
        
        # Dessiner manuellement les points des yeux pour éviter les erreurs de connexions
        try:
            landmarks = results['landmarks']
            # Dessiner les points de l'œil gauche
            for idx in self.LEFT_EYE_EAR_INDICES:
                if idx < len(landmarks.landmark):
                    landmark = landmarks.landmark[idx]
                    x = int(landmark.x * w)
                    y = int(landmark.y * h)
                    cv2.circle(annotated_frame, (x, y), 2, (0, 255, 0), -1)
            
            # Dessiner les points de l'œil droit
            for idx in self.RIGHT_EYE_EAR_INDICES:
                if idx < len(landmarks.landmark):
                    landmark = landmarks.landmark[idx]
                    x = int(landmark.x * w)
                    y = int(landmark.y * h)
                    cv2.circle(annotated_frame, (x, y), 2, (0, 255, 0), -1)
        except Exception as e:
            logger.warning(f"Erreur lors du dessin des yeux: {e}")
        
        return annotated_frame
    
    def release(self):
        """Libère les ressources"""
        if hasattr(self, 'face_mesh'):
            self.face_mesh.close()

