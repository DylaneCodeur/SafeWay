"""
Utilitaires pour SafeWay
"""
import time
from typing import List, Tuple
import numpy as np

def calculate_distance(point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
    """
    Calcule la distance euclidienne entre deux points
    
    Args:
        point1: Premier point (x, y)
        point2: Deuxième point (x, y)
        
    Returns:
        Distance entre les points
    """
    return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def calculate_eye_aspect_ratio(eye_landmarks: List) -> float:
    """
    Calcule le ratio d'aspect de l'œil (EAR - Eye Aspect Ratio)
    Plus le ratio est bas, plus l'œil est fermé
    
    Args:
        eye_landmarks: Liste des landmarks de l'œil (6 points)
        
    Returns:
        Ratio d'aspect de l'œil
    """
    if len(eye_landmarks) < 6:
        return 1.0
    
    # Points pour calculer EAR
    # Vertical distances
    vertical_1 = calculate_distance(eye_landmarks[1], eye_landmarks[5])
    vertical_2 = calculate_distance(eye_landmarks[2], eye_landmarks[4])
    
    # Horizontal distance
    horizontal = calculate_distance(eye_landmarks[0], eye_landmarks[3])
    
    # EAR = (vertical_1 + vertical_2) / (2 * horizontal)
    if horizontal == 0:
        return 1.0
    
    ear = (vertical_1 + vertical_2) / (2.0 * horizontal)
    return ear

def calculate_mouth_aspect_ratio(mouth_landmarks: List) -> float:
    """
    Calcule le ratio d'aspect de la bouche (MAR - Mouth Aspect Ratio)
    Plus le ratio est élevé, plus la bouche est ouverte (bâillement)
    
    Args:
        mouth_landmarks: Liste des landmarks de la bouche
        
    Returns:
        Ratio d'aspect de la bouche
    """
    if len(mouth_landmarks) < 6:
        return 0.0
    
    # Points pour calculer MAR
    # Vertical distances
    vertical_1 = calculate_distance(mouth_landmarks[1], mouth_landmarks[7])
    vertical_2 = calculate_distance(mouth_landmarks[2], mouth_landmarks[6])
    vertical_3 = calculate_distance(mouth_landmarks[3], mouth_landmarks[5])
    
    # Horizontal distance
    horizontal = calculate_distance(mouth_landmarks[0], mouth_landmarks[4])
    
    if horizontal == 0:
        return 0.0
    
    mar = (vertical_1 + vertical_2 + vertical_3) / (3.0 * horizontal)
    return mar

def get_current_timestamp() -> float:
    """
    Retourne le timestamp actuel en secondes
    
    Returns:
        Timestamp actuel
    """
    return time.time()

