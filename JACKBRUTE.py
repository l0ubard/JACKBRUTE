import pyfiglet
from colorama import init, Fore, Back, Style
import os
from telethon import TelegramClient, sync, errors
from telethon.tl.types import PeerChannel, PeerUser, ChannelParticipantsRecent
from telethon.tl.functions.channels import InviteToChannelRequest, LeaveChannelRequest, GetFullChannelRequest
from telethon.tl.functions.messages import SendMessageRequest, GetHistoryRequest, ForwardMessagesRequest, GetDialogsRequest
from telethon.tl.types import InputPeerChat
from telethon.tl.types import InputPeerChannel
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import InputFile
from telethon.errors import SessionPasswordNeededError, PeerFloodError, UserPrivacyRestrictedError, FloodWaitError

from telethon.tl.functions.account import UpdateProfileRequest
import random
import csv
import time
import random
import asyncio
from tqdm import tqdm

# Initialisation des couleurs
init()

# Couleurs pour le texte
rose = Fore.MAGENTA
cyan = Fore.CYAN
reset = Fore.RESET

# Variables globales
dossier_sessions = "sessions"
fichier_comptes = "accounts.csv"
fichier_membres = "membres.csv"  # Fichier pour stocker les membres extraits
api_file_path = os.path.join(dossier_sessions, 'API.csv')


# Fonction pour afficher l'en-tête
def afficher_entete():
    titre = pyfiglet.figlet_format("JACK BRUTE", font="slant")
    print(f"{rose}{titre}{reset}")
    print(f"{cyan}    ÉDITION AZDINE{reset}")
    print()
    print(f"{cyan}    CANAL TG : @JACKBRUTE   |   SUPPORT TG : @JACKBRUTE{reset}")
    print(f"{cyan}    Version : 0.23{reset}")
    print("-" * 60)

# Fonction pour afficher le menu principal
def afficher_menu():

    print(f"\n{cyan}•-----• MENU DE CONNEXION •-----•{reset}")
    print(f"    [1] Connecter des comptes (Telethon/Tdata)")
    print(f"    [2] Déconnecter des comptes")
    print(f"    [3] Lister toutes les sessions")
    print(f"    [4] Checker de spam")
    print(f"    [5] Checker de bannissement")

    print(f"\n{cyan}•-----• MENU D'ÉDITION •-----•{reset}")
    print(f"    [6] Modifier le prénom                -       [9] Modifier le nom de famille")
    print(f"    [7] Modifier le nom d'utilisateur     -       [10] Modifier la biographie")
    print(f"    [8] Modifier la photo de profil")

    print(f"\n{cyan}•-----• MENU DE SCRAPER •-----•{reset}")
    print(f"    [11] Extraire des membres d'un groupe/canal avec options")

    print(f"\n{cyan}•-----• MENU D'AJOUT •-----•{reset}")
    print(f"    [18] Ajouter des membres à votre groupe/canal à partir d'un fichier CSV")

    print(f"\n{cyan}•-----• MENU DES MESSAGES •-----•{reset}")
    print(f"    [19] Envoyer des messages en masse")

    print(f"\n{cyan}•-----• MENU D'ADHÉSION / DÉPART •-----•{reset}")
    print(f"    [27] Rejoindre des groupes/canaux")
    print(f"    [28] Quitter des groupes/canaux")

    print(f"\n{cyan}•-----• MENU DES VUES / RÉACTIONS / SONDAGES •-----•{reset}")
    print(f"    [30] Augmenter les vues des publications avec comptes")

    print(f"\n•-----• JACK-BRUTE •-----•\n")
    print("Choisissez une option : ")

