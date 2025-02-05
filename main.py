import discord
from bot import MyBot
import config

# Initialisation des intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.voice_states = True

client = MyBot(intents=intents)

if __name__ == "__main__":
    client.run(config.TOKEN)
