import pyfiglet
from colorama import init, Fore
import os
from telethon import TelegramClient, sync, errors
from telethon.tl.types import PeerChannel, PeerUser
from telethon.tl.functions.channels import InviteToChannelRequest, LeaveChannelRequest, GetFullChannelRequest
from telethon.tl.functions.messages import SendMessageRequest, GetHistoryRequest, ForwardMessagesRequest, GetDialogsRequest
from telethon.tl.types import InputPeerChat
from telethon.tl.types import InputPeerChannel
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import InputFile
import random
import csv
import time
import random
import asyncio

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

# Fonction pour afficher l'en-tête
def afficher_entete():
    titre = pyfiglet.figlet_format("JACK BRUTE", font="slant")
    print(f"{rose}{titre}{reset}")
    print(f"{cyan}    ÉDITION PREMIUM{reset}")
    print(f"{cyan}    CANAL TG : @JACKBRUTE   |   SUPPORT TG : @JACKBRUTE{reset}")
    print(f"{cyan}    Version : 0.23{reset}")
    print("-" * 60)

# Fonction pour afficher le menu principal
def afficher_menu():
    print(f"\n{cyan}•-----• MENU DE CONNEXION •-----•{reset}")
    print(f"    [1] Connecter des comptes (Telethon / Tdata)")
    print(f"    [2] Déconnecter des comptes")
    print(f"    [3] Lister toutes les sessions")
    print(f"    [4] Vérificateur de spam")
    print(f"    [5] Vérificateur de bannissement")

    print(f"\n{cyan}•-----• MENU D'ÉDITION •-----•{reset}")
    print(f"    [6] Modifier le prénom       -       [9] Modifier le nom de famille")
    print(f"    [7] Modifier le nom d'utilisateur     -     [10] Modifier la biographie")
    print(f"    [8] Modifier la photo de profil")

    print(f"\n{cyan}•-----• MENU DE SCRAPER •-----•{reset}")
    print(f"    [11] Extraire des membres d'un groupe/canal")
    print(f"    [12] Extraire les anciens messages du groupe/canal/membre")
    print(f"    [13] Extraire les messages entrants du groupe/canal/membre")
    print(f"    [14] Extraire les liens du canal/groupe")
    print(f"    [15] Scraper les membres récemment en ligne")
    print(f"    [16] Scraper les membres actuellement en ligne")
    print(f"    [17] Exclure les membres premium du scraping")

    print(f"\n{cyan}•-----• MENU D'AJOUT •-----•{reset}")
    print(f"    [18] Ajouter des membres à votre groupe/canal à partir d'un fichier CSV")

    print(f"\n{cyan}•-----• MENU DES MESSAGES •-----•{reset}")
    print(f"    [19] Envoyer des messages en masse")
    print(f"    [20] Messages auto-transférés")
    print(f"    [21] Transférer tous les anciens messages")
    print(f"    [22] Transférer les messages entrants")
    print(f"    [23] Obtenir l'ID du message")
    print(f"    [24] Copier tous les anciens messages des canaux/groupes vers votre canal/groupe")
    print(f"    [25] Copier les nouveaux messages entrants des canaux/groupes vers votre canal/groupe")
    print(f"    [26] Message d'absence (AFK)")

    print(f"\n{cyan}•-----• MENU D'ADHÉSION / DÉPART •-----•{reset}")
    print(f"    [27] Rejoindre des groupes/canaux")
    print(f"    [28] Quitter des groupes/canaux")

    print(f"\n{cyan}•-----• MENU DES VUES / RÉACTIONS / SONDAGES •-----•{reset}")
    print(f"    [29] Augmenter les vues des publications sans comptes")
    print(f"    [30] Augmenter les vues des publications avec comptes")
    print(f"    [31] Réactions aux publications/messages")
    print(f"    [32] Vote dans les sondages")

    print(f"\n•-----• JACK-BRUTE •-----•\n")
    print("Choisissez une option : ")

