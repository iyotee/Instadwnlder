import subprocess
import sys
import pkg_resources
import instaloader
import re
import getpass
import os
from cryptography.fernet import Fernet

# Liste des dépendances nécessaires
required = {'instaloader', 'cryptography'}

def install_missing_packages():
    """
    Vérifie si les packages requis sont installés. Si ce n'est pas le cas, les installe.
    """
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed

    if missing:
        print(f"Installation des packages manquants : {', '.join(missing)}")
        python = sys.executable
        subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)

# Appel de la fonction pour installer les dépendances manquantes
install_missing_packages()

# Chemin du fichier pour stocker les informations d'identification chiffrées
CREDENTIALS_FILE = 'credentials.dat'
# Clé de chiffrement (générée une seule fois et utilisée ensuite)
KEY_FILE = 'secret.key'

def generate_key():
    """
    Génère et stocke une clé de chiffrement.
    """
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as key_file:
        key_file.write(key)

def load_key():
    """
    Charge la clé de chiffrement depuis le fichier.
    """
    return open(KEY_FILE, 'rb').read()

def encrypt_message(message):
    """
    Chiffre un message (texte) avec la clé.
    """
    key = load_key()
    f = Fernet(key)
    return f.encrypt(message.encode())

def decrypt_message(encrypted_message):
    """
    Déchiffre un message chiffré avec la clé.
    """
    key = load_key()
    f = Fernet(key)
    return f.decrypt(encrypted_message).decode()

def save_credentials(username, password):
    """
    Sauvegarde les informations d'identification chiffrées dans un fichier.
    """
    encrypted_username = encrypt_message(username)
    encrypted_password = encrypt_message(password)

    with open(CREDENTIALS_FILE, 'wb') as cred_file:
        cred_file.write(encrypted_username + b'\n' + encrypted_password)

def load_credentials():
    """
    Charge et déchiffre les informations d'identification depuis un fichier.
    """
    if not os.path.exists(CREDENTIALS_FILE):
        return None, None

    with open(CREDENTIALS_FILE, 'rb') as cred_file:
        encrypted_username, encrypted_password = cred_file.read().split(b'\n')

    username = decrypt_message(encrypted_username)
    password = decrypt_message(encrypted_password)

    return username, password

def is_valid_instagram_url(url):
    """
    Vérifie si l'URL fournie est une URL Instagram valide pour un post ou un profil.
    """
    post_regex = re.compile(r'^(https?://)?(www\.)?instagram\.com/p/([A-Za-z0-9-_]+)/?$')
    profile_regex = re.compile(r'^(https?://)?(www\.)?instagram\.com/([^/]+)/?$')
    return re.match(post_regex, url) is not None or re.match(profile_regex, url) is not None

def verify_credentials(loader, username, password):
    """
    Vérifie les informations d'identification en tentant de se connecter.
    """
    try:
        loader.login(username, password)
        print("Connexion réussie.")
        return True
    except instaloader.exceptions.BadCredentialsException:
        print("Nom d'utilisateur ou mot de passe incorrect.")
        return False
    except instaloader.exceptions.ConnectionException as e:
        print(f"Erreur de connexion : {e}")
        return False
    except instaloader.exceptions.TwoFactorAuthRequiredException:
        print("Authentification à deux facteurs requise. Ce script ne gère pas encore cette fonctionnalité.")
        return False

def download_instagram_video(video_url, username, password):
    """
    Télécharge une vidéo Instagram en fonction de l'URL fournie.
    Authentification requise pour les comptes privés.
    """
    loader = instaloader.Instaloader(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

    if not verify_credentials(loader, username, password):
        return

    if 'instagram.com/p/' in video_url:
        # Télécharger une seule vidéo
        shortcode = video_url.split("/")[-2]
        try:
            post = instaloader.Post.from_shortcode(loader.context, shortcode)
            if post.is_video:
                loader.download_post(post, target=post.owner_username)
                print(f"Vidéo téléchargée : {shortcode}")
            else:
                print("L'URL fournie n'est pas une vidéo.")
        except instaloader.exceptions.InstaloaderException as e:
            print(f"Erreur lors du téléchargement : {e}")
    
    elif 'instagram.com/' in video_url:
        # Télécharger toutes les vidéos du profil
        profile_name = video_url.split('/')[-2]
        try:
            profile = instaloader.Profile.from_username(loader.context, profile_name)
            print(f"Téléchargement des vidéos du profil {profile_name}...")
            for post in profile.get_posts():
                if post.is_video:
                    loader.download_post(post, target=f"{profile_name}_videos")
            print("Téléchargement terminé.")
        except instaloader.exceptions.InstaloaderException as e:
            print(f"Erreur lors du téléchargement : {e}")

if __name__ == "__main__":
    # Générer la clé si elle n'existe pas encore
    if not os.path.exists(KEY_FILE):
        generate_key()

    # Charger les informations d'identification si elles existent
    username, password = load_credentials()

    # Si les informations d'identification ne sont pas trouvées, demander à l'utilisateur
    if not username or not password:
        while True:
            username = input("Entrez votre nom d'utilisateur Instagram: ").strip()
            password = getpass.getpass("Entrez votre mot de passe Instagram: ")

            # Vérifier les informations d'identification
            loader = instaloader.Instaloader(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
            if verify_credentials(loader, username, password):
                save_credentials(username, password)
                print("Informations d'identification enregistrées.")
                break
            else:
                print("Veuillez réessayer.")

    # Demander à l'utilisateur d'entrer le lien de la vidéo ou du profil Instagram
    while True:
        video_url = input("Entrez le lien de la vidéo ou du profil Instagram: ").strip()
        if is_valid_instagram_url(video_url):
            break
        else:
            print("URL invalide. Veuillez entrer une URL Instagram valide, par exemple : https://www.instagram.com/p/XXXXXXXXXX/ ou https://www.instagram.com/username/")

    # Lancer le téléchargement
    download_instagram_video(video_url, username, password)
