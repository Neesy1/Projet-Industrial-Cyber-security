import os
import subprocess

# On définit le chemin du dossier où se trouvent tous tes scripts
DOSSIER_PROJET = "/home/sylvain/Documents/Projet_Indus"

def nettoyer_ecran():
    os.system('clear')

def menu_principal():
    nettoyer_ecran()
    print("""
    ###########################################
    #                HACKER TOOL              #
    #                Version: 1.0             #
    ###########################################
    """)
    print(" [1] SCANNER LE RÉSEAU (Local)")
    print(" [2] ATTAQUE FORCE BRUTE ")
    print(" [3] OPTIONS SYSTÈME")
    print(" [q] QUITTER")
    
    choix = input("\n[>] Faites votre choix : ")

    if choix == "1":
        lancer_script("scan.py")
    elif choix == "2":
        print("\n[!] Ce module est en cours de développement...")
        input("\nAppuyez sur Entrée pour revenir au menu.")
        menu_principal()
    elif choix == "3":
        infos_systeme()
    elif choix.lower() == "q":
        print("\nFermeture du programme. À bientôt !")
    else:
        print("\n[!] Choix invalide.")
        input("Appuyez sur Entrée...")
        menu_principal()

def lancer_script(nom_fichier):
    """Lance un script .py situé dans le même dossier"""
    chemin_complet = os.path.join(DOSSIER_PROJET, nom_fichier)
    
    if os.path.exists(chemin_complet):
        print(f"\n--- Lancement de {nom_fichier} ---")
        # On utilise subprocess pour garder un meilleur contrôle
        subprocess.run(["python3", chemin_complet])
        print("\n--- Fin du module ---")
    else:
        print(f"\n[!] Erreur : Le fichier {nom_fichier} est introuvable dans {DOSSIER_PROJET}")
    
    input("\nAppuyez sur Entrée pour retourner au menu principal...")
    menu_principal()

def infos_systeme():
    nettoyer_ecran()
    print("--- INFORMATIONS SYSTÈME ---")
    os.system("uname -a")
    print("\n--- UTILISATION DISQUE ---")
    os.system("df -h | grep '^/dev/'")
    input("\nAppuyez sur Entrée...")
    menu_principal()

if __name__ == "__main__":
    menu_principal()
