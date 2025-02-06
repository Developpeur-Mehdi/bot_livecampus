import os
import asyncio
import discord
from collections import deque
from bot import tts_queue  # On garde la file d'attente par serveur

# 📌 Chemin du fichier MP3 pour la notification
NOTIFICATION_SOUND = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "ressource", "notification", "notification.mp3"))

async def play_notification_sound(bot, guild, target_voice_channel):
    """Joue une notification sonore dans un salon vocal spécifique."""
    
    if not os.path.exists(NOTIFICATION_SOUND):
        print(f"❌ ERREUR: Le fichier {NOTIFICATION_SOUND} n'existe pas !")
        return

    # Vérifie si le bot est connecté au canal vocal du serveur
    vc = discord.utils.get(bot.voice_clients, guild=guild)

    # 📌 Si le bot n'est pas connecté, il rejoint le bon canal
    if vc is None or not vc.is_connected():
        vc = await target_voice_channel.connect()
    elif vc.channel.id != target_voice_channel.id:
        await vc.move_to(target_voice_channel)  # 🔄 Déplace le bot dans le bon canal

    # 📌 Lecture des sons de la file d'attente
    while tts_queue[guild.id]:
        message = tts_queue[guild.id].popleft()  # Récupère le message
        print(f"🔊 Lecture de la notification pour {guild.name}: {message}")


        # 📌 Joue le son de notification
        vc.play(discord.FFmpegPCMAudio(NOTIFICATION_SOUND))

        while vc.is_playing():
            await asyncio.sleep(1)  # Attendre la fin de la lecture

    # 📌 Déconnexion après 10 secondes si plus personne dans le canal
    await asyncio.sleep(10)
    if len(vc.channel.members) == 1:  # Vérifie si seul le bot est dans le canal
        await vc.disconnect()