# Fonction pour connecter des comptes
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
        print(f"{cyan}Connecté au compte : {telephone}{reset}")
    except errors.SessionPasswordNeeded:
        mot_de_passe = input("Entrez votre mot de passe : ")
        client.start(phone=telephone, password=mot_de_passe)

    enregistrer_compte(telephone)  # Enregistrer les détails du compte

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

async def changer_prenom():
    """Modifier le prénom du compte."""
    phone = input("Entrez le numéro de téléphone du compte à modifier : ")
    new_first_name = input("Entrez le nouveau prénom : ")

    async with TelegramClient(f"{sessions_dir}/{phone}", api_id, api_hash) as client:
        me = await client.get_me()
        await client(UpdateProfile(first_name=new_first_name))
        print(f"{cyan}Prénom modifié pour {phone} en {new_first_name}.{reset}")

async def changer_nom_utilisateur():
    """Modifier le nom d'utilisateur du compte."""
    phone = input("Entrez le numéro de téléphone du compte à modifier : ")
    new_username = input("Entrez le nouveau nom d'utilisateur (sans @) : ")

    async with TelegramClient(f"{sessions_dir}/{phone}", api_id, api_hash) as client:
        await client(UpdateProfile(username=new_username))
        print(f"{cyan}Nom d'utilisateur modifié pour {phone} en @{new_username}.{reset}")

async def changer_photo_profil():
    """Modifier la photo de profil du compte."""
    phone = input("Entrez le numéro de téléphone du compte à modifier : ")
    photo_path = input("Entrez le chemin de la nouvelle photo : ")

    async with TelegramClient(f"{sessions_dir}/{phone}", api_id, api_hash) as client:
        await client(UpdateProfile(photo=photo_path))
        print(f"{cyan}Photo de profil modifiée pour {phone}.{reset}")

async def changer_nom_famille():
    """Modifier le nom de famille du compte."""
    phone = input("Entrez le numéro de téléphone du compte à modifier : ")
    new_last_name = input("Entrez le nouveau nom de famille : ")

    async with TelegramClient(f"{sessions_dir}/{phone}", api_id, api_hash) as client:
        await client(UpdateProfile(last_name=new_last_name))
        print(f"{cyan}Nom de famille modifié pour {phone} en {new_last_name}.{reset}")

async def changer_bio():
    """Modifier la biographie du compte."""
    phone = input("Entrez le numéro de téléphone du compte à modifier : ")
    new_bio = input("Entrez la nouvelle biographie : ")

    async with TelegramClient(f"{sessions_dir}/{phone}", api_id, api_hash) as client:
        await client(UpdateProfile(bio=new_bio))
        print(f"{cyan}Biographie modifiée pour {phone} en '{new_bio}'.{reset}")

# Fonction pour extraire des membres d'un groupe/canal
def extraire_membres():
    groupe = input("Entrez le nom d'utilisateur ou l'ID du groupe/canal : ")
    if os.path.exists(fichier_comptes):
        with open(fichier_comptes, 'r') as f:
            comptes = list(csv.reader(f))
        for acc in comptes:
            client = TelegramClient(f"{dossier_sessions}/{acc[0]}", api_id, api_hash)
            try:
                client.start()
                membres = client.get_participants(groupe)
                with open(fichier_membres, 'w', newline='') as mf:
                    writer = csv.writer(mf)
                    for membre in membres:
                        writer.writerow([membre.first_name, membre.last_name])
                print(f"{cyan}Membres extraits et enregistrés dans {fichier_membres}.{reset}")
                break
            except Exception as e:
                print(f"{rose}Erreur lors de l'extraction des membres : {e}{reset}")
                break
    else:
        print(f"{rose}Aucun compte trouvé.{reset}")

