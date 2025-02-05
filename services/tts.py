import os
import time
from gtts import gTTS
from collections import deque

AUDIO_DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "audio_files"))

def generate_tts(text: str) -> str:
    """Génère un fichier audio TTS à partir du texte."""
    
    # ✅ Vérifie si le dossier existe, sinon le crée
    if not os.path.exists(AUDIO_DIRECTORY):
        os.makedirs(AUDIO_DIRECTORY)

    filename = os.path.join(AUDIO_DIRECTORY, f"tts_{int(time.time())}.mp3")
    
    tts = gTTS(text, lang="fr")
    tts.save(filename)  # Sauvegarde dans le bon dossier
    
    return filename  # Retourne le chemin absolu du fichier généré


def cleanup_old_audio_files(directory: str):
    """Nettoie les anciens fichiers audio après lecture."""
    if not os.path.exists(directory):
        os.makedirs(directory)  # Crée le dossier s'il n'existe pas
        return

    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"❌ Impossible de supprimer {file_path} : {e}")