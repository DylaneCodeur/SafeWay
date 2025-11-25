"""
Module d'analyse de l'état du conducteur pour SafeWay
"""
import time
from typing import Dict, List, Optional
from collections import deque
from config.settings import (
    EYE_CLOSED_TIME_MS,
    YAWN_COUNT_THRESHOLD,
    YAWN_TIME_WINDOW,
    DISTRACTION_TIME_MS,
    ABSENCE_TIME_MS,
    BLINK_RATE_THRESHOLD,
    HEAD_MOVEMENT_THRESHOLD,
    GAZE_DEVIATION_THRESHOLD
)
from core.logger import setup_logger
from core.utils import get_current_timestamp

logger = setup_logger("StateAnalyzer")

class StateAnalyzer:
    """
    Analyse l'état du conducteur et détecte les comportements dangereux
    """
    
    def __init__(self):
        """Initialise l'analyseur d'état"""
        # Historique pour les yeux fermés
        self.eyes_closed_start_time: Optional[float] = None
        self.blink_timestamps: deque = deque(maxlen=30)  # Historique des clignements
        
        # Historique pour les bâillements
        self.yawn_timestamps: deque = deque(maxlen=100)
        
        # Historique pour la distraction (regard détourné)
        self.distraction_start_time: Optional[float] = None
        self.last_head_position: Optional[str] = None
        self.head_positions_history: deque = deque(maxlen=10)  # Historique positions tête
        
        # Historique pour l'absence
        self.face_absent_start_time: Optional[float] = None
        
        # Historique pour la cohérence
        self.last_eye_state = True
        self.eye_state_changes: deque = deque(maxlen=20)
        
        # État actuel
        self.current_state = {
            'fatigue_detected': False,
            'distraction_detected': False,
            'phone_detected': False,
            'driver_absent': False,
            'yawn_detected': False,
            'abnormal_blink_rate': False,
            'excessive_head_movement': False
        }
    
    def analyze(self, face_results: Dict, hand_results: Dict, yolo_results: Dict) -> Dict:
        """
        Analyse l'état du conducteur basé sur les résultats de détection
        
        Args:
            face_results: Résultats de détection du visage
            hand_results: Résultats de détection des mains
            yolo_results: Résultats de détection YOLO
            
        Returns:
            Dictionnaire avec l'état analysé et les alertes
        """
        current_time = get_current_timestamp()
        alerts = []
        
        # Réinitialiser l'état
        self.current_state = {
            'fatigue_detected': False,
            'distraction_detected': False,
            'phone_detected': False,
            'driver_absent': False,
            'yawn_detected': False,
            'abnormal_blink_rate': False,
            'excessive_head_movement': False
        }
        
        # 1. Vérifier l'absence du conducteur
        if not face_results.get('face_detected', False):
            if self.face_absent_start_time is None:
                self.face_absent_start_time = current_time
            else:
                absent_duration = (current_time - self.face_absent_start_time) * 1000
                if absent_duration > ABSENCE_TIME_MS:
                    self.current_state['driver_absent'] = True
                    alerts.append({
                        'type': 'driver_absent',
                        'message': 'Conducteur absent',
                        'severity': 'high'
                    })
        else:
            self.face_absent_start_time = None
        
        # 2. Vérifier la fatigue (yeux fermés) avec détection de clignement
        if face_results.get('face_detected', False):
            eyes_open = face_results.get('eyes_open', True)
            
            # Détecter les clignements (transition fermé -> ouvert)
            if self.last_eye_state == False and eyes_open == True:
                self.blink_timestamps.append(current_time)
            self.last_eye_state = eyes_open
            self.eye_state_changes.append((current_time, eyes_open))
            
            # Calculer le taux de clignement (clignements par seconde)
            if len(self.blink_timestamps) >= 2:
                time_window = current_time - self.blink_timestamps[0]
                if time_window > 0:
                    blink_rate = len(self.blink_timestamps) / time_window
                    if blink_rate < BLINK_RATE_THRESHOLD:  # Taux anormalement bas = fatigue
                        self.current_state['abnormal_blink_rate'] = True
                        if not self.current_state['fatigue_detected']:
                            alerts.append({
                                'type': 'fatigue',
                                'message': 'Taux de clignement anormalement bas',
                                'severity': 'medium'
                            })
            
            if not eyes_open:
                if self.eyes_closed_start_time is None:
                    self.eyes_closed_start_time = current_time
                else:
                    closed_duration = (current_time - self.eyes_closed_start_time) * 1000
                    if closed_duration > EYE_CLOSED_TIME_MS:
                        self.current_state['fatigue_detected'] = True
                        alerts.append({
                            'type': 'fatigue',
                            'message': 'Somnolence détectée',
                            'severity': 'high'
                        })
            else:
                self.eyes_closed_start_time = None
            
            # 3. Vérifier les bâillements
            mouth_open = face_results.get('mouth_open', False)
            if mouth_open:
                self.yawn_timestamps.append(current_time)
                self.current_state['yawn_detected'] = True
            
            # Compter les bâillements dans la fenêtre de temps
            recent_yawns = [
                ts for ts in self.yawn_timestamps
                if current_time - ts <= YAWN_TIME_WINDOW
            ]
            
            if len(recent_yawns) >= YAWN_COUNT_THRESHOLD:
                # Éviter les alertes répétitives
                if not any(a['type'] == 'yawn' for a in alerts):
                    alerts.append({
                        'type': 'yawn',
                        'message': f'Fatigue détectée ({len(recent_yawns)} bâillements)',
                        'severity': 'medium'
                    })
            
            # 4. Vérifier la distraction (regard détourné) avec détection de mouvement excessif
            head_position = face_results.get('head_position', 'center')
            self.head_positions_history.append((current_time, head_position))
            
            # Détecter les mouvements excessifs de tête
            if len(self.head_positions_history) >= 5:
                recent_positions = [pos[1] for pos in list(self.head_positions_history)[-5:]]
                position_changes = sum(1 for i in range(len(recent_positions)-1) 
                                     if recent_positions[i] != recent_positions[i+1])
                if position_changes >= 4:  # Trop de changements = mouvement excessif
                    self.current_state['excessive_head_movement'] = True
                    alerts.append({
                        'type': 'distraction',
                        'message': 'Mouvements de tête excessifs détectés',
                        'severity': 'medium'
                    })
            
            if head_position in ['left', 'right']:
                if self.distraction_start_time is None:
                    self.distraction_start_time = current_time
                    self.last_head_position = head_position
                elif head_position == self.last_head_position:
                    distraction_duration = (current_time - self.distraction_start_time) * 1000
                    if distraction_duration > DISTRACTION_TIME_MS:
                        self.current_state['distraction_detected'] = True
                        alerts.append({
                            'type': 'distraction',
                            'message': 'Distraction détectée (regard détourné)',
                            'severity': 'medium'
                        })
                else:
                    # La tête a changé de position, réinitialiser
                    self.distraction_start_time = current_time
                    self.last_head_position = head_position
            else:
                self.distraction_start_time = None
                self.last_head_position = None
        
        # 5. Vérifier la détection de téléphone
        if yolo_results.get('phone_detected', False):
            self.current_state['phone_detected'] = True
            alerts.append({
                'type': 'phone',
                'message': 'Téléphone détecté - Danger!',
                'severity': 'high'
            })
        
        return {
            'state': self.current_state,
            'alerts': alerts,
            'timestamp': current_time
        }

