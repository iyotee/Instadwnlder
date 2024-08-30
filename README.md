# Instagram Video Downloader

Ce script Python vous permet de télécharger des vidéos depuis Instagram en meilleure qualité possible. Il utilise `Instaloader` pour gérer le téléchargement et prend également en charge l'authentification pour les comptes privés. Le script stocke en toute sécurité vos informations d'identification Instagram après la première connexion réussie pour une utilisation future.

## Fonctionnalités

- **Téléchargement de vidéos Instagram** : Il vous suffit de fournir le lien de la vidéo Instagram ou du profil instagram et le script téléchargera toute les vidéo du profil ou la vidéo de l'URL fournie.
- **Prend en charge les comptes privés** : Authentifiez-vous avec vos informations d'identification Instagram pour télécharger des vidéos depuis des comptes privés.
- **Stockage sécurisé des informations d'identification** : Les informations d'identification sont chiffrées et stockées localement après la première connexion réussie.
- **Installation automatique des dépendances** : Le script vérifie et installe automatiquement les packages Python manquants.

## Prérequis

- Python 3.6+
- Pip (installateur de packages Python)

## Installation

1. **Clonez le dépôt** :

   ```bash
   git clone https://github.com/iyotee/Instadwnlder.git
   cd Instadwnlder   
2. **Configurez un environnement virtuel (optionnel mais recommandé)** : 

   ```bash
    python3 -m venv venv
    source venv/bin/activate
3. **Installer les dépendances** :
   ```bash
   pip install instaloader cryptography

4. **Exécutez le script. Il vérifiera automatiquement les dépendances manquantes et les installera** : 

   ```bash
   python3 main.py
##  Utilisation
1. Lorsque vous exécutez le script pour la première fois, il vous demandera de saisir votre nom d'utilisateur et mot de passe Instagram. Ces informations seront vérifiées avant d'être stockées de manière sécurisée.

2. Après une connexion réussie, vous serez invité à entrer l'URL de la vidéo Instagram que vous souhaitez télécharger.

3. La vidéo sera téléchargée dans le répertoire nommé d'après l'utilisateur Instagram qui a publié la vidéo.  
   ```bash
   Entrez votre nom utilisateur Instagram: votre_nom_utilisateur
   Entrez votre mot de passe Instagram: ********
   Entrez le lien de la vidéo Instagram: https://www.instagram.com/p/XXXXXXXXXX/  

## Sécurité
Vos informations d'identification Instagram sont chiffrées à l'aide de la bibliothèque cryptography avant d'être stockées localement. La clé de chiffrement est générée et stockée de manière sécurisée.
Le script ne partage ni n'envoie vos informations d'identification ailleurs ; elles sont utilisées uniquement localement sur votre machine pour authentifier avec Instagram.

## Dépannage
Problèmes de connexion : Assurez-vous d'avoir une connexion Internet stable. Si vous rencontrez des erreurs d'authentification, vérifiez vos informations d'identification et réessayez.
Dépendances non installées : Assurez-vous que pip est installé et correctement configuré.

## Contribution
N'hésitez pas à forker ce dépôt, créer des problèmes, ou soumettre des pull requests. Les contributions sont les bienvenues !

## Licence
Ce projet est sous la licence MIT - voir le fichier LICENSE pour les détails.



