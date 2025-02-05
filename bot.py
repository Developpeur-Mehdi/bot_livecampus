import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
import time
import os
from collections import defaultdict, deque


tts_queue = defaultdict(deque)  # ✅ Chaque serveur aura sa propre file d'attente


class MyBot(commands.Bot):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(command_prefix="/", intents=intents)

        self.scheduler = AsyncIOScheduler()
        self.voice_connections = {}  # Stocke les connexions vocales par serveur
        
        

    async def setup_hook(self):
        print("🔧 Setup hook exécuté.")
        try:
            # Synchronisation locale pour chaque serveur où le bot est présent
            for guild in self.guilds:
                try:
                    await self.tree.sync(guild=guild)
                    print(f"✅ Commandes synchronisées localement sur {guild.id}.")
                except Exception as e:
                    print(f"❌ Erreur lors de la synchronisation locale sur {guild.id} : {e}")
        except Exception as e:
            print(f"❌ Erreur lors de la synchronisation locale : {e}")



    async def on_ready(self):
        print(f"✅ Bot connecté en tant que {self.user}")
        
        try:
            for guild in self.guilds:  # Itère sur tous les serveurs où le bot est présent
                try:
                    await self.load_extension("cogs.deadline")  # Charge le cog "Deadline"
                    await self.load_extension("cogs.hands")  # Charge le cog "Hands"

                    # Synchronisation locale pour chaque serveur
                    await self.tree.sync(guild=guild)

                    print(f"✅ Commandes synchronisées localement sur {guild.id}.")
                except Exception as e:
                    print(f"❌ Erreur lors de la synchronisation locale sur {guild.id} : {e}")
        
            
        except Exception as e:
            print(f"❌ Erreur lors de la synchronisation locale : {e}")



        
    async def on_member_join(self, member: discord.Member):
        """Envoie un message de bienvenue personnalisé pour un professeur qui rejoint le serveur."""
        guild = member.guild
        
        # Message de bienvenue personnalisé pour un professeur
        welcome_message = (
            f"👋 **Bienvenue, {member.mention} !**\n\n"
            f"Nous sommes ravis de vous accueillir dans le serveur d'études **{guild.name}**.\n\n"
            f"Ce serveur a pour objectif de faciliter les échanges et la collaboration entre les membres.\n"
            f"Quelques points importants pour bien commencer :\n"
            f"- Consultez les **canaux de discussion** pour échanger avec les étudiants.\n"
            f"- Si vous avez des questions ou des besoins particuliers, n'hésitez pas à contacter l'équipe administrative. 📚\n"
            f"- Nous vous remercions de contribuer à la communauté d'enseignement !"
        )

        # Envoie le message dans le canal #général ou un autre canal spécifique
        channel = discord.utils.get(guild.text_channels, name='général')  # Change le nom du canal si nécessaire
        if channel:
            await channel.send(welcome_message)


    async def on_voice_state_update(self, member, before, after):
        """Gère les connexions/déconnexions vocales du bot."""
        if not member.bot:
            await self.handle_voice_update(member, before, after)

    async def handle_voice_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        guild = member.guild
        voice_channel = after.channel if after.channel else before.channel

        if not voice_channel:
            return

        # Vérifie si le bot est déjà connecté à un canal vocal
        if guild.id in self.voice_connections:
            vc = self.voice_connections[guild.id]

            # Déconnecte si le bot est seul
            if len(vc.channel.members) == 1:
                await vc.disconnect()
                del self.voice_connections[guild.id]

        # Connecte le bot uniquement si besoin
        if after.channel and (not before.channel or before.channel.id != after.channel.id):
            if guild.id not in self.voice_connections or not self.voice_connections[guild.id].is_connected():
                self.voice_connections[guild.id] = await voice_channel.connect()
                print(f"🔊 Connecté à {voice_channel.name} sur {guild.name}")


    async def connect_to_voice(self, guild: discord.Guild, voice_channel: discord.VoiceChannel):
        """Connecte le bot à un canal vocal si nécessaire."""
        if guild.id in self.voice_connections and self.voice_connections[guild.id].is_connected():
            return

        try:
            vc = await voice_channel.connect()
            self.voice_connections[guild.id] = vc
            print(f"🔊 Connecté à {voice_channel.name} sur {guild.name}")
        except discord.ClientException:
            print(f"⚠ Impossible de se connecter à {voice_channel.name} sur {guild.name}")

    async def disconnect_from_voice(self, guild: discord.Guild):
        """Déconnecte le bot si le canal est vide."""
        if guild.id not in self.voice_connections:
            return

        vc = self.voice_connections[guild.id]
        await asyncio.sleep(10)

        if vc.is_connected() and len(vc.channel.members) == 1:
            await vc.disconnect()
            del self.voice_connections[guild.id]
            print(f"🔌 Déconnecté du canal vocal sur {guild.name}")