"""
Module de gestion des alertes pour SafeWay
"""
import cv2
import pygame
import time
import numpy as np
import threading
import subprocess
import platform
from typing import Dict, List, Optional
from pathlib import Path
from config.settings import ALERT_SOUND_ENABLED, ALERT_VISUAL_ENABLED, ALERT_VOICE_ENABLED
from core.logger import setup_logger

logger = setup_logger("AlertManager")

# Messages personnalisés en français (ultra cohérents)
ALERT_MESSAGES = {
    'phone': "Veuillez ne pas utiliser le téléphone au volant",
    'fatigue': "Veillez à ne pas dormir au volant, restez vigilant",
    'distraction': "Vous ne regardez pas devant vous, concentrez-vous sur la route",
    'driver_absent': "Conducteur absent, veuillez reprendre le contrôle du véhicule",
    'yawn': "Signes de fatigue détectés, faites une pause si nécessaire",
    'abnormal_blink': "Taux de clignement anormal, vous semblez fatigué",
    'excessive_movement': "Mouvements excessifs détectés, restez concentré"
}

class AlertManager:
    """
    Gère les alertes visuelles, sonores et vocales
    """
    
    def __init__(self):
        """Initialise le gestionnaire d'alertes"""
        self.sound_enabled = ALERT_SOUND_ENABLED
        self.visual_enabled = ALERT_VISUAL_ENABLED
        self.voice_enabled = ALERT_VOICE_ENABLED
        
        # Initialiser pygame pour les sons
        if self.sound_enabled:
            try:
                pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
                logger.info("Pygame mixer initialisé")
            except Exception as e:
                logger.warning(f"Impossible d'initialiser pygame mixer: {e}")
                self.sound_enabled = False
        
        # Initialiser TTS (Text-to-Speech)
        self.tts_enabled = False
        self.tts_lock = threading.Lock()
        if self.voice_enabled:
            self._init_tts()
        
        # Dernière alerte pour éviter les répétitions
        self.last_alert_time: Dict[str, float] = {}
        self.alert_cooldown = 3.0  # Secondes entre deux alertes du même type
        self.last_spoken_message = None
        self.last_speech_time = 0.0
    
    def trigger_alert(self, alert: Dict, frame: Optional[cv2.typing.MatLike] = None) -> Optional[cv2.typing.MatLike]:
        """
        Déclenche une alerte
        
        Args:
            alert: Dictionnaire avec les informations de l'alerte
            frame: Image sur laquelle dessiner l'alerte (optionnel)
            
        Returns:
            Image avec alerte dessinée (si frame fourni)
        """
        alert_type = alert.get('type', 'unknown')
        severity = alert.get('severity', 'medium')
        
        # Obtenir le message personnalisé en français
        message = ALERT_MESSAGES.get(alert_type, alert.get('message', 'Alerte de sécurité'))
        
        # Vérifier le cooldown
        current_time = time.time()
        if alert_type in self.last_alert_time:
            if current_time - self.last_alert_time[alert_type] < self.alert_cooldown:
                return frame
        
        self.last_alert_time[alert_type] = current_time
        
        logger.warning(f"ALERTE: {message} (Type: {alert_type}, Sévérité: {severity})")
        
        # Alerte sonore
        if self.sound_enabled:
            self._play_sound(severity)
        
        # Alerte visuelle
        if self.visual_enabled and frame is not None:
            frame = self._draw_visual_alert(frame, message, severity)
        
        # Alerte vocale (TTS)
        if self.voice_enabled and self.tts_enabled:
            # Éviter de répéter le même message trop souvent
            if message != self.last_spoken_message or (current_time - self.last_speech_time) > 5.0:
                self._speak_message(message)
                self.last_spoken_message = message
                self.last_speech_time = current_time
        
        return frame
    
    def _play_sound(self, severity: str):
        """
        Joue un son d'alerte
        
        Args:
            severity: Niveau de sévérité (low, medium, high)
        """
        try:
            if severity == 'high':
                frequency = 800
                duration = 500  # ms
            elif severity == 'medium':
                frequency = 600
                duration = 300
            else:
                frequency = 400
                duration = 200
            
            # Générer un bip avec pygame (utiliser numpy array correctement)
            sample_rate = 22050
            frames = int(duration * sample_rate / 1000)
            
            # Générer une onde sinusoïdale avec numpy (vectorisé pour performance)
            t = np.arange(frames, dtype=np.float32) / sample_rate
            samples = (32767.0 * 0.4 * np.sin(2.0 * np.pi * frequency * t)).astype(np.int16)
            
            # Créer un array stéréo
            arr = np.zeros((frames, 2), dtype=np.int16)
            arr[:, 0] = samples
            arr[:, 1] = samples
            
            # Convertir en format pygame (transposer si nécessaire)
            try:
                sound = pygame.sndarray.make_sound(arr)
                sound.play()
            except Exception as e:
                # Fallback: essayer avec un format mono
                try:
                    sound = pygame.sndarray.make_sound(samples)
                    sound.play()
                except:
                    logger.warning(f"Impossible de jouer le son: {e}")
            
        except Exception as e:
            logger.error(f"Erreur lors de la lecture du son: {e}")
    
    def _init_tts(self):
        """Initialise le système de synthèse vocale"""
        try:
            # Sur macOS, utiliser la commande 'say' native
            if platform.system() == 'Darwin':
                self.tts_enabled = True
                self.tts_method = 'say'
                logger.info("TTS initialisé avec 'say' (macOS)")
            else:
                # Essayer pyttsx3 pour autres systèmes
                try:
                    import pyttsx3
                    self.tts_engine = pyttsx3.init()
                    # Configurer la voix française si disponible
                    voices = self.tts_engine.getProperty('voices')
                    for voice in voices:
                        if 'french' in voice.name.lower() or 'fr' in voice.id.lower():
                            self.tts_engine.setProperty('voice', voice.id)
                            break
                    self.tts_engine.setProperty('rate', 150)  # Vitesse de parole
                    self.tts_enabled = True
                    self.tts_method = 'pyttsx3'
                    logger.info("TTS initialisé avec pyttsx3")
                except ImportError:
                    logger.warning("pyttsx3 non disponible, TTS désactivé")
                    self.tts_enabled = False
        except Exception as e:
            logger.warning(f"Impossible d'initialiser TTS: {e}")
            self.tts_enabled = False
    
    def _speak_message(self, message: str):
        """
        Énonce un message vocal
        
        Args:
            message: Message à énoncer
        """
        if not self.tts_enabled:
            return
        
        def speak():
            try:
                with self.tts_lock:
                    if self.tts_method == 'say':
                        # Utiliser la commande 'say' de macOS
                        subprocess.run(['say', '-v', 'Thomas', message], 
                                     check=False, timeout=10)
                    elif self.tts_method == 'pyttsx3':
                        self.tts_engine.say(message)
                        self.tts_engine.runAndWait()
            except Exception as e:
                logger.error(f"Erreur lors de la synthèse vocale: {e}")
        
        # Lancer dans un thread pour ne pas bloquer
        thread = threading.Thread(target=speak, daemon=True)
        thread.start()
    
    def _draw_visual_alert(self, frame: cv2.typing.MatLike, message: str, severity: str) -> cv2.typing.MatLike:
        """
        Dessine une alerte visuelle sur l'image
        
        Args:
            frame: Image BGR
            message: Message d'alerte
            severity: Niveau de sévérité
            
        Returns:
            Image avec alerte dessinée
        """
        h, w = frame.shape[:2]
        
        # Couleur selon la sévérité
        if severity == 'high':
            color = (0, 0, 255)  # Rouge
            bg_color = (0, 0, 200)
        elif severity == 'medium':
            color = (0, 165, 255)  # Orange
            bg_color = (0, 140, 200)
        else:
            color = (0, 255, 255)  # Jaune
            bg_color = (0, 200, 200)
        
        # Rectangle de fond
        cv2.rectangle(frame, (10, 10), (w - 10, 80), bg_color, -1)
        cv2.rectangle(frame, (10, 10), (w - 10, 80), color, 3)
        
        # Texte
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.7
        thickness = 2
        
        # Calculer la position du texte (centré)
        text_size = cv2.getTextSize(message, font, font_scale, thickness)[0]
        text_x = (w - text_size[0]) // 2
        text_y = 50
        
        cv2.putText(frame, message, (text_x, text_y), font, font_scale, (255, 255, 255), thickness)
        
        # Indicateur clignotant (simplifié)
        if int(time.time() * 2) % 2 == 0:  # Clignote toutes les 0.5s
            cv2.circle(frame, (w - 30, 40), 15, color, -1)
        
        return frame
    
    def release(self):
        """Libère les ressources"""
        if self.sound_enabled:
            try:
                pygame.mixer.quit()
            except:
                pass
        if hasattr(self, 'tts_engine') and self.tts_method == 'pyttsx3':
            try:
                self.tts_engine.stop()
            except:
                pass