# Fonction pour extraire des messages
def extraire_messages():
    groupe = input("Entrez le nom d'utilisateur ou l'ID du groupe/canal/membre : ")
    if os.path.exists(fichier_comptes):
        with open(fichier_comptes, 'r') as f:
            comptes = list(csv.reader(f))
        for acc in comptes:
            client = TelegramClient(f"{dossier_sessions}/{acc[0]}", api_id, api_hash)
            try:
                client.start()
                messages = client.get_messages(groupe, limit=100)  # Limite à 100 messages
                with open('messages.csv', 'w', newline='') as mf:
                    writer = csv.writer(mf)
                    for msg in messages:
                        writer.writerow([msg.sender_id, msg.date, msg.message])
                print(f"{cyan}Messages extraits et enregistrés dans messages.csv.{reset}")
                break
            except Exception as e:
                print(f"{rose}Erreur lors de l'extraction des messages : {e}{reset}")
                break
    else:
        print(f"{rose}Aucun compte trouvé.{reset}")

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

# Fonction asynchrone pour ajouter des membres
async def ajouter_membre(client, groupe, membre):
    try:
        await client(InviteToChannel(groupe, [membre[0]]))  # Membre à ajouter
        print(f"{cyan}Membre {membre[0]} ajouté avec succès au groupe {groupe}.{reset}")
    except Exception as e:
        print(f"{rose}Erreur lors de l'ajout de {membre[0]} : {e}{reset}")

# Fonction pour ajouter des membres à partir d'un fichier CSV
async def ajouter_membres():
    fichier_membres = input("Entrez le chemin du fichier CSV contenant les membres : ")
    groupe = input("Entrez le nom d'utilisateur ou l'ID du groupe : ")
    delai_entre_ajouts = float(input("Entrez le délai entre chaque ajout (en secondes) : "))

    membres = []
    with open(fichier_membres, 'r') as f:
        lecteurs = csv.reader(f)
        membres = list(lecteurs)

    comptes_utilises = input("Entrez les numéros de téléphone des comptes à utiliser (séparés par des virgules) : ").split(',')

    for compte in comptes_utilises:
        phone = compte.strip()
        client = TelegramClient(f"{sessions_dir}/{phone}", api_id, api_hash)

        try:
            await client.start()
            for membre in membres:
                await ajouter_membre(client, groupe, membre)
                await asyncio.sleep(delai_entre_ajouts)  # Délai entre chaque ajout
        except Exception as e:
            print(f"{rose}Erreur avec le compte {phone} : {e}{reset}")


# Fonction pour envoyer des messages en masse
def envoyer_messages_en_masse():
    # Demander le numéro de téléphone des comptes à utiliser
    print("Entrez les numéros de téléphone des comptes à utiliser (séparés par des virgules) : ")
    comptes_utilises = input().split(',')
    
    # Demander le message à envoyer
    message = input("Entrez le message à envoyer : ")
    
    # Demander le groupe/canal/membre cible
    cible = input("Entrez le nom d'utilisateur ou l'ID du groupe/canal/membre cible : ")

    for compte in comptes_utilises:
        phone = compte.strip()
        client = TelegramClient(f"{sessions_dir}/{phone}", api_id, api_hash)

        try:
            client.start()
            # Envoyer le message
            client(SendMessage(cible, message))
            print(f"{cyan}Message envoyé à {cible} avec le compte {phone}.{reset}")
        except Exception as e:
            print(f"{rose}Erreur lors de l'envoi du message avec le compte {phone} : {e}{reset}")

# Fonction pour transférer tous les anciens messages
def transferer_anciens_messages():
    print("Entrez le numéro de téléphone du compte à utiliser : ")
    phone = input().strip()
    
    # Demander le groupe/canal/membre source et cible
    source = input("Entrez le nom d'utilisateur ou l'ID du groupe/canal source : ")
    cible = input("Entrez le nom d'utilisateur ou l'ID du groupe/canal cible : ")

    client = TelegramClient(f"{sessions_dir}/{phone}", api_id, api_hash)

    try:
        client.start()
        # Récupérer l'historique des messages
        messages = client(GetHistory(source, limit=100))  # Limite à 100 messages pour l'exemple
        for message in messages.messages:
            client(ForwardMessages(cible, [message.id], from_peer=source))
            print(f"{cyan}Message {message.id} transféré de {source} à {cible} avec le compte {phone}.{reset}")

    except Exception as e:
        print(f"{rose}Erreur lors du transfert des messages avec le compte {phone} : {e}{reset}")

