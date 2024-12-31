import cv2
import numpy as np
from fer import FER
import pyttsx3
import time
import random
import threading
import queue
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

@dataclass
class FaceData:
    box: Tuple[int, int, int, int]
    emotions: Dict[str, float]
    age: str
    gender: str

class EmotionClassifier:
    EMOTION_THRESHOLDS = {
        'very': 0.7,
        'moderate': 0.3
    }
    
    @staticmethod
    def categorize_emotions(emotions: Dict[str, float]) -> Dict[str, bool]:
        return {
            'very angry': emotions.get('angry', 0) > EmotionClassifier.EMOTION_THRESHOLDS['very'],
            'angry': EmotionClassifier.EMOTION_THRESHOLDS['moderate'] < emotions.get('angry', 0) <= EmotionClassifier.EMOTION_THRESHOLDS['very'],
            'very sad': emotions.get('sad', 0) > EmotionClassifier.EMOTION_THRESHOLDS['very'],
            'sad': EmotionClassifier.EMOTION_THRESHOLDS['moderate'] < emotions.get('sad', 0) <= EmotionClassifier.EMOTION_THRESHOLDS['very'],
            'very happy': emotions.get('happy', 0) > EmotionClassifier.EMOTION_THRESHOLDS['very'],
            'happy': EmotionClassifier.EMOTION_THRESHOLDS['moderate'] < emotions.get('happy', 0) <= EmotionClassifier.EMOTION_THRESHOLDS['very'],
            'very surprised': emotions.get('surprise', 0) > EmotionClassifier.EMOTION_THRESHOLDS['very'],
            'surprised': EmotionClassifier.EMOTION_THRESHOLDS['moderate'] < emotions.get('surprise', 0) <= EmotionClassifier.EMOTION_THRESHOLDS['very'],
            'very feared': emotions.get('fear', 0) > EmotionClassifier.EMOTION_THRESHOLDS['very'],
            'feared': EmotionClassifier.EMOTION_THRESHOLDS['moderate'] < emotions.get('fear', 0) <= EmotionClassifier.EMOTION_THRESHOLDS['very']
        }

class SpeechEngine:
    def __init__(self):
        self.queue = queue.Queue()
        self.engine = pyttsx3.init()
        self.setup_voice()
        self.thread = threading.Thread(target=self._speak_worker)
        self.thread.daemon = True
        self.thread.start()

    def setup_voice(self):
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if 'female' in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
        self.engine.setProperty('rate', 150)

    def _speak_worker(self):
        while True:
            text = self.queue.get()
            if text == "STOP":
                break
            self.engine.say(text)
            self.engine.runAndWait()

    def say(self, text: str):
        self.queue.put(text)

    def stop(self):
        self.queue.put("STOP")

