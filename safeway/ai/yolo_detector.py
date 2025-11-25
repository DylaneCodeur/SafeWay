"""
Module de détection d'objets avec YOLO pour SafeWay
"""
import cv2
import numpy as np
from ultralytics import YOLO
from typing import Optional, Dict, List
from pathlib import Path
from config.settings import YOLO_MODEL_PATH, PHONE_CLASS_ID, USE_YOLO11
from core.logger import setup_logger

logger = setup_logger("YOLODetector")

class YOLODetector:
    """
    Détecte les objets (notamment téléphones) avec YOLOv11 (ultra performant)
    """
    
    def __init__(self, model_path: Optional[Path] = None):
        """
        Initialise le détecteur YOLO
        
        Args:
            model_path: Chemin vers le modèle YOLO (si None, utilise le chemin par défaut)
        """
        self.model_path = model_path or YOLO_MODEL_PATH
        self.model: Optional[YOLO] = None
        self.phone_class_id = PHONE_CLASS_ID
        
    def load_model(self) -> bool:
        """
        Charge le modèle YOLOv11 (ultra performant et fluide)
        
        Returns:
            True si le modèle est chargé avec succès
        """
        try:
            if not self.model_path.exists() or USE_YOLO11:
                logger.info("Chargement du modèle YOLOv11 (ultra performant)...")
                # Essayer YOLOv11 d'abord
                model_names = ["yolo11n.pt", "yolo11s.pt", "yolov8s.pt", "yolov8n.pt"]
                
                for model_name in model_names:
                    try:
                        logger.info(f"Tentative de chargement de {model_name}...")
                        self.model = YOLO(model_name)
                        
                        # Sauvegarder le modèle téléchargé
                        import shutil
                        if Path(model_name).exists():
                            shutil.copy(model_name, self.model_path)
                            logger.info(f"Modèle {model_name} téléchargé et sauvegardé")
                            break
                    except Exception as e:
                        logger.warning(f"Impossible de charger {model_name}: {e}")
                        continue
                
                if self.model is None:
                    logger.error("Aucun modèle YOLO disponible")
                    return False
            else:
                self.model = YOLO(str(self.model_path))
            
            # Optimiser le modèle pour l'inférence ultra-rapide
            try:
                self.model.fuse()  # Fusionner les couches pour plus de performance
            except:
                pass  # Certains modèles peuvent ne pas supporter fuse()
            
            # Compiler le modèle pour accélération (si disponible)
            try:
                self.model.compile()  # Compilation pour meilleures performances
            except:
                pass  # Compilation optionnelle
            
            logger.info(f"Modèle YOLO chargé et optimisé depuis {self.model_path}")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors du chargement du modèle YOLO: {e}")
            return False
    
    def detect(self, frame: np.ndarray) -> Dict:
        """
        Détecte les objets dans l'image
        
        Args:
            frame: Image BGR (OpenCV)
            
        Returns:
            Dictionnaire avec les résultats de détection
        """
        results = {
            'phone_detected': False,
            'phone_confidence': 0.0,
            'phone_bbox': None,
            'all_detections': []
        }
        
        if self.model is None:
            if not self.load_model():
                return results
        
        if frame is None:
            return results
        
        try:
            # YOLO attend des images RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Détection ultra-optimisée pour fluidité maximale
            yolo_results = self.model(
                rgb_frame, 
                verbose=False, 
                imgsz=640,  # Taille optimale pour performance
                conf=0.45,  # Seuil de confiance ajusté
                iou=0.45,   # Seuil IoU pour NMS
                half=False,  # Utiliser float32 pour compatibilité
                device='cpu',  # Utiliser CPU (ou 'cuda' si GPU disponible)
                max_det=10  # Maximum 10 détections par image
            )
            
            # Parser les résultats
            if yolo_results and len(yolo_results) > 0:
                result = yolo_results[0]
                
                if result.boxes is not None:
                    boxes = result.boxes
                    
                    for i in range(len(boxes)):
                        cls = int(boxes.cls[i])
                        conf = float(boxes.conf[i])
                        bbox = boxes.xyxy[i].cpu().numpy()
                        
                        detection = {
                            'class_id': cls,
                            'confidence': conf,
                            'bbox': bbox.tolist()
                        }
                        results['all_detections'].append(detection)
                        
                        # Vérifier si c'est un téléphone
                        if cls == self.phone_class_id and conf > 0.5:
                            results['phone_detected'] = True
                            results['phone_confidence'] = conf
                            results['phone_bbox'] = bbox.tolist()
            
        except Exception as e:
            logger.error(f"Erreur lors de la détection YOLO: {e}")
        
        return results
    
    def draw_detections(self, frame: np.ndarray, results: Dict) -> np.ndarray:
        """
        Dessine les détections sur l'image
        
        Args:
            frame: Image BGR
            results: Résultats de détection
            
        Returns:
            Image avec détections dessinées
        """
        if not results['phone_detected']:
            return frame
        
        annotated_frame = frame.copy()
        bbox = results['phone_bbox']
        
        if bbox:
            x1, y1, x2, y2 = map(int, bbox)
            
            # Dessiner le rectangle
            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            
            # Ajouter le texte
            label = f"Telephone {results['phone_confidence']:.2f}"
            cv2.putText(annotated_frame, label, (x1, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        
        return annotated_frame

