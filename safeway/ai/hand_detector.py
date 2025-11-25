"""
Module de détection des mains pour SafeWay
"""
import cv2
import numpy as np
import mediapipe as mp
from typing import Optional, Dict, List
from core.logger import setup_logger

logger = setup_logger("HandDetector")

class HandDetector:
    """
    Détecte les mains avec MediaPipe Hands
    """
    
    def __init__(self):
        """Initialise le détecteur de mains MediaPipe"""
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
    
    def detect(self, frame: np.ndarray) -> Dict:
        """
        Détecte les mains dans l'image
        
        Args:
            frame: Image BGR (OpenCV)
            
        Returns:
            Dictionnaire avec les résultats de détection
        """
        results = {
            'hands_detected': False,
            'num_hands': 0,
            'left_hand_detected': False,
            'right_hand_detected': False,
            'hands_landmarks': []
        }
        
        if frame is None:
            return results
        
        # Convertir BGR en RGB pour MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Détection
        hand_results = self.hands.process(rgb_frame)
        
        if not hand_results.multi_hand_landmarks:
            return results
        
        results['hands_detected'] = True
        results['num_hands'] = len(hand_results.multi_hand_landmarks)
        results['hands_landmarks'] = hand_results.multi_hand_landmarks
        
        # Identifier les mains gauche et droite
        if hand_results.multi_handedness:
            for hand_handedness in hand_results.multi_handedness:
                label = hand_handedness.classification[0].label
                if label == "Left":
                    results['left_hand_detected'] = True
                elif label == "Right":
                    results['right_hand_detected'] = True
        
        return results
    
    def draw_landmarks(self, frame: np.ndarray, results: Dict) -> np.ndarray:
        """
        Dessine les landmarks des mains sur l'image
        
        Args:
            frame: Image BGR
            results: Résultats de détection
            
        Returns:
            Image avec landmarks dessinés
        """
        if not results['hands_detected']:
            return frame
        
        annotated_frame = frame.copy()
        
        # Dessiner les landmarks des mains
        for hand_landmarks in results['hands_landmarks']:
            self.mp_drawing.draw_landmarks(
                annotated_frame,
                hand_landmarks,
                self.mp_hands.HAND_CONNECTIONS,
                self.mp_drawing_styles.get_default_hand_landmarks_style(),
                self.mp_drawing_styles.get_default_hand_connections_style()
            )
        
        return annotated_frame
    
    def is_hand_on_steering_wheel(self, results: Dict) -> bool:
        """
        Détermine si une main est sur le volant (simplifié)
        Pour l'instant, on considère qu'une main détectée = main sur le volant
        
        Args:
            results: Résultats de détection
            
        Returns:
            True si une main est détectée
        """
        return results['hands_detected']
    
    def release(self):
        """Libère les ressources"""
        if hasattr(self, 'hands'):
            self.hands.close()