class SmartMirror:
    def __init__(self):
        self.setup_models()
        self.setup_camera()
        self.speech_engine = SpeechEngine()
        self.detector = FER(mtcnn=True)
        self.last_emotion = None
        self.last_time = 0
        self.running = True
        
        # Enhanced UI colors
        self.COLORS = {
            'happy': (0, 255, 0),      # Green
            'sad': (255, 0, 0),        # Red
            'angry': (0, 0, 255),      # Blue
            'surprised': (255, 255, 0), # Yellow
            'feared': (128, 0, 128),   # Purple
            'neutral': (255, 255, 255)  # White
        }
        
        self.load_compliments()

    def setup_models(self):
        self.age_net = cv2.dnn.readNetFromCaffe(
            'D:\\HARSHIT\\SMART MIRROR\\age_deploy.prototxt',
            'D:\\HARSHIT\\SMART MIRROR\\age_net.caffemodel'
        )
        self.gender_net = cv2.dnn.readNetFromCaffe(
            'D:\\HARSHIT\\SMART MIRROR\\gender_deploy.prototxt',
            'D:\\HARSHIT\\SMART MIRROR\\gender_net.caffemodel'
        )
        self.age_list = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
        self.gender_list = ['Male', 'Female']

    def setup_camera(self):
        self.cap = cv2.VideoCapture(0)
        # Set camera properties for better quality
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.cap.set(cv2.CAP_PROP_FPS, 60)

    def load_compliments(self):
        # Your existing compliments dictionary here
        self.compliments = compliments = {
    'very angry': [
        "Take a deep breath, you're stronger than this!",
        "Calm down, you can handle this!",
        "It's okay, things will get better!",
        "Don't let anger take over, you're in control!",
        "You have the power to overcome this!",
        "Deep breaths, you're amazing just as you are!",
        "You can handle anything that comes your way!",
        "Stay strong, you’ve got this!",
        "Let it go, your peace matters!",
        "This too shall pass, you’re stronger than this!"
    ],
    'angry': [
        "Stay calm, you've got this!",
        "Don't let anger control you!",
        "Keep your cool, you're doing great!",
        "You're better than letting anger win!",
        "Take a step back, things will get better!",
        "Stay strong, your calm is your power!",
        "Don’t let the small things get to you!",
        "Take a deep breath, you've got it under control!",
        "Anger is temporary, your peace is forever!",
        "You’re in charge of your emotions!"
    ],
    'very sad': [
        "It’s okay to feel this way. Better days are coming!",
        "You're not alone, things will improve!",
        "Hang in there, brighter days are ahead!",
        "You have the strength to get through this!",
        "Don’t be too hard on yourself, you’re doing great!",
        "Take it slow, tomorrow is a new day!",
        "Every storm eventually passes, keep going!",
        "You are stronger than you realize!",
        "Feel what you need to feel, then move forward!",
        "Better days are coming, I believe in you!"
    ],
    'sad': [
        "You’ve got this, keep going!",
        "Take it one step at a time, you're strong!",
        "Everything will be alright, stay positive!",
        "Your strength is remarkable, even in tough times!",
        "You have the power to turn things around!",
        "You’re not alone in this, we’re here for you!",
        "Keep moving forward, you’re doing great!",
        "Feel your feelings, but don’t let them control you!",
        "One small step today, a giant leap tomorrow!",
        "Your courage shines through even in sadness!"
    ],
    'very happy': [
        "Your happiness is infectious!",
        "You brighten up the room with your smile!",
        "Your joy is contagious!",
        "You light up the world with your energy!",
        "Seeing you happy makes everyone’s day better!",
        "You bring so much positivity wherever you go!",
        "Your laughter is pure joy to hear!",
        "You make the world a better place with your smile!",
        "Your happiness is like a ray of sunshine!",
        "Keep shining, the world needs your positivity!"
    ],
    'happy': [
        "Your smile lights up the room!",
        "You're glowing today, keep shining!",
        "Your positive energy is amazing!",
        "Your presence makes everything better!",
        "The world is a brighter place with you in it!",
        "Keep spreading that happiness around!",
        "You have the best energy, keep it up!",
        "Your smile is like a ray of sunshine!",
        "You’re amazing and it shows in your happiness!",
        "Your happiness is a gift to everyone around you!"
    ],
    'very surprised': [
        "Wow, you’re full of wonder today!",
        "What a delightful surprise!",
        "You are full of excitement!",
        "This is such a great surprise!",
        "You are full of energy and excitement!",
        "Wow, your energy is contagious!",
        "You have a wonderful sense of surprise!",
        "Every day with you is a pleasant surprise!",
        "Your surprise is refreshing and joyful!",
        "I love how full of wonder you are!"
    ],
    'surprised': [
        "What a pleasant surprise!",
        "This is unexpected, in a good way!",
        "You're full of pleasant surprises!",
        "What an exciting twist!",
        "I didn’t see that coming, but I’m glad it did!",
        "You bring excitement wherever you go!",
        "You have a way of making things interesting!",
        "You surprise me in the best way!",
        "Such a pleasant surprise, I love it!",
        "Your surprise makes everything more fun!"
    ],
    'very feared': [
        "You are braver than you think!",
        "Fear is just an illusion, you've got this!",
        "You are stronger than your fears!",
        "Don’t let fear stop you, you're unstoppable!",
        "Bravery is not the absence of fear, it's acting in spite of it!",
        "You have the courage to face anything!",
        "Fear is temporary, your courage is forever!",
        "You’re a warrior, nothing can hold you back!",
        "Keep going, you’re stronger than any fear!",
        "Fear doesn’t stand a chance against your courage!"
    ],
    'feared': [
        "It’s okay to be scared, you’re not alone!",
        "Courage is facing fear, and you're doing it!",
        "Fear is temporary, but your strength is permanent!",
        "You are capable of overcoming anything, even fear!",
        "Don’t let fear dictate your actions, you’re in control!",
        "Fear is just another hurdle to overcome, and you will!",
        "Your strength and courage are unmatched!",
        "Fear is normal, but so is your strength!",
        "You’re stronger than any fear you face!",
        "Courage is moving forward despite fear, and you’re doing it!"
    ]
}

    def get_age_gender(self, frame: np.ndarray) -> Tuple[str, str]:
        blob = cv2.dnn.blobFromImage(frame, 1, (227, 227), (78.43, 87.77, 114.90), swapRB=False)
        
        self.age_net.setInput(blob)
        age_preds = self.age_net.forward()
        
        self.gender_net.setInput(blob)
        gender_preds = self.gender_net.forward()
        
        age = self.age_list[age_preds[0].argmax()]
        gender = self.gender_list[gender_preds[0].argmax()]
        
        return age, gender

    def draw_face_info(self, frame: np.ndarray, face_data: FaceData, emotions_display: str):
        x, y, w, h = face_data.box
        
        # Determine dominant emotion and its color
        dominant_emotion = max(face_data.emotions.items(), key=lambda x: x[1])[0]
        color = self.COLORS.get(dominant_emotion, self.COLORS['neutral'])
        
        # Draw enhanced face rectangle
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        
        # Add background rectangle for better text visibility
        overlay = frame.copy()
        cv2.rectangle(overlay, (x, y - 80), (x + w, y), color, -1)
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
        
        # Draw text with enhanced styling
        font = cv2.FONT_HERSHEY_DUPLEX
        font_scale = 0.6
        thickness = 2
        
        # Display emotions
        cv2.putText(frame, emotions_display, (x + 5, y - 60), font, font_scale, (255, 255, 255), thickness)
        
        # Display age and gender
        info_text = f"Age: {face_data.age}"
        info_gender = f"Gender: {face_data.gender}"
        cv2.putText(frame, info_text, (x + 5, y - 35), font, font_scale, (255, 255, 255), thickness)
        cv2.putText(frame, info_gender, (x + 5, y - 10), font, font_scale, (255, 255, 255), thickness)

    def process_frame(self) -> Optional[np.ndarray]:
        success, frame = self.cap.read()
        if not success:
            return None
            
        frame = cv2.flip(frame, 1)
        detected = self.detector.detect_emotions(frame)
        
        if not detected:
            return frame
            
        for face in detected:
            age, gender = self.get_age_gender(frame)
            face_data = FaceData(
                box=face['box'],
                emotions=face['emotions'],
                age=age,
                gender=gender
            )
            
            categorized_emotions = EmotionClassifier.categorize_emotions(face_data.emotions)
            display_emotions = ', '.join([key for key, value in categorized_emotions.items() if value])
            
            self.draw_face_info(frame, face_data, display_emotions)
            
            # Handle speech feedback
            if display_emotions != self.last_emotion and time.time() - self.last_time > 2:
                compliment = ', '.join([random.choice(self.compliments[key]) 
                                      for key, value in categorized_emotions.items() if value])
                self.speech_engine.say(compliment)
                self.last_emotion = display_emotions
                self.last_time = time.time()
                
        return frame

    def run(self):
        cv2.namedWindow('Smart Mirror', cv2.WINDOW_NORMAL)
        
        while self.running and self.cap.isOpened():
            frame = self.process_frame()
            if frame is None:
                break
                
            cv2.imshow('Smart Mirror', frame)
            
            # Handle keyboard interactions
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):  # Quit
                break
            elif key == ord('s'):  # Toggle speech
                self.speech_engine.say("Speech toggled")
            elif key == ord('h'):  # Help
                help_text = "Controls: Q - Quit, S - Toggle Speech, H - Help"
                self.speech_engine.say(help_text)

        self.cleanup()

    def cleanup(self):
        self.speech_engine.stop()
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    mirror = SmartMirror()
    try:
        mirror.run()
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
        mirror.cleanup()