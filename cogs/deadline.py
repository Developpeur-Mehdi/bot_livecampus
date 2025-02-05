import discord
from discord.ext import commands
from datetime import datetime, timedelta
import pytz

class Deadline(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="deadline", description="Sélectionnez une deadline avec un menu interactif.")
    async def deadline(self, interaction: discord.Interaction):
        # Crée la vue pour sélectionner la date et l'heure
        view = DeadlineView(interaction.user, interaction.guild, interaction.client)
        await interaction.response.send_message("📅 Sélectionnez la date et l'heure de votre deadline :", view=view, ephemeral=True)

class DateSelect(discord.ui.Select):
    def __init__(self):
        # 10 prochains jours
        options = [
            discord.SelectOption(label=(datetime.now() + timedelta(days=i)).strftime("%d %B %Y"), value=str(i))
            for i in range(10)
        ]
        super().__init__(placeholder="📅 Sélectionnez une date", options=options)

    async def callback(self, interaction: discord.Interaction):
        # Met à jour la date sélectionnée dans la vue
        view: DeadlineView = self.view
        view.selected_date = datetime.now() + timedelta(days=int(self.values[0]))
        await interaction.response.defer()  # Défère la réponse pour éviter un temps d'attente trop long

class DescriptionInput(discord.ui.Modal, title="Ajoutez une description"):
    description = discord.ui.TextInput(label="Description de la deadline", style=discord.TextStyle.long, required=True)

    def __init__(self, view: "DeadlineView"):
        super().__init__()
        self.view = view  # On passe la vue pour y enregistrer la description

    async def on_submit(self, interaction: discord.Interaction):
        # Sauvegarde la description dans la vue
        self.view.description = self.description.value
        await interaction.response.send_message(f"✅ Description ajoutée : **{self.description.value}**", ephemeral=True)

class HourSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label=f"{h:02d}:00", value=str(h)) for h in range(24)
        ]
        super().__init__(placeholder="⏰ Sélectionnez une heure", options=options)

    async def callback(self, interaction: discord.Interaction):
        # Met à jour l'heure sélectionnée dans la vue
        view: DeadlineView = self.view
        view.selected_hour = int(self.values[0])
        await interaction.response.defer()

class DeadlineView(discord.ui.View):
    def __init__(self, user: discord.User, guild: discord.Guild, bot: discord.Client):
        super().__init__(timeout=60)  # 60 secondes pour choisir
        self.user = user
        self.guild = guild
        self.bot = bot  # Ajout du bot pour récupérer l'icône
        self.selected_date = None
        self.selected_hour = None
        self.description = None
        self.add_item(DateSelect())  # Ajouter le menu de sélection de la date
        self.add_item(HourSelect())  # Ajouter le menu de sélection de l'heure

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user == self.user  # Limiter l'interaction à l'utilisateur ayant initié la commande

    @discord.ui.button(label="📝 Ajouter une description", style=discord.ButtonStyle.blurple)
    async def add_description(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Ouvrir un modal pour ajouter la description
        await interaction.response.send_modal(DescriptionInput(self))

    @discord.ui.button(label="✅ Valider", style=discord.ButtonStyle.green)
    async def validate(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Vérification des choix avant de valider la deadline
        if not self.selected_date or self.selected_hour is None:
            await interaction.response.send_message("❌ Veuillez sélectionner une date et une heure.", ephemeral=True)
            return

        if not self.description:
            await interaction.response.send_message("❌ Veuillez ajouter une description avant de valider.", ephemeral=True)
            return

        # Conversion en heure de Paris
        paris_tz = pytz.timezone("Europe/Paris")
        deadline_datetime = self.selected_date.replace(hour=self.selected_hour, minute=0, second=0, microsecond=0)
        deadline_datetime = paris_tz.localize(deadline_datetime)

        now = datetime.now(paris_tz)
        if deadline_datetime < now:
            await interaction.response.send_message("❌ La date choisie est déjà passée !", ephemeral=True)
            return

        # Chercher ou créer le canal "🚧┊𝖽𝖾𝖺𝖽𝗅𝗂𝗇𝖾"
        deadline_channel = discord.utils.get(self.guild.text_channels, name="🚧┊𝖽𝖾𝖺𝖽𝗅𝗂𝗇𝖾")
        if deadline_channel is None:
            # Création du canal si inexistant
            deadline_channel = await self.guild.create_text_channel(name="🚧┊𝖽𝖾𝖺𝖽𝗅𝗂𝗇𝖾")
            await interaction.response.send_message(f"🔨 Canal créé : {deadline_channel.mention}", ephemeral=True)

        # Récupération de l'icône du bot
        bot_icon_url = self.bot.user.avatar.url if self.bot.user.avatar else self.bot.user.default_avatar.url

        # Création de l'embed
        embed = discord.Embed(
            title="📅 Nouvelle Deadline !",
            description=f"📝 **{self.description}**",
            color=discord.Color.red(),
            timestamp=now  # Date et heure de création
        )

        # Ajout des champs
        embed.add_field(name="📆 Date", value=f"**{deadline_datetime.strftime('%d %B %Y à %H:%M')}**", inline=False)
        embed.add_field(name="👤 Ajouté par", value=self.user.mention, inline=True)

        # Footer avec l'icône du bot
        embed.set_footer(text="LiveCampus Bot", icon_url=bot_icon_url)

        # Envoi de l'embed dans le canal
        await deadline_channel.send(embed=embed)

        # Utiliser `followup` pour envoyer un message supplémentaire
        await interaction.followup.send(f"✅ Deadline enregistrée et envoyée dans {deadline_channel.mention} !", ephemeral=True)


# Enregistrement du cog
async def setup(bot):
    await bot.add_cog(Deadline(bot))
    # await bot.tree.sync()  # Synchronisation après l'ajout du cog
    print("✅ Commandes de Deadline synchronisées.")

