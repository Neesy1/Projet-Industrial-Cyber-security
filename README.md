**Industrial Cyber Security Project - Siemens S7-1200 Analysis**
Ce projet est un outil de test d'intrusion et d'audit de sécurité dédié aux environnements industriels, spécifiquement ciblé sur les automates Siemens S7-1200. Il regroupe des outils de reconnaissance, d'attaque par force brute sur interface web et de manipulation de processus via Replay Attack (S7Comm).

[!WARNING]
Avertissement Légal : Cet outil est destiné à un usage éducatif et professionnel dans le cadre de tests d'intrusion autorisés uniquement. L'utilisation de ces scripts sur des infrastructures critiques sans autorisation est illégale et dangereuse.

🛠️ Fonctionnalités
Le projet est structuré autour d'un script principal (script.py) qui sert d'interface pour les modules suivants :

1. Reconnaissance & Scan (scan.py)
Utilise python-nmap pour identifier les automates sur le réseau.

Détection intelligente : Identifie les ports spécifiques (80/443 pour le portail web, 102 pour S7Comm).

Fingerprinting : Tente de récupérer les versions des services pour identifier le matériel.

2. Brute Force Web (BF.py)
Cible l'interface d'administration web des automates Siemens.

Simulation de headers macOS pour éviter certains filtrages basiques.

Gestion des redirections HTTP (Code 302) pour valider le succès de l'authentification.

Temporisation (time.sleep) pour éviter le déni de service (DoS) sur le CPU de l'automate.

3. Replay Attack S7Comm (Replay.py)
Injecte des trames binaires directement dans le protocole S7.

Handshake COTP/S7 : Initialise la communication avec l'automate.

Write Request : Envoie des commandes spécifiques pour forcer l'état d'une sortie (ex: Allumer/Éteindre un moteur).

Note : Les trames hexadécimales sont pré-configurées pour un environnement spécifique.


📂 Structure du Dépôt

script.py : Le lanceur central (Dashboard).
scan.py : Module de scan réseau interactif.
BF.py : Script de force brute pour le portail web Siemens.
Replay.py : Script d'injection de trames S7Comm.
.gitignore : Liste des fichiers à exclure (ex: mes_passwords.txt, __pycache__).


**🚀 Installation & Utilisation**

Prérequis
Python 3.x

Nmap installé sur le système

Dépendances Python :

Bash
  pip install python-nmap requests urllib3 tabulate tqdm
Lancement
Clonez le dépôt :

Bash
git clone https://github.com/Neesy1/Projet-Industrial-Cyber-security.git
Modifiez la variable DOSSIER_PROJET dans script.py pour correspondre à votre chemin local.

Lancez l'outil :

Bash
python3 script.py

**🛡️ Mesures de Remédiation (Bonnes Pratiques)**
Pour se protéger contre ces types d'attaques sur un S7-1200 :

Désactiver le serveur Web s'il n'est pas nécessaire.

Activer la protection par mot de passe en lecture/écriture dans TIA Portal.

Utiliser des ACLs pour limiter les communications sur le port 102 aux seules adresses IP de l'ingénierie/SCADA.

Passer à des protocoles sécurisés comme S7Comm-Plus avec TLS si le matériel le permet.

Quelques conseils pour ton dépôt :
Le fichier .gitignore : Assure-toi qu'il contient bien mes_passwords.txt pour ne pas envoyer tes listes de mots de passe par erreur sur GitHub.

Le chemin DOSSIER_PROJET : Dans ton script.py, tu as mis un chemin absolu (/home/sylvain/...). C'est pratique pour toi, mais ça ne marchera pas chez les autres. Tu pourrais le remplacer par :

**Python**

  DOSSIER_PROJET = os.path.dirname(os.path.abspath(__file__))
Cela rendra ton projet portable !
