# Discord Bot - TTS (Text-to-Speech) (Pour LiveCampus)

## Description

Ce bot Discord est conçu pour offrir une fonctionnalité de **Text-to-Speech (TTS)**. Lorsqu'un message est ajouté à la file d'attente, le bot génère un fichier audio à partir du texte et le lit dans un canal vocal du serveur Discord.
Le message ou les messages ajoutés découlent d'une commande **/lever_main**, qui récupère **l'id** de l'utilisateur et qui gènère donc ce message par exemple : **Jean à levé la main**. Un bouton pour baisser la main est également disponible,
lors de l'appel de cette commande. Si, je n'appuie pas sur ce bouton, relancer la commande **/lever_main** suffira pour la baisser. De plus, l'intervenant ou même les élèves ont une méthode **/voir_mains**, qui liste toutes les mains levées,
ou non.
J'ai également créé la commande **/deadline** qui sera utile lorsqu'un intervenant donnera un travail à rendre. L'utilisateur renseigne : 
- **la description du travail à rendre**
- **Le jour du rendu (choix jusqu'à 10 jours en comptant le jour actuel)**
- **L'heure du rendu (de minuit à 23h)**
L'avantage de cette commande c'est son autonomie, dès qu'elle est utilisée elle vérifié si le canal textuel **🚧┊𝖽𝖾𝖺𝖽𝗅𝗂𝗇𝖾** existe sur le serveur, si oui elle ajoute la deadline, dans le cas contraire elle crée ce canal.

Le bot prend en charge plusieurs serveurs Discord, chaque serveur ayant sa propre file d'attente TTS.

Le bot utilise la bibliothèque **gTTS** (Google Text-to-Speech) pour générer les fichiers audio et se connecte automatiquement aux canaux vocaux pour lire les messages.

---

## Fonctionnalités

- **Text-to-Speech** : Convertit les messages textuels en audio et les lit dans un canal vocal.
- **Multi-serveurs** : Gère une file d'attente TTS distincte pour chaque serveur Discord où le bot est présent.
- **Gestion automatique des connexions vocales** : Se connecte automatiquement aux canaux vocaux et se déconnecte lorsqu'il est seul.
- **Nettoyage des fichiers audio** : Supprime les fichiers audio générés après leur lecture pour libérer de l'espace.
- **/lever_main, /voir_mains et /deadline**

---

## Prérequis

Avant de lancer le bot, assure-toi d'avoir les éléments suivants installés :

Création d'un environnement virtuel en python à faire à la racine du dossier du bot
- **python3 -m venv venv** -> Dossier **venv** créé
- Activation de l'environnement virtuel : **source venv/bin/activate**
- Devant le début de la ligne du terminal il doit y avoir **(venv)**

- Python 3.8+  
- [Discord.py](https://discordpy.readthedocs.io/en/stable/) : Bibliothèque pour interagir avec l'API Discord.
- [gTTS](https://pypi.org/project/gTTS/) : Bibliothèque pour générer du texte en parole.
- [FFmpeg](https://ffmpeg.org/) : Outil nécessaire pour lire les fichiers audio dans Discord.
- [APSChduler](https://apscheduler.readthedocs.io/en/stable/) : Pour planifier des tâches asynchrones.

---
- Pour installé toutes les librairies directement, il faut récupérer le fichier **requirements.txt**
- **Vérifier** que l'environnement **virtuel** est activé et écrire **pip install -r requirements.txt**

Le faire manuellement :

- **pip install discord.py**
- **pip install gtts**
- **pip install python-dotenv**
- **pip install apscheduler**

- Pour installer **FFmpeg** faire : **sudo apt install ffmpeg**

- **Attention !!** Ne pas oublier de créer le fichier **.env** et d'y mettre le **token** du bot de cette façon : **DISCORD_TOKEN = "TOKEN_BOT"**

## Installation

1. Clone ce repository :
   ```bash
   git clone https://github.com/ton-utilisateur/nom-du-bot.git
