import discord
from discord import app_commands
from discord.ext import commands
from collections import deque

from bot import tts_queue
from services.tts_service import play_notification_sound

hands_raised = {}  # Dictionnaire pour suivre les mains levées

class LeverMainView(discord.ui.View):
    def __init__(self, user_id, guild_id):
        super().__init__(timeout=None)
        self.user_id = user_id
        self.guild_id = guild_id

    @discord.ui.button(label="Baisser la main", style=discord.ButtonStyle.red)
    async def baisser_main(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Permet à l'utilisateur de baisser sa main."""
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ Ce bouton n'est pas pour toi.", ephemeral=True)
            return

        if self.guild_id in hands_raised and self.user_id in hands_raised[self.guild_id]:
            hands_raised[self.guild_id].remove(self.user_id)
            await interaction.response.edit_message(content=f"✋ {interaction.user.mention} a baissé sa main.", view=None)
        else:
            await interaction.response.send_message("❌ Tu n'avais pas levé la main, ou elle a été baissée.", ephemeral=True)


class LeverMain(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="lever_main", description="Levez la main dans un canal vocal.")
    async def lever_main(self, interaction: discord.Interaction):
        """Commande pour lever la main dans un canal vocal."""
        await interaction.response.defer(thinking=True)

        guild = interaction.guild
        user = interaction.user

        # 📌 Vérifier si l'utilisateur est bien en vocal
        if not user.voice or not user.voice.channel:
            await interaction.followup.send("❌ Tu dois être dans un canal vocal.", ephemeral=True)
            return

        voice_channel = user.voice.channel  # Canal vocal de l'utilisateur

        # 📌 Récupérer le salon textuel lié au canal vocal
        text_channel = discord.utils.get(guild.text_channels, name=voice_channel.name)

        # 📌 Si aucun canal textuel trouvé, envoyer dans le canal par défaut
        # if text_channel is None:
        #     text_channel = guild.system_channel

        if guild.id not in hands_raised:
            hands_raised[guild.id] = set()

        # 📌 Si l'utilisateur a déjà levé la main
        if user.id in hands_raised[guild.id]:
            hands_raised[guild.id].remove(user.id)  # Retirer la main levée
            await interaction.followup.send("❌ Tu as déjà levé la main, elle a été baissée.", ephemeral=True)

            # 📌 Envoyer le message dans le salon textuel du vocal
            if text_channel:
                await text_channel.send(f"✋ {user.mention} a baissé sa main.")

            return

        # 📌 Ajouter l'utilisateur à la liste des mains levées
        hands_raised[guild.id].add(user.id)

        # 📌 Envoyer le message dans le chat textuel du canal vocal
        if text_channel:
            await text_channel.send(f"✋ {user.mention} a levé la main !")

        await interaction.followup.send(
            "✅ Ta main a été levée avec succès !",
            ephemeral=True,
            view=LeverMainView(user.id, guild.id)
        )

        # 📌 Ajouter un message dans la file d'attente de ce serveur
        if guild.id not in tts_queue:
            tts_queue[guild.id] = deque()

        tts_queue[guild.id].append(f"{user.display_name} a levé la main.")

        # ✅ Jouer la notification sonore
        await play_notification_sound(self.bot, guild, voice_channel)

    @app_commands.command(name="voir_mains", description="Voir qui a levé la main.")
    async def voir_mains(self, interaction: discord.Interaction):
        """Commande pour afficher les utilisateurs ayant levé la main."""
        guild_id = interaction.guild.id
        if guild_id not in hands_raised or not hands_raised[guild_id]:
            await interaction.response.send_message("🔹 Personne n'a levé la main.", ephemeral=False)
            return

        user_mentions = [f"<@{user_id}>" for user_id in hands_raised[guild_id]]
        message = "✋ **Utilisateurs ayant levé la main :**\n" + "\n".join(user_mentions)
        await interaction.response.send_message(message, ephemeral=False)


async def setup(bot):
    await bot.add_cog(LeverMain(bot))
    print("✅ Commandes de lever_main synchronisées.")
