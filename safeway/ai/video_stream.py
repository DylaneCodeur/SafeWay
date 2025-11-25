"""
Module de gestion du flux vidéo pour SafeWay
"""
import cv2
import numpy as np
import time
from typing import Optional, Tuple
from config.settings import CAMERA_INDEX, FRAME_WIDTH, FRAME_HEIGHT
from core.logger import setup_logger

logger = setup_logger("VideoStream")

class VideoStream:
    """
    Gère l'acquisition vidéo depuis la caméra
    """
    
    def __init__(self, camera_index: int = CAMERA_INDEX):
        """
        Initialise le flux vidéo
        
        Args:
            camera_index: Index de la caméra à utiliser
        """
        self.camera_index = camera_index
        self.cap: Optional[cv2.VideoCapture] = None
        self.is_opened = False
        
    def start(self) -> bool:
        """
        Ouvre la caméra et l'initialise
        
        Returns:
            True si la caméra est ouverte avec succès
        """
        try:
            logger.info(f"Tentative d'ouverture de la caméra {self.camera_index}...")
            self.cap = cv2.VideoCapture(self.camera_index)
            
            if not self.cap.isOpened():
                logger.error(f"Impossible d'ouvrir la caméra {self.camera_index}")
                # Essayer d'autres indices de caméra
                for i in range(1, 4):
                    logger.info(f"Tentative avec la caméra {i}...")
                    self.cap = cv2.VideoCapture(i)
                    if self.cap.isOpened():
                        self.camera_index = i
                        logger.info(f"Caméra {i} ouverte avec succès")
                        break
                else:
                    logger.error("Aucune caméra disponible")
                    return False
            
            # Configuration de la résolution (sans forcer si non supportée)
            actual_width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            actual_height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            logger.info(f"Résolution actuelle de la caméra: {int(actual_width)}x{int(actual_height)}")
            
            # Essayer de définir la résolution souhaitée
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
            
            # Attendre un peu pour que la caméra s'initialise
            time.sleep(0.5)
            
            # Lire quelques frames pour "chauffer" la caméra
            logger.info("Initialisation de la caméra (lecture de frames de démarrage)...")
            for i in range(5):
                ret, _ = self.cap.read()
                if ret:
                    logger.info(f"Frame de démarrage {i+1}/5 lue avec succès")
                else:
                    logger.warning(f"Frame de démarrage {i+1}/5 échouée")
                time.sleep(0.1)
            
            # Vérifier que la caméra fonctionne vraiment
            ret, test_frame = self.cap.read()
            if not ret or test_frame is None:
                logger.error("La caméra ne peut pas lire de frames")
                self.cap.release()
                return False
            
            self.is_opened = True
            logger.info(f"Caméra {self.camera_index} initialisée avec succès (résolution: {test_frame.shape[1]}x{test_frame.shape[0]})")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de l'ouverture de la caméra: {e}", exc_info=True)
            if self.cap is not None:
                self.cap.release()
            return False
    
    def read_frame(self) -> Tuple[bool, Optional[np.ndarray]]:
        """
        Lit une frame depuis la caméra
        
        Returns:
            Tuple (succès, frame) où frame est une image numpy ou None
        """
        if not self.is_opened or self.cap is None:
            return False, None
        
        try:
            ret, frame = self.cap.read()
            
            if not ret or frame is None:
                # Réessayer une fois
                ret, frame = self.cap.read()
                if not ret or frame is None:
                    return False, None
            
            return True, frame
            
        except Exception as e:
            logger.error(f"Erreur lors de la lecture de la frame: {e}")
            return False, None
    
    def release(self):
        """
        Ferme la caméra et libère les ressources
        """
        if self.cap is not None:
            self.cap.release()
            self.is_opened = False
            logger.info("Caméra fermée")
    
    def __enter__(self):
        """Context manager entry"""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.release()

