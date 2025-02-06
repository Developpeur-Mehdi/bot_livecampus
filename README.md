# Discord Bot - Notification Main(s) Levée(s)(Pour LiveCampus)

## Description

Ce bot Discord est conçu pour offrir une fonctionnalité de **Notification** via **FFmpeg**. Lorsqu'un message est ajouté à la file d'attente, le bot **lit le fichier .mp3** le joue dans un canal vocal du serveur Discord.
Un bouton pour baisser la main est également disponible lors de la commande **/lever_main**
lors de l'appel de cette commande. Si, je n'appuie pas sur ce bouton, relancer la commande **/lever_main** suffira pour la baisser. De plus, l'intervenant ou même les élèves ont une méthode **/voir_mains**, qui liste toutes les mains levées,
ou non.
J'ai également créé la commande **/deadline** qui sera utile lorsqu'un intervenant donnera un travail à rendre. L'utilisateur renseigne : 
- **la description du travail à rendre**
- **Le jour du rendu (choix jusqu'à 10 jours en comptant le jour actuel)**
- **L'heure du rendu (de minuit à 23h)**
L'avantage de cette commande c'est son autonomie, dès qu'elle est utilisée elle vérifie si le canal textuel **🚧┊𝖽𝖾𝖺𝖽𝗅𝗂𝗇𝖾** existe sur le serveur, si oui elle ajoute la deadline, dans le cas contraire elle crée ce canal.

Le bot prend en charge plusieurs serveurs Discord, chaque serveur ayant sa propre file d'attente TTS.

---

## Fonctionnalités

- **Notification via .mp3** : Convertit les messages textuels en audio et les lit dans un canal vocal.
- **Multi-serveurs** : Gère une file d'attente TTS distincte pour chaque serveur Discord où le bot est présent.
- **Gestion automatique des connexions vocales** : Se connecte automatiquement aux canaux vocaux et se déconnecte lorsqu'il est seul.
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
- [FFmpeg](https://ffmpeg.org/) : Outil nécessaire pour lire les fichiers audio dans Discord.
- [APSChduler](https://apscheduler.readthedocs.io/en/stable/) : Pour planifier des tâches asynchrones.

---
- Pour installé toutes les librairies directement, il faut récupérer le fichier **requirements.txt**
- **Vérifier** que l'environnement **virtuel** est activé et écrire **pip install -r requirements.txt**

Le faire manuellement :

- **pip install discord.py**
- **pip install python-dotenv**
- **pip install apscheduler**

- Pour installer **FFmpeg** faire : **sudo apt install ffmpeg**

- **Attention !!** Ne pas oublier de créer le fichier **.env** et d'y mettre le **token** du bot de cette façon : **DISCORD_TOKEN = "TOKEN_BOT"**

## Installation

1. Clone ce repository :
   ```bash
   git clone https://github.com/Developpeur-Mehdi/bot_livecampus.git
