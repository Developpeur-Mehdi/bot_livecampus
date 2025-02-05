import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")  # Récupérer le token depuis un fichier .env