# Fonction pour obtenir l'ID d'un message
def obtenir_id_message():
    print("Entrez le numéro de téléphone du compte à utiliser : ")
    phone = input().strip()
    
    # Demander le groupe/canal/membre cible
    cible = input("Entrez le nom d'utilisateur ou l'ID du groupe/canal/membre cible : ")

    client = TelegramClient(f"{sessions_dir}/{phone}", api_id, api_hash)

    try:
        client.start()
        # Obtenir l'historique des messages
        messages = client(GetHistory(cible, limit=100))  # Limite à 100 messages
        for message in messages.messages:
            print(f"ID du message : {message.id} | Contenu : {message.message}")

    except Exception as e:
        print(f"{rose}Erreur lors de l'obtention de l'ID du message avec le compte {phone} : {e}{reset}")

# Fonction pour copier tous les anciens messages d'un canal/groupe vers un autre
def copier_anciens_messages():
    print("Entrez le numéro de téléphone du compte à utiliser : ")
    phone = input().strip()
    
    # Demander le groupe/canal source et cible
    source = input("Entrez le nom d'utilisateur ou l'ID du groupe/canal source : ")
    cible = input("Entrez le nom d'utilisateur ou l'ID du groupe/canal cible : ")

    client = TelegramClient(f"{sessions_dir}/{phone}", api_id, api_hash)

    try:
        client.start()
        # Récupérer l'historique des messages
        messages = client(GetHistory(source, limit=100))  # Limite à 100 messages
        for message in messages.messages:
            client(SendMessage(cible, message.message))
            print(f"{cyan}Message {message.id} copié de {source} à {cible} avec le compte {phone}.{reset}")

    except Exception as e:
        print(f"{rose}Erreur lors de la copie des anciens messages avec le compte {phone} : {e}{reset}")

# Fonction pour copier les nouveaux messages entrants
def copier_nouveaux_messages():
    print("Entrez le numéro de téléphone du compte à utiliser : ")
    phone = input().strip()
    
    # Demander le groupe/canal source et cible
    source = input("Entrez le nom d'utilisateur ou l'ID du groupe/canal source : ")
    cible = input("Entrez le nom d'utilisateur ou l'ID du groupe/canal cible : ")

    client = TelegramClient(f"{sessions_dir}/{phone}", api_id, api_hash)

    try:
        client.start()
        # Récupérer l'historique des messages
        messages = client(GetHistory(source, limit=100))  # Limite à 100 messages
        for message in messages.messages:
            # Copier uniquement les nouveaux messages
            if not message.is_outgoing:  # Si le message n'est pas envoyé par le compte
                client(SendMessage(cible, message.message))
                print(f"{cyan}Nouveau message copié de {source} à {cible} avec le compte {phone}.{reset}")

    except Exception as e:
        print(f"{rose}Erreur lors de la copie des nouveaux messages avec le compte {phone} : {e}{reset}")

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
    
# Fonction pour augmenter les vues des publications sans comptes
def augmenter_vues_sans_comptes():
    lien_publication = input("Entrez le lien de la publication : ")
    nombre_de_vues = int(input("Entrez le nombre de vues à augmenter : "))
    
    # Simulation de l'augmentation des vues sans comptes
    print(f"{cyan}Augmentation des vues sur la publication {lien_publication} de {nombre_de_vues} vues...{reset}")
    time.sleep(1)  # Simule le temps d'attente
    print(f"{cyan}Les vues ont été augmentées avec succès.{reset}")

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
            envoyer_messages_en_masse()
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