# Fonction pour enregistrer les informations dans le fichier CSV
def enregistrer_informations_api(telephone, api_id, api_hash):
    if not os.path.exists(dossier_sessions):
        os.makedirs(dossier_sessions)  # Crée le dossier sessions s'il n'existe pas

    fichier_existe = os.path.isfile(api_file_path)

    with open(api_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not fichier_existe:
            writer.writerow(['telephone', 'api_id', 'api_hash'])  # Écrire l'en-tête si le fichier est nouveau
        writer.writerow([telephone, api_id, api_hash])

# Fonction pour connecter des comptes (sans exécution automatique)
def connecter_comptes():
    api_id = input("Entrez votre ID API : ")
    api_hash = input("Entrez votre Hash API : ")
    telephone = input("Entrez votre numéro de téléphone : ")
    proxy = input("Voulez-vous utiliser un proxy ? (o/n) : ")

    if proxy.lower() == 'o':
        adresse_proxy = input("Entrez l'adresse du proxy : ")
        port_proxy = int(input("Entrez le port du proxy : "))
        client = TelegramClient(f"{dossier_sessions}/{telephone}", api_id, api_hash,
                                proxy=(adresse_proxy, port_proxy))
    else:
        client = TelegramClient(f"{dossier_sessions}/{telephone}", api_id, api_hash)

    try:
        client.start()
        print(f"Connecté au compte : {telephone}")
        # Enregistrer les informations dans le fichier CSV
        enregistrer_informations_api(telephone, api_id, api_hash)
        print("Informations API enregistrées avec succès.")
    except errors.SessionPasswordNeeded:
        mot_de_passe = input("Entrez votre mot de passe : ")
        client.start(phone=telephone, password=mot_de_passe)
        # Enregistrer les informations dans le fichier CSV après la connexion réussie
        enregistrer_informations_api(telephone, api_id, api_hash)
        print("Informations API enregistrées avec succès.")

# Fonction pour enregistrer les détails du compte
def enregistrer_compte(telephone):
    with open(fichier_comptes, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([telephone])

# Fonction pour lister toutes les sessions
def lister_sessions():
    if os.path.exists(fichier_comptes):
        with open(fichier_comptes, 'r') as f:
            comptes = csv.reader(f)
            print(f"\n{cyan}•-----• LISTE DES COMPTES •-----•{reset}")
            for row in comptes:
                print(f"    {row[0]}")
    else:
        print(f"{rose}Aucun compte trouvé.{reset}")

# Fonction pour déconnecter un compte
def deconnecter_compte():
    telephone = input("Entrez le numéro de téléphone du compte à déconnecter : ")
    if os.path.exists(fichier_comptes):
        with open(fichier_comptes, 'r') as f:
            comptes = list(csv.reader(f))
        comptes = [acc for acc in comptes if acc[0] != telephone]
        with open(fichier_comptes, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(comptes)
        print(f"{cyan}Compte {telephone} déconnecté.{reset}")
    else:
        print(f"{rose}Aucun compte trouvé.{reset}")

# Fonction pour vérifier le spam (exemple)
def verifier_spam():
    print(f"{cyan}Fonctionnalité de vérification de spam ici...{reset}")

# Fonction pour vérifier le bannissement (exemple)
def verifier_bannissement():
    print(f"{cyan}Fonctionnalité de vérification de bannissement ici...{reset}")


# Menu D'EDITION

async def choisir_session():
    """Lister les sessions disponibles dans le dossier et permettre à l'utilisateur de choisir une session."""
    sessions = [f for f in os.listdir(sessions_dir) if f.endswith('.session')]
    
    if not sessions:
        print("Aucune session trouvée.")
        return None

    print("Sessions disponibles :")
    for i, session in enumerate(sessions):
        print(f"{i + 1}: {session}")

    choice = input("Choisissez le numéro de la session : ")
    
    try:
        selected_session = sessions[int(choice) - 1]
        return selected_session
    except (IndexError, ValueError):
        print("Choix invalide.")
        return None

def get_api_info_from_csv(telephone):
    """Récupérer l'API ID et l'API Hash à partir du fichier API.csv en fonction du numéro de téléphone."""
    api_csv_path = os.path.join(sessions_dir, 'API.csv')

    with open(api_csv_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Numéro de téléphone'] == telephone:
                return row['API_ID'], row['API_HASH']
    return None, None

async def modifier_profil(update_request):
    """Modifier le profil avec une demande donnée."""
    session = await choisir_session()
    if not session:
        return

    # Extraire le numéro de téléphone à partir du nom de la session
    telephone = session.split('.')[0]
    api_id, api_hash = get_api_info_from_csv(telephone)

    if not api_id or not api_hash:
        print("Impossible de trouver les informations API pour ce compte.")
        return

    session_path = os.path.join(sessions_dir, session)

    try:
        async with TelegramClient(session_path, api_id, api_hash) as client:
            await client(update_request)
            print(f"Profil modifié pour {session}.")
    except Exception as e:
        print(f"Erreur lors de la connexion avec la session : {e}")

async def changer_prenom():
    """Modifier le prénom du compte."""
    new_first_name = input("Entrez le nouveau prénom : ")
    await modifier_profil(UpdateProfileRequest(first_name=new_first_name))
    await demander_autre_modification()

async def changer_nom_utilisateur():
    """Modifier le nom d'utilisateur du compte."""
    new_username = input("Entrez le nouveau nom d'utilisateur (sans @) : ")
    await modifier_profil(UpdateProfileRequest(username=new_username))
    await demander_autre_modification()

async def changer_photo_profil():
    """Modifier la photo de profil du compte."""
    photo_path = input("Entrez le chemin de la nouvelle photo : ")
    await modifier_profil(UpdateProfileRequest(photo=photo_path))
    await demander_autre_modification()

async def changer_nom_famille():
    """Modifier le nom de famille du compte."""
    new_last_name = input("Entrez le nouveau nom de famille : ")
    await modifier_profil(UpdateProfileRequest(last_name=new_last_name))
    await demander_autre_modification()

async def changer_bio():
    """Modifier la biographie du compte."""
    new_bio = input("Entrez la nouvelle biographie (max 70 caractères) : ")
    
    if len(new_bio) > 70:
        print("La biographie ne doit pas dépasser 70 caractères.")
        return

    await modifier_profil(UpdateProfileRequest(about=new_bio))
    await demander_autre_modification()

async def demander_autre_modification():
    """Demander à l'utilisateur s'il souhaite modifier un autre compte."""
    while True:
        reponse = input("Souhaitez-vous modifier un autre compte ? (o/n) : ").strip().lower()
        if reponse == 'o':
            # Rediriger vers le menu de choix de session
            return
        elif reponse == 'n':
            print("Retour au menu principal.")
            return
        else:
            print("Réponse invalide. Veuillez répondre par 'o' ou 'n'.")

from telethon import TelegramClient
import os
import csv

# Dossier contenant les sessions
sessions_dir = "sessions"

# Dossier pour les fichiers CSV
members_dir = "members"

# Dossier pour les fichiers Tdata
tdata_dir = "tdata" 

# Définition des couleurs
red = "\033[91m"  # Rouge
reset = "\033[0m"  # Réinitialiser la couleur

# Fonction pour extraire les membres d'un groupe/canal
def extraire_membres():
    while True:
        print(f"Sélectionnez une session dans le dossier '{sessions_dir}':")
        print("-" * 50)  # Séparateur visuel
        sessions = [f for f in os.listdir(sessions_dir) if f.endswith('.session')]

        if not sessions:
            print("Aucune session trouvée dans le dossier.")
            return

        # Afficher la liste des sessions disponibles
        for i, session in enumerate(sessions):
            print(f"    [{i + 1}] {session}")

        session_choice = int(input("Choisissez une session (numéro) : ")) - 1

        if session_choice < 0 or session_choice >= len(sessions):
            print("Choix invalide.")
            return

        selected_session = sessions[session_choice]
        print("-" * 50)  # Séparateur visuel après la sélection

        # Utilisation de l'API ID et API Hash existants
        api_id = 123456  # Remplacez par votre API ID déjà défini
        api_hash = 'votre_api_hash'  # Remplacez par votre API Hash déjà défini

        # Créer le client Telegram avec la session sélectionnée
        client = TelegramClient(os.path.join(sessions_dir, selected_session), api_id, api_hash)

        groupe = input("Entrez le nom d'utilisateur ou l'ID du groupe/canal : ")
        print("-" * 50)  # Séparateur visuel après la saisie du nom du groupe

        try:
            client.start()

            # Vérifier si l'utilisateur est déjà membre du groupe/canal
            try:
                client.get_entity(groupe)
                print(f"Vous êtes déjà membre du groupe/canal {groupe}.")
            except Exception:
                rejoindre = input(f"Vous n'êtes pas membre du groupe/canal {groupe}. Voulez-vous le rejoindre ? (o/n) : ").lower()
                if rejoindre == 'o':
                    client(JoinChannelRequest(groupe))
                    print(f"Vous avez rejoint le groupe/canal {groupe}.")

            print("-" * 50)  # Séparateur visuel après la vérification de l'adhésion

            # Demander à l'utilisateur de nommer le fichier CSV
            nom_fichier = input("Entrez le nom du fichier CSV pour enregistrer les membres (sans extension) : ") + ".csv"
            chemin_fichier = os.path.join(members_dir, nom_fichier)  # Chemin complet du fichier

            # Poser des questions pour filtrer les membres
            print("-" * 50)  # Séparateur visuel
            scraper_recents = input("Voulez-vous scraper seulement les membres récemment en ligne ? (o/n) : ").lower() == 'o'
            print("-" * 50)  # Séparateur visuel
            exclure_inactifs = input("Voulez-vous exclure les membres inactifs ? (o/n) : ").lower() == 'o'
            print("-" * 50)  # Séparateur visuel
            exclure_premium = input("Voulez-vous exclure les membres premium ? (o/n) : ").lower() == 'o'

            # Définir le filtre en fonction des choix de l'utilisateur
            membres = client.get_participants(groupe)

            # Compteurs pour les membres exclus
            count_exclus = 0

            print("\n")  # Ajouter une ligne vide pour espacer la barre de chargement

            # Sauvegarder les membres dans un fichier CSV
            with open(chemin_fichier, "w", newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Nom d'utilisateur", "Nom complet", "Est Premium"])

                # Utiliser tqdm pour afficher la barre de progression
                for membre in tqdm(membres, desc="Extraction des membres", unit="membre", bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} membres', colour='cyan'):
                    if exclure_inactifs and not membre.status:  # Exclure les inactifs
                        count_exclus += 1
                        continue
                    if exclure_premium and getattr(membre, 'premium', False):
                        count_exclus += 1
                        continue  # Sauter les membres premium si l'option est sélectionnée
                    username = membre.username if membre.username else "N/A"
                    full_name = f"{membre.first_name} {membre.last_name}".strip() or "N/A"
                    est_premium = "Oui" if getattr(membre, 'premium', False) else "Non"
                    writer.writerow([membre.id, username, full_name, est_premium])

            print(f"\nMembres extraits et enregistrés dans {chemin_fichier}.")

            # Résumé de l'extraction
            total_membres = len(membres)
            print(f"\nTotal des membres extraits : {total_membres}")
            print(f"{red}Total des membres exclus : {count_exclus}{reset}")

            # Analyse des membres
            count_premium = sum(1 for m in membres if getattr(m, 'premium', False))
            print(f"Pourcentage de membres premium : {count_premium / total_membres * 100:.2f}%")

        except Exception as e:
            print(f"Erreur lors de l'extraction des membres : {e}")

        finally:
            client.disconnect()

        # Demander à l'utilisateur s'il souhaite scraper un autre groupe ou revenir au menu principal
        choix = input("\nVoulez-vous scraper un autre groupe ? (o/n) ou taper 'm' pour revenir au menu principal : ").lower()
        if choix == 'n' or choix == 'm':
            break
            
            
# Fonction pour extraire les messages entrants
def extraire_messages_entrants():
    groupe = input("Entrez le nom d'utilisateur ou l'ID du groupe/canal/membre : ")
    if os.path.exists(fichier_comptes):
        with open(fichier_comptes, 'r') as f:
            comptes = list(csv.reader(f))
        for acc in comptes:
            client = TelegramClient(f"{dossier_sessions}/{acc[0]}", api_id, api_hash)
            try:
                client.start()
                messages = client.get_messages(groupe, limit=100, filter=PeerUser)
                with open('messages_entrants.csv', 'w', newline='') as mf:
                    writer = csv.writer(mf)
                    for msg in messages:
                        writer.writerow([msg.sender_id, msg.date, msg.message])
                print(f"{cyan}Messages entrants extraits et enregistrés dans messages_entrants.csv.{reset}")
                break
            except Exception as e:
                print(f"{rose}Erreur lors de l'extraction des messages entrants : {e}{reset}")
                break
    else:
        print(f"{rose}Aucun compte trouvé.{reset}")

# Fonction pour extraire des liens
def extraire_liens():
    groupe = input("Entrez le nom d'utilisateur ou l'ID du groupe/canal : ")
    if os.path.exists(fichier_comptes):
        with open(fichier_comptes, 'r') as f:
            comptes = list(csv.reader(f))
        for acc in comptes:
            client = TelegramClient(f"{dossier_sessions}/{acc[0]}", api_id, api_hash)
            try:
                client.start()
                messages = client.get_messages(groupe, limit=100)
                liens = [msg.message for msg in messages if msg.entities]
                with open('liens.csv', 'w', newline='') as lf:
                    writer = csv.writer(lf)
                    for lien in liens:
                        writer.writerow([lien])
                print(f"{cyan}Liens extraits et enregistrés dans liens.csv.{reset}")
                break
            except Exception as e:
                print(f"{rose}Erreur lors de l'extraction des liens : {e}{reset}")
                break
    else:
        print(f"{rose}Aucun compte trouvé.{reset}")

# Fonction pour scraper les membres récemment en ligne
def scraper_recentement_en_ligne():
    groupe = input("Entrez le nom d'utilisateur ou l'ID du groupe/canal : ")
    if os.path.exists(fichier_comptes):
        with open(fichier_comptes, 'r') as f:
            comptes = list(csv.reader(f))
        for acc in comptes:
            client = TelegramClient(f"{dossier_sessions}/{acc[0]}", api_id, api_hash)
            try:
                client.start()
                membres = client.get_participants(groupe)
                membres_recentement_en_ligne = [membre for membre in membres if membre.status and isinstance(membre.status, PeerChannel)]
                with open('membres_recentement_en_ligne.csv', 'w', newline='') as mf:
                    writer = csv.writer(mf)
                    for membre in membres_recentement_en_ligne:
                        writer.writerow([membre.first_name, membre.last_name])
                print(f"{cyan}Membres récemment en ligne extraits et enregistrés dans membres_recentement_en_ligne.csv.{reset}")
                break
            except Exception as e:
                print(f"{rose}Erreur lors du scraping des membres récemment en ligne : {e}{reset}")
                break
    else:
        print(f"{rose}Aucun compte trouvé.{reset}")

# Fonction pour scraper les membres actuellement en ligne
def scraper_actuellement_en_ligne():
    groupe = input("Entrez le nom d'utilisateur ou l'ID du groupe/canal : ")
    if os.path.exists(fichier_comptes):
        with open(fichier_comptes, 'r') as f:
            comptes = list(csv.reader(f))
        for acc in comptes:
            client = TelegramClient(f"{dossier_sessions}/{acc[0]}", api_id, api_hash)
            try:
                client.start()
                membres = client.get_participants(groupe)
                membres_actuellement_en_ligne = [membre for membre in membres if membre.status == "online"]
                with open('membres_actuellement_en_ligne.csv', 'w', newline='') as mf:
                    writer = csv.writer(mf)
                    for membre in membres_actuellement_en_ligne:
                        writer.writerow([membre.first_name, membre.last_name])
                print(f"{cyan}Membres actuellement en ligne extraits et enregistrés dans membres_actuellement_en_ligne.csv.{reset}")
                break
            except Exception as e:
                print(f"{rose}Erreur lors du scraping des membres actuellement en ligne : {e}{reset}")
                break
    else:
        print(f"{rose}Aucun compte trouvé.{reset}")

# Fonction pour exclure les membres premium du scraping
def exclure_membres_premium():
    groupe = input("Entrez le nom d'utilisateur ou l'ID du groupe/canal : ")
    if os.path.exists(fichier_comptes):
        with open(fichier_comptes, 'r') as f:
            comptes = list(csv.reader(f))
        for acc in comptes:
            client = TelegramClient(f"{dossier_sessions}/{acc[0]}", api_id, api_hash)
            try:
                client.start()
                membres = client.get_participants(groupe)
                membres_non_premium = [membre for membre in membres if not membre.is_premium]
                with open('membres_non_premium.csv', 'w', newline='') as mf:
                    writer = csv.writer(mf)
                    for membre in membres_non_premium:
                        writer.writerow([membre.first_name, membre.last_name])
                print(f"{cyan}Membres non premium extraits et enregistrés dans membres_non_premium.csv.{reset}")
                break
            except Exception as e:
                print(f"{rose}Erreur lors de l'exclusion des membres premium : {e}{reset}")
                break
    else:
        print(f"{rose}Aucun compte trouvé.{reset}")

def get_api_info_from_csv(telephone):
    """Récupère l'API ID et l'API Hash à partir du fichier API.csv en fonction du numéro de téléphone."""
    api_csv_path = os.path.join(sessions_dir, 'API.csv')
    with open(api_csv_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Numéro de téléphone'] == telephone:
                return row['API_ID'], row['API_HASH']
    print(f"Aucune information d'API trouvée pour le numéro {telephone}")
    return None, None

async def ajouter_membre(client, groupe, membre):
    """Ajoute un membre spécifique à un groupe donné."""
    try:
        await client(InviteToChannelRequest(groupe, [membre]))
        print(f"Ajouté avec succès : {membre}")
    except UserPrivacyRestrictedError:
        print(f"Le membre {membre} a des paramètres de confidentialité restreints.")
    except FloodWaitError as e:
        print(f"FloodWaitError : Attente de {e.seconds} secondes.")
        await asyncio.sleep(e.seconds)

def get_api_info_from_csv(telephone):
    """Récupère l'API ID et l'API Hash à partir du fichier API.csv en fonction du numéro de téléphone."""
    api_csv_path = os.path.join(sessions_dir, 'API.csv')
    with open(api_csv_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Numéro de téléphone'] == telephone:
                return int(row['API_ID']), row['API_HASH']
    print(f"Aucune information d'API trouvée pour le numéro {telephone}")
    return None, None

async def ajouter_membre(client, groupe, membre):
    """Ajoute un membre spécifique à un groupe donné."""
    try:
        await client(InviteToChannelRequest(groupe, [membre]))
        print(f"Ajouté avec succès : {membre}")
    except UserPrivacyRestrictedError:
        print(f"Le membre {membre} a des paramètres de confidentialité restreints.")
    except FloodWaitError as e:
        print(f"FloodWaitError : Attente de {e.seconds} secondes.")
        await asyncio.sleep(e.seconds)

# Fonction asynchrone pour ajouter des membres
async def ajouter_membres():
    while True:
        print(f"Sélectionnez une session dans le dossier '{sessions_dir}':")
        print("-" * 50)  # Séparateur visuel
        sessions = [f for f in os.listdir(sessions_dir) if f.endswith('.session')]

        if not sessions:
            print("Aucune session trouvée dans le dossier.")
            return

        # Afficher la liste des sessions disponibles
        for i, session in enumerate(sessions):
            print(f"    [{i + 1}] {session}")

        session_choice = input("Choisissez les numéros des sessions (séparés par des virgules) : ")
        session_choices = [int(choice.strip()) - 1 for choice in session_choice.split(",")]

        selected_sessions = []
        for choice in session_choices:
            if 0 <= choice < len(sessions):
                selected_sessions.append(sessions[choice])
            else:
                print("Choix invalide.")
                return

        # Choisir le groupe
        groupe = input("Entrez le nom d'utilisateur ou l'ID du groupe : ")
        print("-" * 50)  # Séparateur visuel après la saisie du nom du groupe

        try:
            delai_entre_ajouts = float(input("Entrez le délai entre chaque ajout (en secondes) : "))

            # Lister les fichiers CSV disponibles
            members_dir = os.path.join(os.path.dirname(__file__), 'members')
            csv_files = [f for f in os.listdir(members_dir) if f.endswith('.csv')]

            if not csv_files:
                print("Aucun fichier CSV trouvé dans le dossier 'members'.")
                return

            print("Fichiers disponibles :")
            for i, file in enumerate(csv_files):
                print(f"    [{i + 1}] {file}")

            file_choice = int(input("Choisissez le fichier CSV (numéro) : ")) - 1
            if file_choice < 0 or file_choice >= len(csv_files):
                print("Choix invalide.")
                return

            members_file = os.path.join(members_dir, csv_files[file_choice])

            # Charger les membres du fichier CSV
            membres = []
            try:
                with open(members_file, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        if 'ID' in row:
                            membres.append(row['ID'])
                        else:
                            print("Erreur : la colonne 'ID' est manquante dans le fichier CSV.")
                            return
            except Exception as e:
                print(f"Erreur lors de la lecture du fichier CSV : {e}")
                return

            # Ajouter les membres pour chaque session
            for session_file in selected_sessions:
                phone = session_file.split(".")[0]
                api_id, api_hash = get_api_info_from_csv(phone)

                if not api_id or not api_hash:
                    print(f"Impossible de trouver les informations API pour le compte {phone}.")
                    continue

                session_path = os.path.join(sessions_dir, session_file)
                client = TelegramClient(session_path, int(api_id), api_hash)

                try:
                    await client.start()
                    for membre_id in membres:
                        await ajouter_membre(client, groupe, membre_id)
                        await asyncio.sleep(delai_entre_ajouts)
                except Exception as e:
                    print(f"Erreur avec le compte {phone} : {e}")
                finally:
                    await client.disconnect()

        except Exception as e:
            print(f"Erreur lors de l'ajout de membres : {e}")

        # Demander à l'utilisateur s'il souhaite ajouter des membres à un autre groupe
        choix = input("\nVoulez-vous ajouter des membres à un autre groupe ? (o/n) : ").lower()
        if choix != 'o':
            break

def get_api_info_from_csv(phone):
    # Lire le fichier API.csv pour obtenir API_ID et API_HASH
    api_file_path = os.path.join(sessions_dir, 'API.csv')
    with open(api_file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Numéro de téléphone'] == phone:
                return row['API_ID'], row['API_HASH']
    return None, None

# Fonction pour envoyer des messages en masse

async def choisir_fichier(dossier):
    """Lister les fichiers dans un dossier et permettre à l'utilisateur de choisir un fichier."""
    fichiers = [f for f in os.listdir(dossier) if f.endswith('.csv')]
    
    if not fichiers:
        print("Aucun fichier CSV trouvé.")
        return None

    print("Fichiers disponibles :")
    for i, fichier in enumerate(fichiers):
        print(f"{i + 1}: {fichier}")

    choice = input("Choisissez le numéro du fichier : ")
    
    try:
        selected_file = fichiers[int(choice) - 1]
        return os.path.join(dossier, selected_file)
    except (IndexError, ValueError):
        print("Choix invalide.")
        return None

async def choisir_sessions():
    """Lister les sessions disponibles et permettre à l'utilisateur de choisir plusieurs sessions."""
    sessions = [f for f in os.listdir(sessions_dir) if f.endswith('.session')]
    
    if not sessions:
        print("Aucune session trouvée.")
        return []

    print("Sessions disponibles :")
    for i, session in enumerate(sessions):
        print(f"{i + 1}: {session}")

    choices = input("Choisissez les numéros des sessions (séparés par des virgules) : ")
    selected_sessions = []

    for choice in choices.split(','):
        try:
            selected_sessions.append(sessions[int(choice.strip()) - 1])
        except (IndexError, ValueError):
            print(f"Choix invalide : {choice.strip()}.")

    return selected_sessions

async def ajouter_membre(client, groupe, membre):
    try:
        await client(InviteToChannel(groupe, [membre[0]]))  # Membre à ajouter
        print(f"{cyan}Membre {membre[0]} ajouté avec succès au groupe {groupe}.{reset}")
    except Exception as e:
        print(f"{rose}Erreur lors de l'ajout de {membre[0]} : {e}{reset}")

async def ajouter_membres():
    fichier_membres = await choisir_fichier("members")
    if not fichier_membres:
        return

    groupe = input("Entrez le nom d'utilisateur ou l'ID du groupe : ")

    delai_entre_ajouts = float(input("Entrez le délai entre chaque ajout (en secondes) : "))

    membres = []
    with open(fichier_membres, 'r') as f:
        lecteurs = csv.reader(f)
        membres = list(lecteurs)

    comptes_utilises = await choisir_sessions()

    for compte in comptes_utilises:
        phone = compte.strip()
        client = TelegramClient(os.path.join(sessions_dir, phone))

        try:
            await client.start()
            for membre in membres:
                await ajouter_membre(client, groupe, membre)
                await asyncio.sleep(delai_entre_ajouts)  # Délai entre chaque ajout
        except Exception as e:
            print(f"{rose}Erreur avec le compte {phone} : {e}{reset}")
            
            
 #Fonction envoyer des messages en masse
 
async def envoyer_messages_en_masse():
    """Envoyer des messages en masse à partir d'un fichier CSV contenant des ID."""
    
    while True:  # Boucle principale pour permettre l'envoi de plusieurs fichiers
        # Lister les sessions disponibles
        sessions = [f for f in os.listdir(sessions_dir) if f.endswith('.session')]
        
        if not sessions:
            print("Aucune session trouvée.")
            return

        print("Sessions disponibles :")
        for i, session in enumerate(sessions):
            print(f"{i + 1}: {session}")

        choix_sessions = input("Choisissez les numéros des sessions à utiliser (séparés par des virgules) : ")
        choix_sessions = [sessions[int(i) - 1] for i in choix_sessions.split(',') if i.isdigit()]

        if not choix_sessions:
            print("Aucune session sélectionnée.")
            return

        # Lister les fichiers CSV dans le dossier 'members' au même niveau que le script
        members_dir = os.path.join(os.path.dirname(__file__), 'members')
        fichiers_csv = [f for f in os.listdir(members_dir) if f.endswith('.csv')]
        
        if not fichiers_csv:
            print("Aucun fichier CSV trouvé dans le dossier 'members'.")
            return

        print("Fichiers CSV disponibles dans le dossier 'members' :")
        for i, fichier in enumerate(fichiers_csv):
            print(f"{i + 1}: {fichier}")

        choix_fichier = input("Choisissez le numéro du fichier CSV à utiliser : ")
        try:
            csv_path = os.path.join(members_dir, fichiers_csv[int(choix_fichier) - 1])
        except (IndexError, ValueError):
            print("Choix de fichier invalide.")
            continue

        # Lire le fichier CSV et récupérer les ID
        try:
            with open(csv_path, mode='r') as file:
                reader = csv.DictReader(file)
                ids_utilisateurs = [(int(row['ID']), int(row['access_hash'])) for row in reader]  # Changer 'user_id' à 'ID'
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier CSV : {e}")
            return

        message = input("Entrez le message à envoyer : ")
        
        # Demander à l'utilisateur combien de secondes attendre entre chaque envoi
        try:
            intervalle = float(input("Entrez le temps d'attente entre chaque envoi de message (en secondes) : "))
        except ValueError:
            print("Veuillez entrer un nombre valide.")
            return

        for session in choix_sessions:
            session_path = os.path.join(sessions_dir, session)
            telephone = session.split('.')[0]
            api_id, api_hash = get_api_info_from_csv(telephone)

            if not api_id or not api_hash:
                print(f"Impossible de trouver les informations API pour {session}.")
                continue

            try:
                async with TelegramClient(session_path, api_id, api_hash) as client:
                    for user_id, access_hash in ids_utilisateurs:
                        try:
                            user = InputPeerUser(user_id=user_id, access_hash=access_hash)
                            await client(SendMessageRequest(user, message))
                            print(f"[SUCCÈS] Message envoyé à {user_id} depuis {session}.")
                        except PeerFloodError:
                            print(f"[ERREUR] Peer flood error pour {user_id} depuis {session}. Essayez de réduire la fréquence des messages.")
                            break
                        except UserPrivacyRestrictedError:
                            print(f"[ERREUR] La vie privée de l'utilisateur {user_id} restreint l'envoi de messages depuis {session}.")
                        except Exception as e:
                            print(f"[ERREUR] Erreur lors de l'envoi du message à {user_id} depuis {session} : {e}")

                        # Attendre l'intervalle spécifié avant d'envoyer le prochain message
                        await asyncio.sleep(intervalle)

            except Exception as e:
                print(f"Erreur lors de la connexion avec la session {session} : {e}")

        print("Envoi de messages terminé.")

        # Demander à l'utilisateur s'il souhaite envoyer d'autres messages
        encore = input("Souhaitez-vous envoyer d'autres messages à partir d'un autre fichier CSV ? (o/n) : ")
        if encore.lower() != 'o':
            break

# Fonction pour gérer le message d'absence (AFK)
def message_absence():
    print("Entrez le numéro de téléphone du compte à utiliser : ")
    phone = input().strip()
    
    message = input("Entrez le message d'absence : ")
    client = TelegramClient(f"{sessions_dir}/{phone}", api_id, api_hash)

    try:
        client.start()
        # Configurer le message d'absence
        client.send_message('me', message)  # Envoyer le message à soi-même
        print(f"{cyan}Message d'absence configuré pour le compte {phone} : {message}{reset}")

    except Exception as e:
        print(f"{rose}Erreur lors de la configuration du message d'absence avec le compte {phone} : {e}{reset}")
        

# Fonction pour rejoindre un groupe/canal
def rejoindre_groupe():
    print("Entrez le numéro de téléphone des comptes à utiliser (séparés par des virgules) : ")
    comptes_utilises = input().split(',')
    
    cible = input("Entrez le lien ou le nom d'utilisateur du groupe/canal à rejoindre : ")

    for compte in comptes_utilises:
        phone = compte.strip()
        client = TelegramClient(f"{sessions_dir}/{phone}", api_id, api_hash)

        try:
            client.start()
            # Rejoindre le groupe ou canal
            client(JoinChannel(cible))
            print(f"{cyan}Compte {phone} a rejoint le groupe/canal {cible}.{reset}")
        except Exception as e:
            print(f"{rose}Erreur lors de la tentative de rejoindre le groupe/canal avec le compte {phone} : {e}{reset}")

# Fonction pour quitter un groupe/canal
def quitter_groupe():
    print("Entrez le numéro de téléphone des comptes à utiliser (séparés par des virgules) : ")
    comptes_utilises = input().split(',')
    
    cible = input("Entrez le lien ou le nom d'utilisateur du groupe/canal à quitter : ")

    for compte in comptes_utilises:
        phone = compte.strip()
        client = TelegramClient(f"{sessions_dir}/{phone}", api_id, api_hash)

        try:
            client.start()
            # Quitter le groupe ou canal
            client(LeaveChannel(cible))
            print(f"{cyan}Compte {phone} a quitté le groupe/canal {cible}.{reset}")
        except Exception as e:
            print(f"{rose}Erreur lors de la tentative de quitter le groupe/canal avec le compte {phone} : {e}{reset}")

# Fonction pour afficher le menu d'adhésion
def afficher_menu_adhesion():
    print(f"\n{cyan}•-----• MENU D'ADHÉSION •-----•{reset}")
    print(f"    [27] Rejoindre des groupes/canaux")
    print(f"    [28] Quitter des groupes/canaux")
    
    
# Fonction pour augmenter les vues des publications avec comptes
def augmenter_vues_avec_comptes():
    lien_publication = input("Entrez le lien de la publication : ")
    nombre_de_vues = int(input("Entrez le nombre de vues à augmenter : "))
    
    comptes_utilises = input("Entrez les numéros de téléphone des comptes à utiliser (séparés par des virgules) : ").split(',')
    
    for compte in comptes_utilises:
        phone = compte.strip()
        client = TelegramClient(f"{sessions_dir}/{phone}", api_id, api_hash)

        try:
            client.start()
            for _ in range(nombre_de_vues):
                # Ici, vous pouvez implémenter une logique pour augmenter les vues
                print(f"{cyan}Compte {phone} a augmenté les vues sur {lien_publication}.{reset}")
                time.sleep(random.uniform(0.5, 1.5))  # Délai aléatoire entre chaque vue
        except Exception as e:
            print(f"{rose}Erreur avec le compte {phone} : {e}{reset}")

# Fonction pour réagir aux publications/messages
def reagir_aux_publications():
    lien_publication = input("Entrez le lien de la publication ou du message : ")
    reaction = input("Entrez la réaction que vous souhaitez envoyer (ex: 👍, ❤️, etc.) : ")
    
    comptes_utilises = input("Entrez les numéros de téléphone des comptes à utiliser (séparés par des virgules) : ").split(',')

    for compte in comptes_utilises:
        phone = compte.strip()
        client = TelegramClient(f"{sessions_dir}/{phone}", api_id, api_hash)

        try:
            client.start()
            # Simulation de l'envoi de réaction
            print(f"{cyan}Compte {phone} a réagi à {lien_publication} avec {reaction}.{reset}")
            time.sleep(random.uniform(0.5, 1.5))  # Délai aléatoire entre chaque réaction
        except Exception as e:
            print(f"{rose}Erreur avec le compte {phone} : {e}{reset}")

# Fonction pour voter dans les sondages
def voter_dans_les_sondages():
    lien_sondage = input("Entrez le lien du sondage : ")
    choix = input("Entrez votre choix (ex: 1, 2, etc.) : ")
    
    comptes_utilises = input("Entrez les numéros de téléphone des comptes à utiliser (séparés par des virgules) : ").split(',')

    for compte in comptes_utilises:
        phone = compte.strip()
        client = TelegramClient(f"{sessions_dir}/{phone}", api_id, api_hash)

        try:
            client.start()
            # Simulation du vote
            print(f"{cyan}Compte {phone} a voté pour le choix {choix} dans le sondage {lien_sondage}.{reset}")
            time.sleep(random.uniform(0.5, 1.5))  # Délai aléatoire entre chaque vote
        except Exception as e:
            print(f"{rose}Erreur avec le compte {phone} : {e}{reset}")

# Fonction pour afficher le menu des vues/réactions/sondages
def afficher_menu_vues_reactions_sondages():
    print(f"\n{cyan}•-----• MENU DES VUES / RÉACTIONS / SONDAGES •-----•{reset}")
    print(f"    [29] Augmenter les vues des publications sans comptes")
    print(f"    [30] Augmenter les vues des publications avec comptes")
    print(f"    [31] Réactions aux publications/messages")
    print(f"    [32] Vote dans les sondages")

            
# Boucle principale
if __name__ == "__main__":
    afficher_entete()
    while True:
        afficher_menu()
        choice = input()
        
        if choice == '1':
            connecter_comptes()
        elif choice == '2':
            deconnecter_compte()
        elif choice == '3':
            lister_sessions()
        elif choice == '4':
            verifier_spam()
        elif choice == '5':
            verifier_bannissement()
        elif choice == '6':
            asyncio.run(changer_prenom())  # Modifier le prénom
        elif choice == '7':
            asyncio.run(changer_nom_utilisateur())  # Modifier le nom d'utilisateur
        elif choice == '8':
            asyncio.run(changer_photo_profil())  # Modifier la photo de profil
        elif choice == '9':
            asyncio.run(changer_nom_famille())  # Modifier le nom de famille
        elif choice == '10':
            asyncio.run(changer_bio())  # Modifier la biographie
        elif choice == '11':
            extraire_membres()
        elif choice == '12':
            extraire_messages()
        elif choice == '15':
            scraper_recentement_en_ligne()
        elif choice == '18':
            asyncio.run(ajouter_membres())  # Appeler la fonction asynchrone correctement
        elif choice == '19':
            asyncio.run(envoyer_messages_en_masse())
        elif choice == '20':
            transferer_anciens_messages()
        elif choice == '21':
            obtenir_id_message()
        elif choice == '24':
            copier_anciens_messages()
        elif choice == '25':
            copier_nouveaux_messages()
        elif choice == '26':
            message_absence()
        elif choice == '27':
            rejoindre_groupe()
        elif choice == '28':
            quitter_groupe()
        elif choice == '29':
            augmenter_vues_sans_comptes()
        elif choice == '30':
            augmenter_vues_avec_comptes()
        elif choice == '31':
            reagir_aux_publications()
        elif choice == '32':
            voter_dans_les_sondages()
        elif choice.lower() == 'exit':
            print("Sortie...")
            break
        else:
            print(f"{rose}Option invalide. Veuillez réessayer.{reset}")            


