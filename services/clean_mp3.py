import os
import time
import config

def cleanup_old_audio_files(directory, max_age=60):
    """Supprime les fichiers audio de plus de 60 secondes."""
    now = time.time()
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath) and now - os.path.getmtime(filepath) > max_age:
            os.remove(filepath)
